import os
import requests
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request

load_dotenv(find_dotenv())


def format_time_get_date(value):
    date = datetime.fromtimestamp(value).strftime('%d-%m-%Y')
    return date


def format_time_get_time(value):
    time = datetime.fromtimestamp(value).strftime('%H:%M')
    return time


def get_day_category(value):
    hours = int(datetime.fromtimestamp(value).hour)
    timeOfDay = ""
    if 24 > hours > 18:
        timeOfDay = "NIGHT"
    elif 18 > hours > 12:
        timeOfDay = "AFTERNOON"
    elif hours < 12:
        timeOfDay = "MORNING"

    return timeOfDay


app = Flask(__name__)
app.config['DEBUG'] = True
app.jinja_env.filters['format_time_get_date'] = format_time_get_date
app.jinja_env.filters['format_time_get_time'] = format_time_get_time
app.jinja_env.filters['get_day_category'] = get_day_category


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        URL = 'http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid={api_key}'
        city = request.form.get('city')
        api_key = os.getenv("OPEN_WEATHER_API_KEY")
        try:
            weather = requests.get(URL.format(
                city=city, api_key=api_key)).json()
        except Exception as e:
            print(f"Error in processing request")
        if weather["cod"] == 200:
            weather['dt'] = weather['dt'] + weather['timezone']
            timeOfDay = get_day_category(weather['dt'])
            weather['text_color'] = 'black' if timeOfDay == 'MORNING' else 'white'
            weather['background'] = os.path.join(timeOfDay.lower()+'.jpeg')
            return render_template('weather.html', weather=weather)
        else:
            # PASS A RELEVANT MESSAGE IF CITY ENTERED IS INCORRECT
            pass
    return render_template('weather.html')


if __name__ == '__main__':
    app.run()

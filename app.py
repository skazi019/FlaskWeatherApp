import os
import requests
from datetime import date, datetime
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request

load_dotenv(find_dotenv())


def format_time_get_date(value):
    date = datetime.fromtimestamp(value).strftime('%d-%m-%Y')
    return date


def get_day_category(hour):
    if 6 <= int(hour) <= 16:
        return 'MORNING'
    elif 17 <= int(hour) <= 23:
        return 'AFTERNOON'
    elif 0 <= int(hour) <= 5:
        return 'NIGHT'
    else:
        return 'MORNING'


app = Flask(__name__)
app.config['DEBUG'] = True
app.jinja_env.filters['format_time_get_date'] = format_time_get_date
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
            # print(f"unix time is: {weather['dt']}")
            offset = int(weather.get('timezone'))
            dt = int(weather.get('dt'))
            local_hour = dt + offset
            local_hour = int(datetime.utcfromtimestamp(
                local_hour).strftime('%H'))
            timeOfDay = get_day_category(local_hour)
            weather['timeOfDay'] = timeOfDay
            weather['top_text_color'] = 'black' if timeOfDay == 'MORNING' or timeOfDay == 'AFTERNOON' else 'white'
            weather['bottom_text_color'] = 'black' if timeOfDay == 'MORNING' else 'white'
            weather['background'] = os.path.join(timeOfDay.lower()+'.jpeg')
            return render_template('weather.html', weather=weather)
        else:
            pass
    return render_template('weather.html')


if __name__ == '__main__':
    app.run()

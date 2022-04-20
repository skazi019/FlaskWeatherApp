import os
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

URL = 'http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid={api_key}'
city = 'mumbai'
api_key = os.getenv("OPEN_WEATHER_API_KEY")

weather = requests.get(URL.format(city=city, api_key=api_key)).json()
print(weather['name'])

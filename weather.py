import requests
import pytz
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

from main import API_WEATHER


class CityWeather:
    @staticmethod
    async def get_weather(city):
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(city)
        obj = TimezoneFinder()

        try:
            result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
        except AttributeError as e:
            print("Weather App", "Invalid city name")

        api = f"https://api.openweathermap.org/data/2.5/weather?lat={location.latitude}&lon={location.longitude}&appid={API_WEATHER}"

        json_data = requests.get(api).json()
        weather = json_data["weather"][0]["main"]
        weather_desc = json_data["weather"][0]["description"]
        temp = round(json_data["main"]["temp"] - 273.15, 2)
        temp_feels_like = round(json_data["main"]["feels_like"] - 273.15, 2)
        pressure = json_data["main"]["pressure"]
        visibility = json_data["visibility"]
        wind = json_data["wind"]["speed"]
        city_name = json_data["name"]

        weather_msg = f"The current tempreature in <em>{city_name}</em> is {temp}° and it feels like {temp_feels_like}°\n\
Weather description: <em>{weather}, {weather_desc}</em>.\n\
Pressure: <em>{pressure} hPa</em>.\n\
Visibility: <em>{visibility} km</em>.\n\
Wind speed: <em>{wind} m/s</em>."
        return weather_msg

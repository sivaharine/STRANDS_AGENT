from strands import tool
import requests
from config import WEATHER_API_KEY

@tool
def get_weather(city: str):

    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"

    r = requests.get(url)

    data = r.json()

    return f"The weather in {city} is {data['current']['temp_c']}°C and {data['current']['condition']['text']}"
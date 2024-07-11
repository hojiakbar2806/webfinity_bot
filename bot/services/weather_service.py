import json
import aiohttp

from bot.middlewares.logging_middleware import logger
from data.config import settings


async def fetch_weather_data(lat, lon, username):
    url = f"https://weatherapi-com.p.rapidapi.com/current.json?q={lat},{lon}"
    headers = {
        'x-rapidapi-key': settings.RAPIDAPI_KEY,
        'x-rapidapi-host': "weatherapi-com.p.rapidapi.com"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            res = await response.json()
            logger.info(
                f"{username}: {res['location']['name']} {res['location']['region']} {res['location']['country']}")
            logger.info(f"Request: {url} it's <{response.status}>")
            return res


async def weather_info(weather_data):
    location = weather_data['location']
    current = weather_data['current']

    message = f"""
Joylashuv: {location['name']}, {location['region']}, {location['country']}
    
Kenglik: {location['lat']}
Uzunlik: {location['lon']}
Mahalliy vaqt: {location['localtime']}

Joriy ob-havo:
- So'nggi yangilangan: {current['last_updated']}
- Harorat: {current['temp_c']}°C / {current['temp_f']}°F
- Holat: {current['condition']['text']}
- Shamol: {current['wind_mph']} mph / {current['wind_kph']} kph ({current['wind_dir']})
- Bosim: {current['pressure_mb']} mb / {current['pressure_in']} in
- Namlik: {current['humidity']}%
- Bulutlilik: {current['cloud']}%
- Seziladigan harorat: {current['feelslike_c']}°C / {current['feelslike_f']}°F
- Ko'rinish: {current['vis_km']} km / {current['vis_miles']} miles
- UV indeksi: {current['uv']}
- Shamol tezligi: {current['gust_mph']} mph / {current['gust_kph']} kph"""
    return message

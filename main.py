import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import requests

from config import TOKEN
from config import WEATHER_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()
CITY_NAME = 'Moscow'
# Функция для получения прогноза погоды
def get_weather(city_name):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': WEATHER_API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        return f"Погода в {city_name}:\nТемпература: {temperature}°C\nОписание: {description}"
    else:
        return "Не удалось получить данные о погоде."

@dp.message(Command('weather'))
async def send_weather(message: Message):
    weather_info = get_weather(CITY_NAME)
    await message.reply(weather_info)


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды: \n /start \n /help')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я бот, который может предоставить прогноз погоды. Напишите /weather, чтобы узнать погоду в Москве.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
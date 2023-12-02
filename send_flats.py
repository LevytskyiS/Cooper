import requests
from configparser import ConfigParser
from pathlib import Path

from aiogram.types.input_file import InputFile


config = ConfigParser()
config.read("C:/Users/Berzerk/Documents/GitHub/Cooper/config.ini")

FLATS = config.get("TG", "FLATS")
API_KEY = config.get("TG", "API_KEY")
MY_ID = config.get("TG", "MY_ID")

f = open(FLATS, "rb")

url = f"https://api.telegram.org/bot{API_KEY}/sendDocument"

payload = {
    "chat_id": MY_ID,
}
headers = {
    "accept": "application/json",
    "User-Agent": "Telegram Bot SDK - (https://github.com/irazasyed/telegram-bot-sdk)",
    "content-type": "application/json",
}

files = {"document": f}

response = requests.post(url, data=payload, files=files)
# print(response.text)

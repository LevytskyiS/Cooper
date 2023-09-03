import random

import requests

from conf import bot, MY_ID
from commands import cats_stickers


class MotivationalQuote:
    @staticmethod
    async def get_quote():
        url = "https://zenquotes.io/api/today"
        response = requests.get(url)
        json_data = response.json()

        msg = f"<em>{json_data[0]['q']}</em>\n\n<b>{json_data[0]['a']}</b>"
        return msg

    @staticmethod
    async def send_q_to_me():
        msg = await MotivationalQuote.get_quote()
        await bot.send_message(chat_id=MY_ID, text=msg, parse_mode="HTML")
        await bot.send_sticker(chat_id=MY_ID, sticker=random.choice(cats_stickers))

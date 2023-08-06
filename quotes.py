import random

import requests

from main import bot
from commands import cats_stickers


class MotivationalQuote:
    @staticmethod
    async def get_quote():
        url = "https://zenquotes.io/api/today"
        response = requests.get(url)
        json_data = response.json()

        msg = f"<em>{json_data[0]['q']}</em>\n\n<b>{json_data[0]['a']}</b>"
        # msg2 = json_data[0]["h"]
        return msg

    @staticmethod
    async def send_q_to_me():
        msg = await MotivationalQuote.get_quote()
        await bot.send_message(chat_id=200930937, text=msg, parse_mode="HTML")
        await bot.send_sticker(chat_id=200930937, sticker=random.choice(cats_stickers))

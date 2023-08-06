import random

import requests


class MotivationalQuote:
    @staticmethod
    async def get_quote():
        url = "https://zenquotes.io/api/today"
        response = requests.get(url)
        json_data = response.json()

        msg = f"<em>{json_data[0]['q']}</em>\n\n<b>{json_data[0]['a']}</b>"
        # msg2 = json_data[0]["h"]
        return msg

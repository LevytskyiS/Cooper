import aioschedule

import asyncio
from pytz import timezone

from quotes import MotivationalQuote


async def schedule_func():
    try:
        aioschedule.every().day.at("06:30").do(MotivationalQuote.send_q_to_me)
        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(5)

    except Exception as error:
        print(error)

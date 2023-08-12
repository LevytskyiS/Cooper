import aioschedule

import asyncio
from pytz import timezone

from quotes import MotivationalQuote
from pokemon import SendPokemon


async def schedule_func():
    try:
        aioschedule.every().day.at("07:28").do(MotivationalQuote.send_q_to_me)
        # aioschedule.every().day.at("07:31").do(SendPokemon.send_pokemon)
        aioschedule.every(4).seconds.do(SendPokemon.send_me_pokemon)
        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(5)

    except Exception as error:
        print(error)

import aioschedule
import asyncio

from quotes import MotivationalQuote
from jobcz.vacancies import NewVacancies


async def schedule_func():
    try:
        aioschedule.every().day.at("06:30").do(MotivationalQuote.send_q_to_me)

        # aioschedule.every().day.at("10:00").do(NewVacancies.send_me_report)
        # aioschedule.every().day.at("12:00").do(NewVacancies.send_me_report)
        # aioschedule.every().day.at("14:00").do(NewVacancies.send_me_report)
        # aioschedule.every().day.at("16:00").do(NewVacancies.send_me_report)
        # aioschedule.every().day.at("18:00").do(NewVacancies.send_me_report)

        # aioschedule.every().day.at("08:00").do(SearchFlats.send_me_new_flats)
        # aioschedule.every().day.at("10:00").do(SearchFlats.send_me_new_flats)
        # aioschedule.every().day.at("12:00").do(SearchFlats.send_me_new_flats)
        # aioschedule.every().day.at("14:00").do(SearchFlats.send_me_new_flats)
        # aioschedule.every().day.at("16:00").do(SearchFlats.send_me_new_flats)
        # aioschedule.every().day.at("18:00").do(SearchFlats.send_me_new_flats)
        # aioschedule.every().day.at("20:00").do(SearchFlats.send_me_new_flats)

        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(1)

    except Exception as error:
        print(error)

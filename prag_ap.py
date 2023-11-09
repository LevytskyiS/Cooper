import time
import datetime
import asyncio
import re
import random

import requests
import pandas as pd
from bs4 import BeautifulSoup
from aiogram.types.input_file import InputFile

from ch_driver import GetChromeDriver
from conf import bot, MY_ID

NUMS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


class PragueApartments:
    """Collect data from sreality."""

    @staticmethod
    async def get_page_source():
        """Get page source"""
        driver = await GetChromeDriver.get_chrome_driver()
        url = "https://www.sreality.cz/hledani/pronajem/byty/praha-1,praha-2,praha-3,praha-7?velikost=1%2B1,2%2Bkk&cena-od=0&cena-do=15000"
        # url = "https://www.sreality.cz/hledani/pronajem/byty/praha-7,praha-3,praha-2,praha-1?velikost=1%2B1,2%2Bkk&cena-od=0&cena-do=25000"
        driver.get(url)
        time.sleep(2)
        page = driver.page_source
        driver.close()
        driver.quit()

        return page

    @staticmethod
    async def get_basic_data():
        """Collect appartments' data."""
        result = []
        page = await PragueApartments.get_page_source()
        soup = BeautifulSoup(page, "lxml")
        flats = soup.find("div", class_="dir-property-list").find_all(
            "span", class_="basic"
        )

        for flat in flats:
            link = "https://www.sreality.cz" + flat.find("h2").find("a")["href"]
            flat_id = link.split("/")[-1]
            price_ = flat.find("span", class_="norm-price").text.split("Kč")[0].strip()
            price = int("".join([x for x in price_ if x in NUMS]))
            location = flat.find("span", class_="locality ng-binding").text
            result.append(
                {
                    "date": datetime.datetime.now(),
                    "f_id": flat_id,
                    "price": price,
                    "location": location,
                    "link": link,
                }
            )
        return result


class Bezrealitky:
    """Collect data from bezrealitky."""

    @staticmethod
    async def find_flats() -> list:
        flats = []
        urls = [
            "https://www.bezrealitky.cz/vyhledat?offerType=PRONAJEM&estateType=BYT&disposition=DISP_1_1&disposition=DISP_2_KK&priceTo=15000&regionOsmIds=R20000063962&osm_value=Praha+3%2C+Praha%2C+okres+Hlavní+město+Praha%2C+Hlavní+město+Praha%2C+Praha%2C+Česko",  # Prague 3
            "https://www.bezrealitky.cz/vyhledat?offerType=PRONAJEM&estateType=BYT&disposition=DISP_1_1&disposition=DISP_2_KK&priceTo=15000&regionOsmIds=R20000063928&osm_value=Praha+2%2C+Praha%2C+okres+Hlavní+město+Praha%2C+Hlavní+město+Praha%2C+Praha%2C+Česko",  # Prague 2
            "https://www.bezrealitky.cz/vyhledat?offerType=PRONAJEM&estateType=BYT&disposition=DISP_1_1&disposition=DISP_2_KK&priceTo=15000&regionOsmIds=R20000061612&osm_value=Praha+1%2C+Praha%2C+okres+Hlavní+město+Praha%2C+Hlavní+město+Praha%2C+Praha%2C+Česko",  # Prague 1
            "https://www.bezrealitky.cz/vyhledat?offerType=PRONAJEM&estateType=BYT&disposition=DISP_1_1&disposition=DISP_2_KK&priceTo=15000&regionOsmIds=R20000064370&osm_value=Praha+8%2C+Praha%2C+okres+Hlavní+město+Praha%2C+Hlavní+město+Praha%2C+Praha%2C+Česko",  # Prague 8
        ]

        for url in urls:
            response = requests.get(url)
            time.sleep(random.randint(1, 3))
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "lxml")

                articles = soup.find_all(
                    "article",
                    class_="PropertyCard_propertyCard__moO_5 propertyCard PropertyCard_propertyCard--landscape__XvPmC",
                )
                if articles:
                    flats += articles
                else:
                    continue

        return flats

    @staticmethod
    async def get_clean_data(flats: list):
        """Parse collected ads."""
        result = []

        for flat in flats:
            location = (
                flat.find(
                    "h2",
                    class_="PropertyCard_propertyCardHeadline___diKI mt-md-0 mt-4 mb-0",
                )
                .find(
                    "span",
                    class_="PropertyCard_propertyCardAddress__hNqyR text-subheadline text-truncate",
                )
                .text
            )

            link = flat.find(
                "h2",
                class_="PropertyCard_propertyCardHeadline___diKI mt-md-0 mt-4 mb-0",
            ).find("a")["href"]

            flat_id = re.findall("\d{3,10}", link)[0]

            price_ = flat.find(
                "span", class_="PropertyPrice_propertyPriceAmount__WdEE1"
            ).text.replace("Kč", "")
            price = int("".join([n for n in price_ if n in NUMS]))

            result.append(
                {
                    "date": datetime.datetime.now(),
                    "f_id": flat_id,
                    "price": price,
                    "location": location,
                    "link": link,
                }
            )
        return result

    @staticmethod
    async def get_basic_data():
        """Collect new flats for rent."""
        flats = await Bezrealitky.find_flats()
        if flats:
            clean_data = await Bezrealitky.get_clean_data(flats)
            return clean_data
        else:
            return None


class SearchFlats:
    @staticmethod
    async def get_new_flats():
        """Collect new flats for rent at bezrealitky and sreality."""
        flats = await asyncio.gather(
            Bezrealitky.get_basic_data(), PragueApartments.get_basic_data()
        )
        csv = await SearchFlats.get_csv(flats)
        return csv

    @staticmethod
    async def get_csv(flats: list):
        """Prepare a csv-file with collected appartments."""
        csv_file = "data/flats.csv"
        number_of_rows = len(pd.read_csv(csv_file)["date"])
        number_of_new_rows = 0

        for data in flats:
            if data:
                df = pd.read_csv(csv_file)
                checked_flats = await SearchFlats.check_existing_ids(df, data)

                if checked_flats:
                    dates = [d["date"] for d in checked_flats]
                    f_ids = [f["f_id"] for f in checked_flats]
                    prices = [p["price"] for p in checked_flats]
                    locations = [l["location"] for l in checked_flats]
                    links = [l["link"] for l in checked_flats]

                    ndf = pd.DataFrame(
                        {
                            "date": dates,
                            "f_id": f_ids,
                            "price": prices,
                            "location": locations,
                            "link": links,
                        }
                    )
                    ndf = ndf.sort_values(by="price", ascending=False).reset_index()
                    number_of_new_rows += len(ndf["date"])
                    df_to_save = pd.concat([df, ndf]).reset_index()
                    df_to_save.to_csv(
                        csv_file, columns=["date", "f_id", "price", "location", "link"]
                    )
                else:
                    continue

        return number_of_new_rows, csv_file

    @staticmethod
    async def check_existing_ids(df: pd.DataFrame, data: list):
        """Check collected appartments' ids."""
        result = []
        df_ids = df["f_id"]
        df_ids = [int(i) for i in df_ids]

        for flat in data:
            if int(flat["f_id"]) in df_ids:
                continue
            else:
                result.append(flat)

        return result

    @staticmethod
    async def send_me_new_flats():
        """Send file with new appartments to Telegram Bot."""
        new_flats, csv_file = await SearchFlats.get_new_flats()
        await bot.send_document(chat_id=MY_ID, document=InputFile(csv_file))
        if new_flats:
            await bot.send_message(
                chat_id=MY_ID, text=f"{new_flats} flat/s was/were found."
            )
        else:
            await bot.send_message(chat_id=MY_ID, text=f"No new flats were found.")


# asyncio.run(SearchFlats.send_me_new_flats())
# df = pd.DataFrame(columns=["date", "f_id", "price", "location", "link"])
# df.to_csv("data/flats2.csv")

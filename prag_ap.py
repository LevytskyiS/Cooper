import time
import datetime
import asyncio

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from aiogram.types.input_file import InputFile

from ch_driver import GetChromeDriver

NUMS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


class PragueApartments:
    @staticmethod
    async def get_page_source():
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
        result = []
        page = await PragueApartments.get_page_source()

        with open("page.txt", "w", encoding="utf-8") as file:
            file.write(page)

        with open("page.txt", "r", encoding="utf-8") as file:
            source = file.read()

        soup = BeautifulSoup(source, "lxml")
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

    @staticmethod
    async def check_existing_ids(df: pd.DataFrame, flats: list):
        result = []
        df_ids = df["f_id"]
        df_ids = [int(i) for i in df_ids]

        for flat in flats:
            if int(flat["f_id"]) in df_ids:
                continue
            else:
                result.append(flat)

        return result

    @staticmethod
    async def get_csv(flats: list):
        csv_file = "data/flats.csv"
        df = pd.read_csv(csv_file)
        checked_flats = await PragueApartments.check_existing_ids(df, flats)

        if not checked_flats:
            return "No new flats at the moment", csv_file

        else:
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

            df_to_save = pd.concat([df, ndf]).reset_index()

            df_to_save.to_csv(
                csv_file, columns=["date", "f_id", "price", "location", "link"]
            )

            return f"{len(checked_flats)} new apartments were found", csv_file

    @staticmethod
    async def get_new_flats():
        new_flats = await PragueApartments.get_basic_data()
        msg, csv_file = await PragueApartments.get_csv(new_flats)
        return msg, InputFile(csv_file)


# asyncio.run(PragueApartments.get_new_flats())

# df = pd.DataFrame(columns=["date", "f_id", "price", "location", "link"])
# df.to_csv("data/flats.csv")

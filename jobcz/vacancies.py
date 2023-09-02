import os
import sys
import datetime

sys.path.append(os.path.abspath("."))

import requests
import pandas as pd
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from aiogram.types.input_file import InputFile

from main import MY_ID, bot


class JobStack:
    @staticmethod
    async def ul_list() -> ResultSet:
        page_source = requests.get(
            "https://www.jobstack.it/it-jobs?positiontype=79&location=Praha&isDetail=0"
        ).text

        soup = BeautifulSoup(page_source, "lxml")
        ul_list = soup.find("ul", class_="jobposts-list").find_all("a")
        return ul_list

    @staticmethod
    async def get_links(ul: ResultSet) -> dict:
        desc = "it-job"
        url = "https://www.jobstack.it"
        links = [url + li["href"] for li in ul if desc in li["href"]]
        ids = [l.split("/")[-1] for l in links]
        return {"links": links, "id": ids}

    @staticmethod
    async def get_new_vacs() -> dict:
        ul = await JobStack.ul_list()
        job_links = await JobStack.get_links(ul)
        return job_links


class PraceCZ:
    @staticmethod
    async def ul_list() -> ResultSet:
        page_source = requests.get(
            "https://www.prace.cz/nabidky/praha/python-vyvojar/plny-uvazek/"
        ).text

        soup = BeautifulSoup(page_source, "lxml")
        ul_list = soup.find("ul", class_="search-result list-unstyled").find_all("a")
        return ul_list

    @staticmethod
    async def get_links(ul: ResultSet) -> dict:
        desc = "nabidka"
        links = list({li["href"] for li in ul if desc in li["href"]})
        ids = [l.split("/")[4] for l in links]
        return {"links": links, "id": ids}

    @staticmethod
    async def get_new_vacs() -> dict:
        ul = await PraceCZ.ul_list()
        job_links = await PraceCZ.get_links(ul)
        return job_links


class NewVacancies:
    @staticmethod
    async def send_me_report():
        msg, csv_file = NewVacancies.main()
        await bot.send_message(chat_id=MY_ID, text=msg)
        await bot.send_document(chat_id=MY_ID, document=InputFile(csv_file))

    @staticmethod
    async def main():
        vacs = await NewVacancies.get_new_vacs()
        msg, csv_file = await NewVacancies.prer_report(vacs)
        return msg, csv_file

    @staticmethod
    async def get_new_vacs():
        js = await JobStack.get_new_vacs()
        pcz = await PraceCZ.get_new_vacs()
        js["links"] += pcz["links"]
        js["id"] += pcz["id"]
        return js

    @staticmethod
    async def check_exist_links(df: pd.DataFrame, vacancies: dict) -> list:
        result = {"links": [], "id": []}
        df_id = df["ids"]
        df_id = [str(l) for l in df_id]
        for l, i in zip(vacancies.get("links"), vacancies.get("id")):
            if i in df_id:
                continue
            else:
                result["links"].append(l)
                result["id"].append(i)
        return result

    @staticmethod
    async def prer_report(vacancies: dict):
        csv_file = "data/vacancies.csv"
        df = pd.read_csv(csv_file)
        checked_vacs = await NewVacancies.check_exist_links(df, vacancies)

        if not checked_vacs:
            return "No new vacancies at the moment", csv_file

        else:
            ids = checked_vacs.get("id")
            links = checked_vacs.get("links")

            ndf = pd.DataFrame(
                {
                    "date": [datetime.datetime.now() for i in range(len(links))],
                    "link": links,
                    "ids": ids,
                }
            )

            ndf = ndf.sort_values(by="date", ascending=False).reset_index()

            df_to_save = pd.concat([df, ndf]).reset_index()
            df_to_save.to_csv(csv_file, columns=["date", "link", "ids"])

            return f"{len(links)} new vacancies were found", csv_file


# df = pd.DataFrame(columns=["date", "link", "price", "location", "ids"])
# df.to_csv("data/vacancies.csv")

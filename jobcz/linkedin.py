import time
import os
import sys
import asyncio
import random
import pickle

sys.path.append(os.path.abspath("."))

import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from ch_driver import GetChromeDriver
from conf import LINKEDIN_LOGIN, LINKEDIN_PASSWORD
from mongodb.models import Recruiter
from mongodb.connect import connect


class LinkedIn:
    @staticmethod
    async def get_recruiters():
        # all_recruiters = await LinkedIn.login_get_pages()
        # await LinkedIn.save_all_pages(all_recruiters)
        source = await LinkedIn.get_htmls()
        recr_data = await LinkedIn.get_recr_data(source)
        await LinkedIn.fill_db(recr_data)

    @staticmethod
    async def login_get_pages() -> list:
        linkedin = "https://www.linkedin.com"
        driver = await GetChromeDriver.get_chrome_driver()

        driver.get(linkedin)
        time.sleep(3)
        driver.find_element(
            By.XPATH,
            "//*[@id='artdeco-global-alert-container']/div/section/div/div[2]/button[2]",
        ).click()
        time.sleep(2)

        username = driver.find_element(By.XPATH, "//*[@id='session_key']")
        password = driver.find_element(By.XPATH, "//*[@id='session_password']")

        username.send_keys(LINKEDIN_LOGIN)
        time.sleep(3)
        password.send_keys(LINKEDIN_PASSWORD)
        time.sleep(5)

        log_btn = driver.find_element(
            By.XPATH, "//*[@id='main-content']/section[1]/div/div/form/div[2]/button"
        ).click()
        time.sleep(20)

        pages = []

        for i in range(1, 101):
            print(f"--- Page {i} is being collected ---")
            page = f'https://www.linkedin.com/search/results/people/?geoUrn=%5B"103973174"%2C"106156085"%5D&keywords=it%20recruiter&origin=FACETED_SEARCH&page={i}&sid=6P5'
            driver.get(page)
            time.sleep(random.randrange(3, 7))
            source = driver.page_source
            pages.append(source)
        driver.close()
        driver.quit()

        return pages

    @staticmethod
    async def save_all_pages(pages: list) -> None:
        file = "data/recrs.bin"
        with open(file, "wb") as fh:
            pickle.dump(pages, fh)
        print("Saved")

    @staticmethod
    async def get_htmls():
        file = "data/recrs.bin"
        with open(file, "rb") as fh:
            sources = pickle.load(fh)
            print("Loaded")
            return sources

    @staticmethod
    async def get_recr_data(sources: list):
        result = []
        for source in sources:
            soup = BeautifulSoup(source, "lxml")
            recruiters = soup.find_all("div", class_="entity-result__item")
            for recruiter in recruiters:
                link = recruiter.find("a", class_="app-aware-link")["href"]

                try:
                    name = recruiter.find("span", dir="ltr").find("span").text.strip()
                except AttributeError as err:
                    continue

                if link and name:
                    result.append({"name": name, "link": link})
        return result

    @staticmethod
    async def fill_db(recruiters: list):
        recr_ids = [i for i in range(1, len(recruiters) + 1)]
        for i, r in zip(recr_ids, recruiters):
            recruiter = Recruiter.objects(recr_id=i).first()
            if not recruiter:
                try:
                    recr = Recruiter(recr_id=i, name=r["name"], link=r["link"])
                    recr.save()
                    # print(f"User {recr.name} was created successfully.")
                except Exception as e:
                    print(e)
            else:
                print(f"The id '{recruiter.recr_id}' is already used.")


async def main():
    await LinkedIn.get_recruiters()


if __name__ == "__main__":
    asyncio.run(main())

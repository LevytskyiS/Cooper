from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class GetChromeDriver:
    @staticmethod
    async def get_chrome_driver() -> webdriver.Chrome:
        # def get_chrome_driver() -> webdriver.Chrome:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("window-size=1366x768")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=chrome_options)
        return driver

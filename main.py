from configparser import ConfigParser

from aiogram import Bot, Dispatcher

config = ConfigParser()
config.read("config.ini")

API_KEY = config.get("TG", "API_KEY")
API_WEATHER = config.get("TG", "API_WEATHER")
MY_ID = config.get("TG", "MY_ID")
API_MARVEL = config.get("TG", "API_MARVEL")
PUBLIC_MARVEL = config.get("TG", "PUBLIC_MARVEL")

bot = Bot(API_KEY)
dp = Dispatcher(bot)


def main():
    pass


if __name__ == "__main__":
    main()

from configparser import ConfigParser

from aiogram import Bot, Dispatcher

config = ConfigParser()
config.read("config.ini")

API_KEY = config.get("TG", "API_KEY")
MY_ID = config.get("TG", "MY_ID")
API_WEATHER = config.get("TG", "API_WEATHER")

API_MARVEL = config.get("TG", "API_MARVEL")
PUBLIC_MARVEL = config.get("TG", "PUBLIC_MARVEL")

LINKEDIN_LOGIN = config.get("TG", "LINKEDIN_LOGIN")
LINKEDIN_PASSWORD = config.get("TG", "LINKEDIN_PASSWORD")

USERNAME_MONGO = config.get("TG", "USERNAME_MONGO")
PASSWORD_MONGO = config.get("TG", "PASSWORD_MONGO")
CLUSTER_MONGO = config.get("TG", "CLUSTER_MONGO")
MONGO_DB_NAME = config.get("TG", "MONGO_DB_NAME")


bot = Bot(API_KEY)
dp = Dispatcher(bot)


def main():
    pass


if __name__ == "__main__":
    main()

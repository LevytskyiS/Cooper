from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

API_KEY = config.get("TG", "API_KEY")
API_WEATHER = config.get("TG", "API_WEATHER")


def main():
    pass


if __name__ == "__main__":
    main()

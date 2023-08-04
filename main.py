from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

API_KEY = config.get("TG", "API_KEY")


def main():
    pass


if __name__ == "__main__":
    main()

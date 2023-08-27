import requests


async def get_activity():
    uri = "https://www.boredapi.com/api/activity/"
    response = requests.get(uri).json()
    return response["activity"]

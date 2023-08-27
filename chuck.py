import random

import requests


jedi_chuck = "https://i.kym-cdn.com/photos/images/original/000/008/624/Chuck_Norris__Jedi_Master_by_timstuff.png"
serious_chuck = "https://i.kym-cdn.com/photos/images/original/000/008/640/Chuck_Norris_by_joranvanlook.jpg"
like_chuck = "https://i.kym-cdn.com/photos/images/original/000/012/774/omfg_chuck_norris_approves.gif"
dog_chuck = "https://i.kym-cdn.com/photos/images/original/000/097/728/chuck-norris-top-10-xl.jpg"
eminem_chuck = "https://i.kym-cdn.com/photos/images/original/000/172/079/tumblr_lr6u58yXj91qbypelo1_500.jpg"
darth_chuck = "https://i.kym-cdn.com/photos/images/original/000/863/220/fbb.jpg"
lego_chuck = "https://i.kym-cdn.com/photos/images/original/001/280/637/5cc.png"
mac_chuck = "https://i.kym-cdn.com/photos/images/original/001/304/726/879.jpg"

chucks_memes = [
    jedi_chuck,
    serious_chuck,
    like_chuck,
    dog_chuck,
    eminem_chuck,
    darth_chuck,
    lego_chuck,
    mac_chuck,
]


class ChuckJokes:
    @staticmethod
    async def get_joke():
        url = "https://api.chucknorris.io/jokes/random"
        response = requests.get(url)
        json_data = response.json()

        joke = json_data["value"]
        # icon = random.choice(chucks_memes)
        # icon = json_data["icon_url"]
        # return joke, icon
        return joke

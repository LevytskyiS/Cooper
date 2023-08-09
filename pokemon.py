import requests
import random


class SendPokemon:
    @staticmethod
    async def get_pokemon_name() -> str:
        url = "https://pokeapi.co/api/v2/pokemon/?limit=10000"
        response = requests.get(url)
        data = response.json()["results"]
        all_pokemon_names = [name["name"] for name in data]
        name = random.choice(all_pokemon_names)
        return name

    @staticmethod
    async def get_pokemon_image(data):
        image = data["sprites"]["other"]["official-artwork"]["front_default"]
        return image

    @staticmethod
    async def get_json_data(name: str):
        url = f"https://pokeapi.co/api/v2/pokemon/{name}/"
        response = requests.get(url)
        data = response.json()
        return data

    @staticmethod
    async def get_description(data):
        experience = data["base_experience"]
        if not experience:
            experience = "Unknown"
        height = data["height"]
        weight = data["weight"]
        return f"{data['name'].capitalize()}'s basic characteristics are 😈:\nExperience - {experience} exp.\nWeight - {weight} kg\nHeight - {height} dm."

    @staticmethod
    async def send_pokemon():
        pokemon = await SendPokemon.get_pokemon_name()
        pokemon_json = await SendPokemon.get_json_data(pokemon)
        image = await SendPokemon.get_pokemon_image(pokemon_json)
        description = await SendPokemon.get_description(pokemon_json)
        return pokemon.capitalize(), image, description

import asyncio
import random

from aiogram import types, executor
from aiogram.types import ReplyKeyboardRemove
from aiogram.types.input_file import InputFile

from main import API_KEY, bot, dp
from commands import START_MSG, HELP_MSG, DESC_MSG, WEATHER_MSG, cats_stickers
from keyboards import kb, ikb
from exchange import exch_rate_msg
from weather import CityWeather
from quotes import MotivationalQuote
from scheduler import schedule_func
from pokemon import SendPokemon
from chuck import ChuckJokes
from bored import get_activity
from prag_ap import PragueApartments


async def on_startup(_):
    print("The bot is running...")
    asyncio.create_task(schedule_func())


@dp.message_handler(commands=["start"])
async def start_cmd(msg: types.Message):
    await msg.answer(text=START_MSG)


@dp.message_handler(commands=["help"])
async def help_cmd(msg: types.Message):
    await msg.answer(text=HELP_MSG, reply_markup=kb)


@dp.message_handler(commands=["desc"])
async def desc_cmd(msg: types.Message):
    await msg.answer(text=DESC_MSG)
    await msg.delete()


@dp.message_handler(commands=["exchange_rate"])
async def exch_rate_cmd(msg: types.Message):
    await msg.answer(text=exch_rate_msg)


@dp.message_handler(commands=["weather"])
async def weather_cmd(msg: types.Message):
    await msg.answer(text=WEATHER_MSG, reply_markup=ikb)


@dp.message_handler(commands=["quote"])
async def quote_cmd(msg: types.Message):
    quote = await MotivationalQuote.get_quote()
    await msg.answer(text=quote, parse_mode="HTML")
    await bot.send_sticker(
        chat_id=msg.from_user.id, sticker=random.choice(cats_stickers)
    )
    await msg.delete()


@dp.callback_query_handler(lambda callback_query: callback_query.data)
async def weather_cb_handler(callback: types.CallbackQuery):
    msg_weather = await CityWeather.get_weather(callback.data)
    await callback.message.answer(text=msg_weather, parse_mode="HTML")


@dp.message_handler(commands=["pokemon"])
async def pokemon_cmd(msg: types.Message):
    name, image, description = await SendPokemon.send_pokemon()
    await msg.answer(text=f"{name} 🤩\n\n{description}")
    await bot.send_photo(chat_id=msg.from_user.id, photo=image)
    await msg.delete()


@dp.message_handler(commands=["chuck"])
async def chuck_norris_jokes_cmd(msg: types.Message):
    # joke, icon = await ChuckJokes.get_joke()
    joke = await ChuckJokes.get_joke()
    await msg.answer(text=joke)
    # await bot.send_photo(chat_id=msg.from_user.id, photo=icon)


@dp.message_handler(commands=["activity"])
async def activity_cmd(msg: types.Message):
    activity = await get_activity()
    await msg.answer(text=activity)


@dp.message_handler(commands=["prague"])
async def prague_flats_cmd(msg: types.Message):
    message, csv_file = await PragueApartments.get_new_flats()
    await msg.answer(text=message)
    await bot.send_document(chat_id=msg.from_user.id, document=InputFile(csv_file))


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

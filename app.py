from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardRemove

from main import API_KEY
from commands import START_MSG, HELP_MSG, DESC_MSG, WEATHER_MSG
from keyboards import kb, ikb
from exchange import exchange_rates
from weather import CityWeather

bot = Bot(API_KEY)
dp = Dispatcher(bot)


async def on_startup(_):
    print("Bot is starting...")


@dp.message_handler(commands=["start"])
async def start_cmd(msg: types.Message):
    await msg.answer(text=START_MSG)


@dp.message_handler(commands=["help"])
async def help_cmd(msg: types.Message):
    await msg.answer(text=HELP_MSG, reply_markup=kb)


@dp.message_handler(commands=["desc"])
async def desc_cmd(msg: types.Message):
    await msg.answer(text=DESC_MSG, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands=["exchange_rate"])
async def exch_rate_cmd(msg: types.Message):
    await msg.answer(text=exchange_rates, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands=["weather"])
async def weather_cmd(msg: types.Message):
    await msg.answer(text=WEATHER_MSG, reply_markup=ikb)


@dp.callback_query_handler(lambda callback_query: callback_query.data)
async def weather_cb_handler(callback: types.CallbackQuery):
    msg_weather = await CityWeather.get_weather(callback.data)
    await callback.message.answer(
        text=msg_weather, parse_mode="HTML", reply_markup=ReplyKeyboardRemove()
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

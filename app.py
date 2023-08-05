from aiogram import Bot, Dispatcher, types, executor

from main import API_KEY
from commands import START_MSG, HELP_MSG, DESC_MSG
from keyboards import kb

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
    await msg.answer(text=DESC_MSG, reply_markup=kb)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

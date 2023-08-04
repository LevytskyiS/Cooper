from aiogram import Bot, Dispatcher, executor, types

from main import API_KEY


bot = Bot(API_KEY)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(msg: types.Message):
    await msg.answer(text=msg.text)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

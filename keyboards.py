from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton


kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton("/help")
b2 = KeyboardButton("/desc")
b3 = KeyboardButton("/exchange_rate")

kb.add(b1).insert(b2).insert(b3)

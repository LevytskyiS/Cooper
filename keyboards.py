from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton("/help")
b2 = KeyboardButton("/desc")
b3 = KeyboardButton("/exchange_rate")
b4 = KeyboardButton("/weather")
b5 = KeyboardButton("/quote")
b6 = KeyboardButton("/pokemon")
b7 = KeyboardButton("/chuck")
b8 = KeyboardButton("/activity")
b9 = KeyboardButton("/prague")

kb.add(b1).insert(b2).insert(b3)
kb.add(b4).insert(b5).insert(b6)
kb.add(b7).insert(b8).insert(b9)

ikb = InlineKeyboardMarkup()
ib1 = InlineKeyboardButton(text="Prague", callback_data="Prague")
ib2 = InlineKeyboardButton(text="Ústí nad Labem", callback_data="Ústí nad Labem")
ib3 = InlineKeyboardButton(text="Teplice", callback_data="Teplice")
ib4 = InlineKeyboardButton(text="Šiauliai", callback_data="Šiauliai")
ib5 = InlineKeyboardButton(text="Vilnius", callback_data="Vilnius")
ib6 = InlineKeyboardButton(text="Kaunas", callback_data="Kaunas")
ib7 = InlineKeyboardButton(text="Riga", callback_data="Riga")
ib8 = InlineKeyboardButton(text="Tallinn", callback_data="Tallinn")
ib9 = InlineKeyboardButton(text="Helsinki", callback_data="Helsinki")
ikb.add(ib1, ib2, ib3, ib4, ib5, ib6, ib7, ib8, ib9)

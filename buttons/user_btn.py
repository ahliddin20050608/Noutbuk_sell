from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

option_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛍 Noutbuklar")],
        [KeyboardButton(text="📞 Aloqa")],
        [KeyboardButton(text="🤖 Botdan foydalanish")]
    ],
    resize_keyboard=True
)
choice_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🆕 Yangi"), KeyboardButton(text="♻️ Eski")],
        [KeyboardButton(text="🔙 Ortga")]
    ],
    resize_keyboard=True
)


category_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💻 Dasturlash"), KeyboardButton(text="📊 Office")],
        [KeyboardButton(text="🔙 Ortga")]
    ],
    resize_keyboard=True
)



# 🔹 Aloqa bo'limi chiroyli keyboard
contact_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📞 Admin bilan bog‘lanish")],  # telefon/telegram ko'rsatish uchun
        [KeyboardButton(text="✉️ Habar qoldirish")],         # xabar qoldirish
        [KeyboardButton(text="🔙 Ortga")]                     # asosiy menyuga qaytish
    ],
    resize_keyboard=True,  # tugmalar ekran o'lchamiga moslashadi
    one_time_keyboard=True  # foydalanuvchi bir marta bossin, keyin default keyboard chiqadi
)

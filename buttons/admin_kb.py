from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👤 Userlar"), KeyboardButton(text="💻 Laptoplar")],
        [KeyboardButton(text="➕ Laptop qo'shish"), KeyboardButton(text="💬 Javob berish")],
        [KeyboardButton(text="✉️ Habar yuborish (ID orqali)"), KeyboardButton(text="📊 Hisobot")],
        [ KeyboardButton(text="❌ Bekor qilish")],  # yangi tugma qo'shildi
    ],
    resize_keyboard=True
)


cancel_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="❌ Bekor qilish")]
    ],
    resize_keyboard=True
)

# KeyboardButton(text="📊 Admin xabarlar"),
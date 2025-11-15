from aiogram.types import Message, FSInputFile
from aiogram import Router, F, Bot
from buttons import START_TEXT, OPTION_TEXT, NEXT_MENU_TEXT, TEXT_CHOICE, REGISTRETED_TEXT
from database import is_registered_by_chat_id, get_laptops, get_admins, get_user_phone, save_user_message
from buttons import register_kb, option_kb, choice_kb, category_kb, contact_kb
import pdfkit
from environs import Env
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

# 🔹 Env va bot
env = Env()
env.read_env()
TOKEN = env.str("TOKEN")
bot = Bot(token=TOKEN)
 


class LeaveMessage(StatesGroup):
    waiting_for_message = State()
# 🔹 Router
user_router = Router()
user_choice = {}  # { user_id: {"status": "new/old"} }

# 🔹 Boshlang'ich bo'limlar: Noutbuklar / Aloqa
@user_router.message(F.text == "🛍 Noutbuklar")
async def choose_noutbuk(message: Message):
    uid = message.from_user.id
    if is_registered_by_chat_id(uid):
        await message.answer(
            text=OPTION_TEXT,
            reply_markup=choice_kb
        )
    else:
        await message.answer_photo(
            photo=FSInputFile("images/main_image2.jpg"),
            caption=START_TEXT,
            reply_markup=register_kb
        )

# 🔙 Ortga
@user_router.message(F.text == "🔙 Ortga")
async def back(message: Message):
    await message.answer(
        text=NEXT_MENU_TEXT,
        reply_markup=option_kb
    )

# 🔹 Mahsulot holati: Yangi / Eski
@user_router.message(F.text.in_(["🆕 Yangi", "♻️ Eski"]))
async def select_status(message: Message):
    uid = message.from_user.id
    if not is_registered_by_chat_id(uid):
        return await message.answer_photo(
            photo=FSInputFile("images/main_image2.jpg"),
            caption=START_TEXT,
            reply_markup=register_kb
        )

    status = "new" if message.text == "🆕 Yangi" else "old"
    user_choice[uid] = {"status": status}

    await message.answer(
        text=REGISTRETED_TEXT,
        reply_markup=category_kb
    )

# 🔹 Kategoriya bo'limlari
@user_router.message(F.text == "💻 Dasturlash")
async def programming_laptops(message: Message):
    await send_laptops_by_category(message, "programming")

@user_router.message(F.text == "📊 Office")
async def office_laptops(message: Message):
    await send_laptops_by_category(message, "office")

# 🔹 Umumiy funksiya: PDF va rasm/text yuborish
async def send_laptops_by_category(message: Message, category: str):
    uid = message.from_user.id
    status = user_choice.get(uid, {}).get("status")

    if not is_registered_by_chat_id(uid):
        return await message.answer_photo(
            photo=FSInputFile("images/main_image2.jpg"),
            caption=START_TEXT,
            reply_markup=register_kb
        )

    if not status:
        return await message.answer(
            "Avval 🆕 Yangi yoki ♻️ Eski tanlang!",
            reply_markup=choice_kb
        )

    laptops = get_laptops(category, status)
    if not laptops:
        return await message.answer("🚫 Hozircha bu bo‘limda mahsulot yo‘q")

    # 🔹 PDF fayl yaratish
    file_path = f"{uid}_{status}_{category}.pdf"

    html_content = f"""
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid black; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
    </head>
    <body>
        <h2>{status.capitalize()} {category.capitalize()} noutbuklari</h2>
        <table>
            <tr>
                <th>Title</th>
                <th>Brand</th>
                <th>CPU</th>
                <th>RAM</th>
                <th>Storage</th>
                <th>GPU</th>
                <th>Price</th>
            </tr>
    """

    for lap in laptops:
        html_content += f"""
            <tr>
                <td>{lap['title']}</td>
                <td>{lap['brand']}</td>
                <td>{lap['cpu'] if lap['cpu'] else '-'}</td>
                <td>{lap['ram'] if lap['ram'] else '-'}</td>
                <td>{lap['storage'] if lap['storage'] else '-'}</td>
                <td>{lap['gpu'] if lap['gpu'] else '-'}</td>
                <td>{lap['price']} 💰</td>
            </tr>
        """

    html_content += "</table></body></html>"

    # 🔹 wkhtmltopdf konfiguratsiyasi
    path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_string(html_content, file_path, configuration=config)

    # PDF yuborish
    await message.answer_document(FSInputFile(file_path), caption=f"💻 {status.capitalize()} {category.capitalize()} noutbuklari PDF")

    # 🔹 Oddiy rasm/text yuborish
    for laptop in laptops:
        text = f"""
    📌 {laptop['title']}
    💰 {laptop['price']} so'm
    ⚙️ CPU: {laptop['cpu'] if laptop['cpu'] else '-'}
    🧠 RAM: {laptop['ram'] if laptop['ram'] else '-'}
    💾 SSD: {laptop['storage'] if laptop['storage'] else '-'}
    🎮 GPU: {laptop['gpu'] if laptop['gpu'] else '-'}
    """
        try:
            await message.answer_photo(photo=FSInputFile(laptop["image"]), caption=text)
        except:
            await message.answer(text)


# 🔹 Aloqa bo‘limi
@user_router.message(F.text == "📞 Aloqa")
async def contact(message: Message):
    await message.answer(
        text=TEXT_CHOICE,
        reply_markup=contact_kb
    )

@user_router.message(F.text == "📞 Admin bilan bog‘lanish")
async def contact_admin(message: Message):
    text = (
        "📞 Admin bilan bog‘lanish:\n\n"
        "Telefon: +998 90 123 45 67\n"
        "Telegram: @AdminUsername\n\n"
        "🔙 Ortga tugmasi bilan asosiy menyuga qaytishingiz mumkin."
    )
    await message.answer(text=text, reply_markup=contact_kb)


@user_router.message(F.text == "✉️ Habar qoldirish")
async def leave_message_start(message: Message, state: FSMContext):
    await state.set_state(LeaveMessage.waiting_for_message)
    text = (
        "✉️ Habar qoldirish bo‘limi.\n\n"
        "Iltimos, xabaringizni shu yerga yuboring. "
        "Admin tez orada javob beradi.\n\n"
        "🔙 Ortga tugmasi bilan asosiy menyuga qaytishingiz mumkin."
    )
    await message.answer(text=text)

@user_router.message(LeaveMessage.waiting_for_message)
async def leave_message_receive(message: Message, state: FSMContext):
    """
    Foydalanuvchi yozgan matnni qabul qilish, DB ga saqlash va adminlarga yuborish
    """
    if not message.text:
        return await message.answer(
            "❗ Iltimos, matnli xabar yuboring yoki 🔙 Ortga tugmasi bilan chiqishingiz mumkin."
        )
    
    user_text = message.text.strip()
    
    if not user_text:
        return await message.answer(
            "❗ Iltimos, xabarni yozing yoki 🔙 Ortga tugmasi bilan chiqishingiz mumkin."
        )

    # Foydalanuvchi ma'lumotlari
    full_name = message.from_user.full_name
    user_id = message.from_user.id
    username = f"@{message.from_user.username}" if message.from_user.username else None
    phone = get_user_phone(user_id) or "-"

    # 🔹 DB ga saqlash
    
    save_user_message(
        chat_id=user_id,   # <- bu yerda user_id emas chat_id
        message_text=user_text
    )



    # 🔹 Adminlarga xabar yuborish
   
    admins = get_admins()
    for admin_id in admins:
        text_to_admin = f"📩 Yangi xabar:\n\n{user_text}\n\nFrom: {full_name} (ID: {user_id})"
        if username:
            text_to_admin += f" {username}"
        text_to_admin += f"\nTelefon: {phone}"
        await bot.send_message(admin_id, text_to_admin)

    await message.answer(
        "✅ Xabaringiz adminlarga yuborildi va DB ga saqlandi. Tez orada javob beriladi."
    )
    await state.clear()
# 🔹 Botdan foydalanish bo‘yicha qo‘llanma
@user_router.message(F.text == "🤖 Botdan foydalanish")
async def bot_guide(message: Message):
    text = """
🤖 Botdan foydalanish bo‘yicha qisqacha qo‘llanma:

1️⃣ Noutbuklar bo‘limidan yangi yoki eski noutbuklarni ko‘rishingiz mumkin.
2️⃣ Har bir kategoriya (Dasturlash / Office) bo‘yicha PDF yoki rasm shaklida ko‘rsatish mavjud.
3️⃣ Aloqa bo‘limi orqali admin bilan bog‘lanishingiz yoki xabar qoldirishingiz mumkin.
4️⃣ 🔙 Ortga tugmasi bilan asosiy menyuga qaytishingiz mumkin.
"""
    await message.answer(text, reply_markup=option_kb)

from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from database import is_admin, get_users, get_laptops, insert_laptop, get_admins, get_user_messages, get_admin_messages, save_admin_message
from buttons import admin_kb, cancel_kb, report_kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from states import AddLaptop, SendToUser
import pdfkit
from environs import Env
import os
from aiogram.types import ForceReply
import re

# 🔹 LeaveMessage state
class LeaveMessage(StatesGroup):
    waiting = State()

# 🔹 .env dan token o‘qish va bot yaratish
env = Env()
env.read_env()
TOKEN = env.str("TOKEN")
bot = Bot(token=TOKEN)

# 🔹 Router
admin_router = Router()

# 🔹 Admin start
@admin_router.message(Command("admin"))
async def start_admin(message: Message):
    if is_admin(message.from_user.id):
        await message.answer("Admin bo'limiga xush kelibsiz 😊", reply_markup=admin_kb)
    else:
        await message.answer("Siz admin emassiz 😂")

# 🔹 Foydalanuvchilar ro‘yxati (ID bilan)
@admin_router.message(F.text == "👤 Userlar")
async def get_all_users(message: Message):
    if not is_admin(message.from_user.id):
        return await message.answer("🚫 Siz admin emassiz!")

    users = get_users()  # bu yerda chat_id qaytaradigan qilib o'zgartiring
    if not users:
        return await message.answer("📭 Bazada userlar yo‘q!")

    html_content = """
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { font-family: DejaVu Sans, sans-serif; margin: 20px; background-color: #fafafa; }
            h2 { text-align: center; color: #333; margin-bottom: 20px; }
            table { width: 100%%; border-collapse: collapse; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: center; }
            th { background-color: #2196F3; color: white; }
        </style>
    </head>
    <body>
        <h2>📋 Foydalanuvchilar ro‘yxati</h2>
        <table>
            <tr>
                <th>ID</th>
                <th>Chat ID</th>
                <th>Ism</th>
                <th>Username</th>
                <th>Telefon</th>
            </tr>
    """

    for user in users:
        html_content += f"""
            <tr>
                <td>{user[0]}</td>
                <td>{user[1]}</td>
                <td>{user[2]}</td>
                <td>{user[3] or '-'}</td>
                <td>{user[4] or '-'}</td>
            </tr>
        """

    html_content += "</table></body></html>"

    config = pdfkit.configuration(
        wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    )
    pdf_path = "users.pdf"
    pdfkit.from_string(html_content, pdf_path, configuration=config)

    # PDFni yuborish
    await message.answer_document(
        FSInputFile(pdf_path),
        caption="📄 Foydalanuvchilar ro'yxati (ID va Chat ID bilan)"
    )
    os.remove(pdf_path)

# 🔹 Laptoplar ro‘yxati
@admin_router.message(F.text == "💻 Laptoplar")
async def get_all_laptops(message: Message):
    if not is_admin(message.from_user.id):
        return await message.answer("🚫 Siz admin emassiz!")

    laptops = get_laptops()
    if not laptops:
        return await message.answer("📭 Bazada noutbuklar yo‘q!")

    html_content = """
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { font-family: DejaVu Sans, sans-serif; margin: 20px; background: #fafafa; }
            h2 { text-align: center; color: #222; margin-bottom: 20px; }
            table { width: 100%%; border-collapse: collapse; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: center; font-size: 13px; }
            th { background-color: #4CAF50; color: white; }
        </style>
    </head>
    <body>
        <h2>💻 Noutbuklar ro‘yxati</h2>
        <table>
            <tr>
                <th>ID</th><th>Nomi</th><th>Brend</th><th>CPU</th><th>RAM</th>
                <th>Storage</th><th>GPU</th><th>Narx ($)</th><th>Soni</th><th>Status</th><th>Turi</th>
            </tr>
    """
    for lap in laptops:
        lap = dict(lap)  # sqlite3.Row -> dict
        html_content += f"""
            <tr>
                <td>{lap['id']}</td>
                <td>{lap['title']}</td>
                <td>{lap['brand']}</td>
                <td>{lap.get('cpu','-')}</td>
                <td>{lap.get('ram','-')}</td>
                <td>{lap.get('storage','-')}</td>
                <td>{lap.get('gpu','-')}</td>
                <td>{lap['price']}</td>
                <td>{lap['quantity']}</td>
                <td>{lap.get('status','-')}</td>
                <td>{lap.get('type','-')}</td>
            </tr>
        """

    html_content += "</table></body></html>"

    config = pdfkit.configuration(
        wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    )
    pdf_path = "laptops.pdf"
    pdfkit.from_string(html_content, pdf_path, configuration=config)
    await message.answer_document(FSInputFile(pdf_path), caption="📄 Noutbuklar ro‘yxati")
    os.remove(pdf_path)

# 🔹 Laptop qo‘shish bosqichlari (AddLaptop)
@admin_router.message(F.text == "➕ Laptop qo'shish")
async def start_add_laptop(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return await message.answer("🚫 Siz admin emassiz!")
    await state.clear()
    await state.set_state(AddLaptop.title)
    await message.answer("📥 Yangi laptop qo'shish\n1) Iltimos, laptop nomini kiriting:", reply_markup=cancel_kb)

# 🔹 FSM bosqichlari
@admin_router.message(AddLaptop.title)
async def process_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await state.set_state(AddLaptop.description)
    await message.answer("2) Tavsif kiriting (description) — bo‘sh qoldirish uchun `-`:", reply_markup=cancel_kb)

@admin_router.message(AddLaptop.description)
async def process_description(message: Message, state: FSMContext):
    description = None if message.text.strip() == "-" else message.text.strip()
    await state.update_data(description=description)
    await state.set_state(AddLaptop.brand)
    await message.answer("3) Brendni kiriting (masalan: Asus, Lenovo):", reply_markup=cancel_kb)

@admin_router.message(AddLaptop.brand)
async def process_brand(message: Message, state: FSMContext):
    await state.update_data(brand=message.text.strip())
    await state.set_state(AddLaptop.cpu)
    await message.answer("4) CPU kiriting (masalan: Intel i5, M2) — bo‘sh qoldirish uchun `-`:", reply_markup=cancel_kb)

@admin_router.message(AddLaptop.cpu)
async def process_cpu(message: Message, state: FSMContext):
    cpu = None if message.text.strip() == "-" else message.text.strip()
    await state.update_data(cpu=cpu)
    await state.set_state(AddLaptop.ram)
    await message.answer("5) RAM kiriting (masalan: 8GB):", reply_markup=cancel_kb)

@admin_router.message(AddLaptop.ram)
async def process_ram(message: Message, state: FSMContext):
    ram = None if message.text.strip() == "-" else message.text.strip()
    await state.update_data(ram=ram)
    await state.set_state(AddLaptop.storage)
    await message.answer("6) Storage kiriting (masalan: 512GB SSD):", reply_markup=cancel_kb)

@admin_router.message(AddLaptop.storage)
async def process_storage(message: Message, state: FSMContext):
    storage = None if message.text.strip() == "-" else message.text.strip()
    await state.update_data(storage=storage)
    await state.set_state(AddLaptop.gpu)
    await message.answer("7) GPU kiriting (masalan: RTX 4060) — bo‘sh qoldirish uchun `-`:", reply_markup=cancel_kb)

@admin_router.message(AddLaptop.gpu)
async def process_gpu(message: Message, state: FSMContext):
    gpu = None if message.text.strip() == "-" else message.text.strip()
    await state.update_data(gpu=gpu)
    await state.set_state(AddLaptop.price)
    await message.answer("8) Narxni butun son yoki raqam shaklida kiriting (masalan: 1200):", reply_markup=cancel_kb)

@admin_router.message(AddLaptop.price)
async def process_price(message: Message, state: FSMContext):
    try:
        price = int(float(message.text.strip()))
        if price < 0:
            raise ValueError()
    except:
        return await message.answer("❗ Narx noto‘g‘ri. Iltimos, raqam kiriting (masalan: 1200).", reply_markup=cancel_kb)
    await state.update_data(price=price)
    await state.set_state(AddLaptop.quantity)
    await message.answer("9) Soni (quantity) kiriting (default 1):", reply_markup=cancel_kb)

@admin_router.message(AddLaptop.quantity)
async def process_quantity(message: Message, state: FSMContext):
    try:
        quantity = int(message.text.strip())
        if quantity < 1:
            raise ValueError()
    except:
        return await message.answer("❗ Soni noto‘g‘ri. Iltimos, 1 yoki katta butun son kiriting.", reply_markup=cancel_kb)
    await state.update_data(quantity=quantity)
    await state.set_state(AddLaptop.image)
    await message.answer("10) Rasm yuboring (photo) yoki rasm URLini yozing. Rasm yo‘q bo‘lsa `-` yozing:", reply_markup=cancel_kb)

@admin_router.message(AddLaptop.image)
async def process_image(message: Message, state: FSMContext):
    if message.photo:
        file_id = message.photo[-1].file_id
        image = file_id
    else:
        text = (message.text or "").strip()
        image = None if text == "-" else text
    await state.update_data(image=image)
    await state.set_state(AddLaptop.status)
    await message.answer("11) Status (new / old). Masalan: new", reply_markup=cancel_kb)

@admin_router.message(AddLaptop.status)
async def process_status(message: Message, state: FSMContext):
    text = (message.text or "").strip().lower()
    if text not in ("new", "old"):
        return await message.answer("❗ Iltimos `new` yoki `old` kiriting.", reply_markup=cancel_kb)
    await state.update_data(status=text)
    await state.set_state(AddLaptop.type_)
    await message.answer("12) Turi (programming / office). Masalan: programming", reply_markup=cancel_kb)

@admin_router.message(AddLaptop.type_)
async def process_type(message: Message, state: FSMContext):
    text = (message.text or "").strip().lower()
    if text not in ("programming", "office"):
        return await message.answer("❗ Iltimos `programming` yoki `office` kiriting.", reply_markup=cancel_kb)

    await state.update_data(type_=text)
    data = await state.get_data()

    # 🔹 Rasmni yuklab olish (agar file_id bo‘lsa)
    image_path = None
    if data.get("image"):
        try:
            os.makedirs("images", exist_ok=True)
            # Agar image file_id bo'lsa (Telegram file_id formatida)
            file_id = data.get("image")
            # File_id formatini tekshirish (odatda uzun string)
            if len(file_id) > 20 and not file_id.startswith("http"):
                # Bu file_id, uni yuklab olish kerak
                file = await bot.get_file(file_id)
                local_path = f"images/{file_id}.jpg"
                await bot.download_file(file.file_path, local_path)
                image_path = local_path
            else:
                # Bu URL yoki boshqa path
                image_path = data.get("image")
        except Exception as e:
            print(f"⚠️ Rasmni saqlashda xatolik: {e}")
            image_path = data.get("image")  # Xatolik bo'lsa ham, asl qiymatni saqlash

    try:
        insert_laptop(
            title=data.get("title"),
            description=data.get("description"),
            brand=data.get("brand"),
            cpu=data.get("cpu"),
            ram=data.get("ram"),
            storage=data.get("storage"),
            gpu=data.get("gpu"),
            price=data.get("price"),
            quantity=data.get("quantity"),
            image=image_path,
            status=data.get("status"),
            type_=data.get("type_")
        )
    except Exception as e:
        await state.clear()
        return await message.answer(f"❗ Bazaga yozishda xatolik: {e}", reply_markup=admin_kb)

    await state.clear()
    await message.answer("✅ Laptop muvaffaqiyatli qo‘shildi!", reply_markup=admin_kb)

# 🔹 LeaveMessage yuborish
@admin_router.message(F.text == "✉️ Habar qoldirish")
async def leave_message(message: Message, state: FSMContext):
    await message.answer(
        "✉️ Xabaringizni yuboring. Adminlar tez orada javob beradi.",
        reply_markup=cancel_kb
    )
    await state.set_state(LeaveMessage.waiting)

@admin_router.message(LeaveMessage.waiting)
async def process_leave_message(message: Message, state: FSMContext):
    if not message.text:
        return await message.answer("❗ Iltimos, matnli xabar yuboring.", reply_markup=cancel_kb)
    
    admins = get_admins()
    for admin_id in admins:
        await bot.send_message(admin_id, f"📩 Yangi xabar:\n\n{message.text}\n\nFrom: {message.from_user.full_name}")
    await state.clear()
    await message.answer("✅ Xabaringiz yuborildi!", reply_markup=admin_kb)

# 🔹 Cancel har qanday state-da
@admin_router.message(F.text.in_(["❌ Bekor qilish", "cancel", "Cancel", "❌ Cancel"]))
async def cancel_process(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Amaliyot bekor qilindi.", reply_markup=admin_kb)



# 🔹 Admin foydalanuvchiga javob yozish
@admin_router.message(F.text == "💬 Javob berish")
async def reply_to_user_start(message: Message):
    """
    Admin "Javob berish" tugmasini bosganda ishlaydi.
    Foydalanuvchiga javob yuborish uchun, reply qilishi kerak bo‘ladi.
    """
    await message.answer(
        "❗ Javob berish uchun, foydalanuvchining xabariga reply qiling va xabaringizni yozing.",
        reply_markup=ForceReply(selective=True)
    )

@admin_router.message(F.reply_to_message)
async def reply_to_user(message: Message):
    """
    Admin foydalanuvchi xabariga reply qilsa,
    shu foydalanuvchiga javobni yuboradi.
    """
    if not is_admin(message.from_user.id):
        return await message.answer("🚫 Siz admin emassiz!")

    # Original xabar (foydalanuvchidan kelgan)
    original = message.reply_to_message
    
    if not original or not original.text:
        return await message.answer("❗ Original xabardan user ID topilmadi. Matnli xabarga reply qiling.")

    # User ID ni topish (original xabardan)
    match = re.search(r"ID: (\d+)", original.text)
    if not match:
        return await message.answer("❗ Original xabardan user ID topilmadi.")
    
    user_id = int(match.group(1))
    reply_text = message.text.strip()

    if not reply_text:
        return await message.answer("❗ Bo‘sh javob yuborib bo‘lmaydi.")

    # Javobni yuborish
    try:
        await bot.send_message(
            chat_id=user_id,
            text=f"💬 Admin javobi:\n\n{reply_text}"
        )
        # DB ga saqlash
        save_admin_message(
            admin_id=message.from_user.id,
            user_id=user_id,
            message_text=reply_text
        )
        await message.answer("✅ Javob foydalanuvchiga muvaffaqiyatli yuborildi!")
    except Exception as e:
        await message.answer(f"❗ Javob yuborilmadi: {e}")


# 🔹 Reply qilingan xabarni foydalanuvchiga yuborish
@admin_router.message(F.text == "📊 Hisobot")
async def show_report_menu(message: Message):
    """Hisobot menyusini ko'rsatish"""
    await message.answer(
        "📊 Hisobot bo'limi\n\nQuyidagilardan birini tanlang:",
        reply_markup=report_kb
    )

# 🔹 User xabarlari
@admin_router.message(F.text == "📬 User xabarlari")
async def show_user_messages(message: Message):
    users_messages = get_user_messages()
    
    if not users_messages:
        await message.answer("Hech qanday foydalanuvchi xabari yo'q 😔", reply_markup=report_kb)
        return

    html_content = """
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { font-family: DejaVu Sans, sans-serif; margin: 20px; background: #fafafa; }
            h2 { text-align: center; color: #222; margin-bottom: 20px; }
            table { width: 100%; border-collapse: collapse; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: left; font-size: 11px; }
            th { background-color: #4CAF50; color: white; }
        </style>
    </head>
    <body>
        <h2>📬 Foydalanuvchi xabarlari</h2>
        <table>
            <tr>
                <th>ID</th>
                <th>Foydalanuvchi</th>
                <th>Username</th>
                <th>Xabarlar</th>
            </tr>
    """

    for msg in users_messages:
        user_id = msg[0]
        full_name = msg[1]
        username = msg[2] or '-'
        message_text = msg[3] or '-'
        html_content += f"""
            <tr>
                <td>{user_id}</td>
                <td>{full_name}</td>
                <td>{username}</td>
                <td>{message_text.replace('\n','<br>').replace('<','&lt;').replace('>','&gt;')}</td>
            </tr>
        """

    html_content += """
        </table>
    </body>
    </html>
    """

    path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdf_path = "user_messages.pdf"
    pdfkit.from_string(html_content, pdf_path, configuration=config)

    await message.answer_document(FSInputFile(pdf_path), caption="📄 Foydalanuvchi xabarlari", reply_markup=report_kb)
    
    if os.path.exists(pdf_path):
        os.remove(pdf_path)

# 🔹 Admin xabarlari
@admin_router.message(F.text == "💬 Admin xabarlari")
async def show_admin_messages_report(message: Message):
    from database.connect import get_connect
    
    admin_messages = get_admin_messages()
    
    if not admin_messages:
        await message.answer("Hech qanday admin xabari yo'q 😔", reply_markup=report_kb)
        return

    html_content = """
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { font-family: DejaVu Sans, sans-serif; margin: 20px; background: #fafafa; }
            h2 { text-align: center; color: #222; margin-bottom: 20px; }
            table { width: 100%; border-collapse: collapse; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: left; font-size: 11px; }
            th { background-color: #2196F3; color: white; }
        </style>
    </head>
    <body>
        <h2>💬 Admin xabarlari</h2>
        <table>
            <tr>
                <th>Admin</th>
                <th>Foydalanuvchi</th>
                <th>Xabar</th>
                <th>Vaqt</th>
            </tr>
    """

    conn = get_connect()
    cursor = conn.cursor()
    
    for msg in admin_messages:
        admin_id = msg[1]  # admin_id (chat_id)
        user_id = msg[2]   # user_id (chat_id)
        message_text = msg[3]
        timestamp = msg[4]
        
        # Admin ismini olish
        cursor.execute("SELECT name FROM users WHERE chat_id = ?", (admin_id,))
        admin_result = cursor.fetchone()
        admin_name = admin_result[0] if admin_result else f"Admin (ID: {admin_id})"
        
        # Foydalanuvchi ismini olish
        cursor.execute("SELECT name FROM users WHERE chat_id = ?", (user_id,))
        user_result = cursor.fetchone()
        user_name = user_result[0] if user_result else f"User (ID: {user_id})"
        
        html_content += f"""
            <tr>
                <td>{admin_name}</td>
                <td>{user_name}</td>
                <td>{message_text.replace('\n','<br>').replace('<','&lt;').replace('>','&gt;')}</td>
                <td>{timestamp}</td>
            </tr>
        """
    
    conn.close()

    html_content += """
        </table>
    </body>
    </html>
    """

    path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdf_path = "admin_messages_report.pdf"
    pdfkit.from_string(html_content, pdf_path, configuration=config)

    await message.answer_document(FSInputFile(pdf_path), caption="📄 Admin xabarlari", reply_markup=report_kb)
    
    if os.path.exists(pdf_path):
        os.remove(pdf_path)

# 🔹 Ortga qaytish
@admin_router.message(F.text == "🔙 Ortga qaytish")
async def back_to_admin_menu(message: Message):
    await message.answer("Admin bo'limiga qaytdingiz", reply_markup=admin_kb)


# 🔹 Admin ID kiritadi
@admin_router.message(F.text == "✉️ Habar yuborish (ID orqali)")
async def ask_user_id(message: Message, state: FSMContext):
    await state.set_state(SendToUser.waiting_for_user_id)
    await message.answer("❗ Iltimos, foydalanuvchi ID sini kiriting:", reply_markup=cancel_kb)

# 🔹 ID qabul qilinadi
@admin_router.message(SendToUser.waiting_for_user_id)
async def process_user_id(message: Message, state: FSMContext):
    try:
        user_id = int(message.text.strip())
    except ValueError:
        return await message.answer("❌ ID noto‘g‘ri. Iltimos, faqat raqam kiriting.")

    await state.update_data(user_id=user_id)
    await state.set_state(SendToUser.waiting_for_message)
    await message.answer("✏️ Endi xabaringizni yozing:", reply_markup=cancel_kb)

# 🔹 Xabar qabul qilinadi va foydalanuvchiga yuboriladi
@admin_router.message(SendToUser.waiting_for_message)
async def send_message_to_user(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    text = message.text.strip()

    if not text:
        return await message.answer("❌ Bo‘sh xabar yuborib bo‘lmaydi.")

    try:
        await bot.send_message(user_id, f"📩 Admindan xabar:\n\n{text}")
        # DB ga saqlash
        save_admin_message(
            admin_id=message.from_user.id,
            user_id=user_id,
            message_text=text
        )
        await message.answer(f"✅ Xabar {user_id} ID li foydalanuvchiga yuborildi!")
    except Exception as e:
        await message.answer(f"❌ Xabar yuborilmadi: {e}")

    await state.clear()


@admin_router.message(F.text == "📊 Admin xabarlar")
async def show_admin_messages(message: Message):
    messages = get_admin_messages()
    if not messages:
        return await message.answer("Hech qanday admin xabarlari yo‘q 😔")

    html_content = """
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { font-family: DejaVu Sans, sans-serif; margin: 20px; background: #fafafa; }
            h2 { text-align: center; color: #222; margin-bottom: 20px; }
            table { width: 100%; border-collapse: collapse; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
            th { background-color: #4CAF50; color: white; }
        </style>
    </head>
    <body>
        <h2>📬 Admin xabarlari</h2>
        <table>
            <tr>
                <th>ID</th>
                <th>Admin Chat ID</th>
                <th>User Chat ID</th>
                <th>Xabar</th>
                <th>Vaqt</th>
            </tr>
    """
    for msg in messages:
        html_content += f"""
            <tr>
                <td>{msg[0]}</td>
                <td>{msg[1]}</td>
                <td>{msg[2]}</td>
                <td>{msg[3].replace('\n','<br>')}</td>
                <td>{msg[4]}</td>
            </tr>
        """

    html_content += "</table></body></html>"

    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
    pdf_path = "admin_messages.pdf"
    pdfkit.from_string(html_content, pdf_path, configuration=config)

    await message.answer_document(FSInputFile(pdf_path), caption="📄 Admin xabarlari")
    if os.path.exists(pdf_path):
        os.remove(pdf_path)

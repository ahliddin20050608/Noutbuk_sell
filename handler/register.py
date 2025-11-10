from aiogram import Router, F
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from buttons import START_TEXT, NAME_TEXT, PHONE_TEXT, SUCCESS_REG_TEXT, NEXT_MENU_TEXT
from buttons import register_kb, phone_kb, option_kb
from filter import validate_fullname, validate_phone
from database import is_registered_by_chat_id, save_user
from states import Register

register_router = Router()


@register_router.message(CommandStart())
async def start_bot(message: Message):
    registreted = is_registered_by_chat_id(message.from_user.id)
    image_path = "images/main_image2.jpg"
    
    if registreted:
        image_path = "images/a.jpg"
        await message.answer_photo(
            photo=FSInputFile(image_path), 
            caption=NEXT_MENU_TEXT, 
            reply_markup=option_kb
        )
    else:
        await message.answer_photo(
            photo=FSInputFile(image_path), 
            caption=START_TEXT, 
            reply_markup=register_kb
        )


@register_router.message(F.text == "Ro'yxatdan o'tish")
async def start_register(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer(text=NAME_TEXT, reply_markup=ReplyKeyboardRemove())


@register_router.message(Register.name)
async def get_name(message: Message, state: FSMContext):
    if validate_fullname(message.text):
        await state.update_data(name=message.text)
        await state.set_state(Register.phone)
        await message.answer(PHONE_TEXT, reply_markup=phone_kb)
    else:
        await message.answer("Iltimos, to'g'ri formatda kiriting.")


@register_router.message(Register.phone)
async def get_phone(message: Message, state: FSMContext):
    phone = None

    # Agar foydalanuvchi kontakt yuborsa
    if message.contact:
        phone = message.contact.phone_number
    # Agar foydalanuvchi matn shaklida yuborsa
    elif validate_phone(message.text):
        phone = message.text
    else:
        await message.answer("Iltimos, to‘g‘ri telefon raqam kiriting.")
        return  # xatolik bo‘lsa funksiyani to‘xtatish

    # Agar telefon mavjud bo‘lsa, saqlash
    if phone:
        data = await state.get_data()
        fullname = data.get("name")
        save_user(
            chat_id=message.from_user.id,
            name=fullname, 
            phone=phone,
            username=message.from_user.username
        )

        # Muvaffaqiyatli xabar va keyingi menu
        success_msg = await message.answer(text=SUCCESS_REG_TEXT, reply_markup=None)
        await success_msg.delete()  # vaqtincha xabarni o‘chirish

        image_path = "images/a.jpg"
        await message.answer_photo(
            photo=FSInputFile(image_path),
            caption=NEXT_MENU_TEXT,
            reply_markup=option_kb
        )

        await state.clear()  # FSMni tozalash

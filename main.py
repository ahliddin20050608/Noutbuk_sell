from aiogram import Bot, Dispatcher, F
from environs import Env
from handler import register_router, user_router, admin_router
from database import create_tables, add_messages_column
import logging
import asyncio


env = Env()
env.read_env()

TOKEN = env.str("TOKEN")
dp = Dispatcher()


async def main():
    # 🔹 Bazani ishga tushirish
    create_tables()
    add_messages_column()

    bot = Bot(token=TOKEN)

    dp.include_router(register_router)
    dp.include_router(user_router)
    dp.include_router(admin_router)
    
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except KeyboardInterrupt:
        logging.info("Bot to'xtatildi (Ctrl+C)")
    except Exception as e:
        logging.error(f"Xatolik yuz berdi: {e}")
        raise
    finally:
        await bot.session.close()



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("BOT ISHGA TUSHDI...")
    asyncio.run(main())
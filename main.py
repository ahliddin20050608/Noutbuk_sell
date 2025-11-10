from aiogram import Bot, Dispatcher, F
from environs import Env
from handler import register_router, user_router, admin_router
import logging
import asyncio


env = Env()
env.read_env()

TOKEN = env.str("TOKEN")
dp = Dispatcher()


async def main():

    bot = Bot(token=TOKEN)

    dp.include_router(register_router)
    dp.include_router(user_router)
    dp.include_router(admin_router)
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("BOT ISHGA TUSHDI...")
    asyncio.run(main())
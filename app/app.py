import asyncio

from extensions import bot, dp
from views.main import router as main_router


async def on_startup():
    print("Бот запущен")


async def main():
    dp.startup.register(on_startup)
    dp.include_router(main_router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

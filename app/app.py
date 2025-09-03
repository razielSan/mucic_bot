import asyncio

from extensions import bot, dp
from views.main import router as main_router
from views.add_music import router as add_music_router
from views.music_archive import router as music_archive_router
from views.search import router as search_router
from views.add_collection_of_songs import router as add_collection_of_songs_router
from views.collection_songs import router as collection_songs_router
from views.list_executor import router as list_executor_router
from views.add_music_network.main import router as main_add_music_network_router
from views.add_music_network.search_music_archive import (
    router as search_music_archive_router,
)
from views.add_music_network.search_by_hitmotop import router as search_hitmotop_router
from views.add_music_network.music_archive_executor import (
    router as music_archive_executor_router,
)
from views.admin import router as admin_router
from config import settings


async def on_startup():
    """Срабатывает при старте бота."""
    print("Бот запущен")


async def main():
    """Запускает бота."""
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(settings.bot_command)
    # await bot.delete_my_commands()

    dp.startup.register(on_startup)
    dp.include_router(search_music_archive_router)
    dp.include_router(search_hitmotop_router)
    dp.include_router(add_music_router)
    dp.include_router(collection_songs_router)
    dp.include_router(search_router)
    dp.include_router(music_archive_router)
    dp.include_router(add_collection_of_songs_router)

    dp.include_router(music_archive_executor_router)
    dp.include_router(main_add_music_network_router)
    dp.include_router(list_executor_router)
    dp.include_router(main_router)
    dp.include_router(admin_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

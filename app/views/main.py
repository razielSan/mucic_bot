from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from extensions import bot
from keyboards.reply import get_music_menu_button
from repository.user import UserSQLAlchemyRepository
from repository.album import AlbumSQLAlchemyRepository
from repository.executor import ExecutorSQLAlchemyRepository

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    chat_id = message.chat.id
    message_id = message.message_id
    print("Ok")
    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    await message.answer(
        text="Музыкальный архив",
        reply_markup=get_music_menu_button(),
    )

    # print(os.path.dirname(os.path.abspath(__name__)))
    # path_dir = os.path.dirname(os.path.abspath(__name__))
    # path = os.path.join(
    #     path_dir, "media"
    # )
    # audio_file = FSInputFile(
    #     path=os.path.join(path, "name.mp3"),
    #     filename="Мечты не сбываются"
    # )
    # audio_file = (
    #     "CQACAgIAAxkBAAIBEWh0wDrr21Cmxclmg5tLRbnX0yNzAAK_fAAC5muoS3yrtyD6An64NgQ"
    # )
    # await message.answer_audio(audio=audio_file, caption="мечты не сбываются")
    # await message.answer_audio(audio_file)


@router.message()
async def start2(message: Message):
    user = UserSQLAlchemyRepository().get_user_by_id(telegram=message.chat.id)
    executor = ExecutorSQLAlchemyRepository().get_executor_by_name(
        user_id=user.id, name="Ария", country="Неизвестно"
    )
    alubum = AlbumSQLAlchemyRepository().delete_album(
        title="Среда", year=2023, executor_id=executor.id
    )
    if alubum:
        result = ExecutorSQLAlchemyRepository().delete_executor(
            name="Ария", user_id=user.id, country="Неизвестно"
        )
        if result:
            await message.answer(f"{result}")
        else:
            await message.answer("executor none")
    else:
        await message.answer("album none")
    


# @router.message(F.content_type == "audio")
# async def temp(message: Message):
#     global count
#     list_audio.append(message.audio.file_id)
#     print(list_audio)
#     print(message.audio.file_id)
#     print(message.audio.file_name)
#     count += 1
#     if count == 10:
#         await message.answer("ok")

# @router.message(F.text == "go")
# async def temp(message: Message):
#     for file_id in list_audio:
#         await message.answer_audio(audio=file_id)

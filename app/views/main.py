from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from extensions import bot
from keyboards.reply import get_music_menu_button

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

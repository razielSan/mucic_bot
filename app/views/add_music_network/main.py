from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter

from keyboards.reply import get_button_for_add_music_network


router = Router(name=__name__)


@router.message(StateFilter(None), F.text == "💾 Искать музыку в интернете 💾")
async def main_add_music_netowrk(message: Message):
    await message.answer(
        text="Меню поиска",
        reply_markup=get_button_for_add_music_network(),
    )

@router.message(StateFilter(None), F.text == "Список исполнителей музыкального хранилища")
async def main_add_music_netowrk(message: Message):
    await message.answer(
        text="Меню поиска",
        reply_markup=get_button_for_add_music_network(),
    )

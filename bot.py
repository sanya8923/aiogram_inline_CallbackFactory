import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command, Message
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest

from typing import Optional
from contextlib import suppress


logging.basicConfig(level=logging.INFO)
bot = Bot(token='6204362749:AAEK2ymI8Jac_1uZYrZbL7gBoBu4yl7i37Q')
dp = Dispatcher()
user_data = {}


class NumbersCallBackFactory(CallbackData, prefix='fabnum'):
    action: str
    value: Optional[int]


# КЛАВИАТУРА
def get_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text='-2', callback_data=NumbersCallBackFactory(action='change', value=-2))
    builder.button(text='-1', callback_data=NumbersCallBackFactory(action='change', value=-1))
    builder.button(text='1', callback_data=NumbersCallBackFactory(action='change', value=1))
    builder.button(text='2', callback_data=NumbersCallBackFactory(action='change', value=2))
    builder.button(text='Confirm', callback_data=NumbersCallBackFactory(action='finish'))

    builder.adjust(4)
    return builder.as_markup()


async def update_num_text(message: Message, new_value: int):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f'Write number: {new_value}',
            reply_markup=get_keyboard()
        )


@dp.message(Command('start'))
async def cmd_start_bot(message: Message):
    user_data[message.from_user.id] = 0
    await message.answer('Write number: 0',
                         reply_markup=get_keyboard()
                         )







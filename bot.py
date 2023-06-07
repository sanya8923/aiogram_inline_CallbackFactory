import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command, Message
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from typing import Optional


logging.basicConfig(level=logging.INFO)
bot = Bot(token='6204362749:AAEK2ymI8Jac_1uZYrZbL7gBoBu4yl7i37Q')
dp = Dispatcher()


class NumbersCallBackFactory(CallbackData, prefix='fabnum'):
    action: str
    value: Optional[int]


@dp.message(Command('start'))
async def cmd_start_bot(message: Message):
    pass


def get_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text='-2', callback_data=NumbersCallBackFactory(action='change', value=-2))
    builder.button(text='-1', callback_data=NumbersCallBackFactory(action='change', value=-1))
    builder.button(text='1', callback_data=NumbersCallBackFactory(action='change', value=1))
    builder.button(text='2', callback_data=NumbersCallBackFactory(action='change', value=2))
    builder.button(text='Confirm', callback_data=NumbersCallBackFactory(action='finish'))

    builder.adjust(4)
    return builder.as_markup()







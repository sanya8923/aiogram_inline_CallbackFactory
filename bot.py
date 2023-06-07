import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command, Message
from aiogram.filters.callback_data import CallbackData

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



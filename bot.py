import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command, Message
from aiogram.filters.callback_data import CallbackData, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest

from typing import Optional
from contextlib import suppress
from magic_filter import F


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


#  ТЕКСТ "Write number:" НАД КЛАВИАТУРОЙ
async def update_num_text(message: Message, new_value: int):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f'Write number: {new_value}',
            reply_markup=get_keyboard()
        )


# ЗАПУСК КЛАВИАТУРЫ
@dp.message(Command('start'))
async def cmd_start_bot(message: Message):
    user_data[message.from_user.id] = 0
    await message.answer('Write number: 0',
                         reply_markup=get_keyboard()
                         )


#  ОБРАБОТКА КАЛБЕКОВ (одной функцией)
@dp.callback_query(NumbersCallBackFactory.filter())
async def callback_num_change(
        callback: CallbackQuery,
        callback_data: NumbersCallBackFactory
        ):
    # текущее значение
    user_value = user_data.get(callback.from_user.id, 0)

    # Если число нужно изменить
    if callback_data.action == 'change':
        user_data[callback.from_user.id] = user_value + callback_data.value
        await update_num_text(callback.message, user_value + callback_data.value)
    else:
        await callback.message.edit_text(f'Total: {user_value}')
    await callback.answer()


#  ОБРАБОТКА КАЛБЕКОВ (двумя функциями)
# Нажатие на одну из кнопок: -2, -1, +1, +2
@dp.callback_query(NumbersCallBackFactory.filter(F.action == 'change'))
async def callback_num_change(
        callback: CallbackQuery,
        callback_data: NumbersCallBackFactory
        ):
    # текущее значение
    user_value = user_data.get(callback.from_user.id, 0)

    user_data[callback.from_user.id] = user_value + callback_data.value
    await update_num_text(callback.message, user_value + callback_data.value)
    await callback.answer()


# Нажатие на кнопку "confirm"
@dp.callback_query(NumbersCallBackFactory.filter(F.action == 'finish'))
async def callback_num_finish(
        callback: CallbackQuery,
        callback_data: NumbersCallBackFactory
        ):
    user_value = user_data.get(callback.from_user.id, 0)

    await callback.message.edit_text(f'Total: {user_value}')
    await callback.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())



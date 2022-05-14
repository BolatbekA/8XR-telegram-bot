# import os
# from dotenv import load_dotenv
# import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.dispatcher.filters.state import State, StatesGroup

# from main import dp


async def cmd_start(message: types.Message):
    text = (
        f'Hi, {message.from_user.first_name}.\nWe are a startup from London. '
        'Build and deliver your 3Dimmersive art online to VR/AR devices. '
        'Trade as NFT.'
            )
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Dive in extended reality', 'About us']
    keyboard.add(*buttons)
    await message.answer(text, reply_markup=keyboard)


async def go_to_rooms(message: types.Message):
    # это надо переделать, надо сразу попадать в другую функцию room_start
    await message.reply(
        'тест, далее в проекты',
        reply_markup=types.ReplyKeyboardRemove()
        )


async def about_us(message: types.Message):
    await message.reply('тест, далее инфа о нас')


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        'Action canceled',
        reply_markup=types.ReplyKeyboardRemove()
        )


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start', state='*')
    dp.register_message_handler(
        go_to_rooms,
        Text(equals='Dive in extended reality', ignore_case=True),
        state='*'
        )
    dp.register_message_handler(
        about_us,
        Text(equals='About us', ignore_case=True),
        state='*')
    dp.register_message_handler(
        cmd_cancel,
        Text(equals='Action canceled', ignore_case=True),
        commands='cancel',
        state='*'
        )

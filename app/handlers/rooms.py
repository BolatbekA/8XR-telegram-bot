from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
# from xrbot import dp

available_room_names = {
    'Blue space bar': 'https://8xr.io/s/spacebar1/view',
    'Interstellar gasoline station': 'https://8xr.io/s/petrolstation/view',
    'EdelExtra art gallery': 'https://8xr.io/s/digitalairstart/view',
    'Sea & Sky': 'https://8xr.io/s/searoom/view',
    'Bullwark art gallery': 'https://8xr.io/s/gallerybullwark/view',
    'Purple Room': 'https://8xr.io/s/relaxroom/view',
    'Boutique Room': 'https://8xr.io/s/boutique/view',
    'Back to the main menu': '',
}


class ChooseRoom(StatesGroup):
    waiting_for_room_name = State()


async def room_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_room_names.keys():
        keyboard.add(name)
    await message.answer('Choose extended reality:', reply_markup=keyboard)
    await ChooseRoom.waiting_for_room_name.set()


async def room_chosen(message: types.Message, state: FSMContext):
    if message.text not in available_room_names.keys():
        await message.answer('Pease choose a room using the keyboard below.')
        return
    user_data = (message.text, available_room_names[message.text])
    await message.answer(user_data)


def register_handlers_room(dp: Dispatcher):
    dp.register_message_handler(room_start, commands='rooms', state='*')
    dp.register_message_handler(
        room_chosen,
        state=ChooseRoom.waiting_for_room_name
        )

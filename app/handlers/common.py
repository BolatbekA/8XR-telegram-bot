from aiogram import Dispatcher, types, asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import aiogram.utils.markdown as fmt


available_room_names = {
    'Blue space bar': (
        'https://8xr.io/s/spacebar1/view',
        'Beautiful orbital space bar. Perfect place to hang out with 3-4 '
        'of your friends',
        ('https://8xr.io/images/'
         'tild3736-6532-4065-b132-363662386635__blue-bar.png')
    ),
    'Interstellar gasoline station': (
        'https://8xr.io/s/petrolstation/view',
        'Transcendental sci-fi scene to relax and talk with your friends',
        ('https://8xr.io/images/'
         'tild6533-6433-4462-a334-663031663133__space-gasolin-statio.png')
    ),
    'EdelExtra art gallery': (
        'https://8xr.io/s/digitalairstart/view',
        'Art gallery located at Nuremberg, Germany which produced a great '
        'number of artworks in XR theme',
        ('https://8xr.io/images/'
         'tild3434-6138-4432-b235-356532616465__edel-extra.png')
    ),
    'Sea & Sky': (
        'https://8xr.io/s/searoom/view',
        'Endless horizon scene designed for meditative talks with a few '
        'closest friends',
        ('https://8xr.io/images/'
         'tild3230-3964-4530-b664-306166353464__seasky.png')
    ),
    'Bullwark art gallery': (
        'https://8xr.io/s/gallerybullwark/view',
        'The nice and spacious art gallery that has been made by BullWark '
        'marketing agency',
        ('https://8xr.io/images/'
         'tild3539-3934-4930-b761-313132343837__bullwark.png')
    ),
    'Purple Room': (
        'https://8xr.io/s/relaxroom/view',
        'Purple cubic room designed to chill and walk around ',
        ('https://8xr.io/images/'
         'tild3438-6631-4233-b437-366233303063__purpleroom.png')
    ),
    'Boutique Room': (
        'https://8xr.io/s/boutique/view',
        'The colorful boutique place where you could place 5 or 6 of your '
        'digital assets',
        ('https://8xr.io/images/'
         'tild3662-6361-4161-b932-613633356461__boutique.png')
    ),
    'Back to the main menu': '',
}


class ChooseRoom(StatesGroup):
    waiting_for_room_name = State()


async def cmd_start(message: types.Message):
    '''Welcomes the user and offers a choice of 2 buttons'''
    text = (
        f'Hi, {message.from_user.first_name}.\nWe are a startup from London. '
        'Build and deliver your 3Dimmersive art online to VR/AR devices. '
        'Trade as NFT.'
            )
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Dive in extended reality', 'Contact us']
    keyboard.add(*buttons)
    await message.answer(text, reply_markup=keyboard)
    # await asyncio.sleep(0.5)
    await message.answer('Choose the next action using the keyboard below.')


async def about_us(message: types.Message):
    '''Displays information about the project'''
    buttons = [
        types.InlineKeyboardButton(
            text='Web site',
            url='https://8xr.io/'
            ),
        types.InlineKeyboardButton(
            text='LinkedIn',
            url='https://www.linkedin.com/company/8xr/'
            ),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    text = (
        'We are constantly looking for talented artists '
        'and beautiful collections that will fit our XR ecosystem.\n'
        'Apply if you have a project and want to work together.'
            )
    await message.answer(text, reply_markup=keyboard)


async def go_to_rooms(message: types.Message):
    '''Creates buttons based on dictionary keys and waits for input'''
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    for name in available_room_names.keys():
        buttons.append(name)
    keyboard.add(*buttons)
    await message.answer(
        'Choose extended reality using the keyboard below.',
        reply_markup=keyboard
        )
    await ChooseRoom.waiting_for_room_name.set()


async def room_chosen(message: types.Message, state: FSMContext):
    '''Returns to the main menu or displays information about the space'''
    if message.text not in list(available_room_names.keys()):
        await message.answer('Please, choose extended reality '
                             'using the keyboard below.')
        return
    user_data = (message.text, available_room_names[message.text])
    if user_data[0] == 'Back to the main menu':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ['Dive in extended reality', 'Contact us']
        keyboard.add(*buttons)
        await message.answer(
            'You are back in the main menu.',
            reply_markup=keyboard
            )
    else:
        buttons = [
            types.InlineKeyboardButton(text='Dive in', url=user_data[1][0]),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        await message.answer(
            fmt.text(
               fmt.text(fmt.hbold(user_data[0])),
               fmt.text(fmt.hitalic(user_data[1][1])),
               fmt.hide_link(user_data[1][2]),
               sep="\n"
                ), parse_mode='HTML',
            reply_markup=keyboard
        )


def register_handlers_common(dp: Dispatcher):
    '''Function for registering higher-level handlers'''
    dp.register_message_handler(cmd_start, commands='start', state='*')
    dp.register_message_handler(go_to_rooms, commands='rooms', state='*')
    dp.register_message_handler(
        go_to_rooms,
        Text(equals='Dive in extended reality', ignore_case=True),
        state='*'
        )
    dp.register_message_handler(
        about_us,
        Text(equals='Contact us', ignore_case=True),
        state='*')
    dp.register_message_handler(
        room_chosen,
        state=ChooseRoom.waiting_for_room_name
        )

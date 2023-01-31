import logging  
import aiogram.utils.markdown as md
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN_API, CONTACTS_TEXT, INFO_TEXT, START_TEXT, HELP_COMMAND
from keyboards import get_kb_start, get_kb_contacts
from form import Order

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN_API)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    print("Бот Работает")

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=START_TEXT,
                           reply_markup=get_kb_start())



@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=INFO_TEXT,
                           parse_mode="HTML",
                           reply_markup=get_kb_start())
    await message.delete()



@dp.message_handler(commands=['contacts'])
async def contacts(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=CONTACTS_TEXT,
                           parse_mode="HTML",
                           reply_markup=get_kb_contacts())
    await message.delete()

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=HELP_COMMAND,
                           parse_mode="HTML",
                           reply_markup=get_kb_start())
    await message.delete()



@dp.message_handler(commands='order')
async def cmd_start(message: types.Message):
    await Order.fullname.set()
    await message.reply("Hi there! What's your name?")


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Order.fullname)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fullname'] = message.text
    await Order.next()
    markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
    )
    await message.reply("Phone number?", reply_markup=markup_request)


@dp.message_handler(content_types=types.ContentType.CONTACT, state=Order.phone_number)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.contact.phone_number
        print(message.contact['phone_number'])
        markup = types.ReplyKeyboardRemove()
        await bot.send_message(
            message.chat.id,
            'Успешно',
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )
        await bot.send_message('710921551', text=md.text(
                md.text('Hi! Nice to meet you,', md.bold(data['fullname'])),
                md.text('phonenumber:', md.code(data['phone_number'])),
                sep='\n'))
        await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
from aiogram.dispatcher.filters.state import StatesGroup, State

class Order(StatesGroup):
    fullname = State() 
    phone_number = State()
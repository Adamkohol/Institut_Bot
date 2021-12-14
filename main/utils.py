from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class BotStates(StatesGroup):
    Menu = State()
    Dialog = State()
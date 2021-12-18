import logging
import asyncio
import emoji
from emoji import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import BotBlocked
from aiogram import Bot, executor, types
from aiogram.dispatcher import Dispatcher
from os import getenv
from sys import exit
from utils import BotStates
import json
import nltk
import numpy
import random
import bot as nav
import tensorflow
import tflearn
import pickle
import tg_analytic
from nltk.stem.lancaster import LancasterStemmer
from Responses import chat

password = getenv("PASS_TOKEN_KEY")
bot_token = getenv("BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

AUTHORIZATION_STATE = False
print("PROGRAM START")


# пример обработчика ошибки
# ОБЩИЙ ОБРАБОТЧИК ОБЩИЙ ОБРАБОТЧИК ОБЩИЙ ОБРАБОТЧИК ОБЩИЙ ОБРАБОТЧИК ОБЩИЙ ОБРАБОТЧИК ОБЩИЙ ОБРАБОТЧИК ОБЩИЙ ОБРАБОТЧИК



# ОБЩИЙ ОБРАБОТЧИК ОБЩИЙ ОБРАБОТЧИК ОБЩИЙ ОБРАБОТЧИК ОБЩИЙ ОБРАБОТЧИК ОБЩИЙ ОБРАБОТЧИК ОБЩИЙ ОБРАБОТЧИК ОБЩИЙ ОБРАБОТЧИК

# EXCEPTION FOR BLOCK---------------------------------------------------------------------------------------------------
@dp.message_handler(commands="block")
async def cmd_block(message: types.Message):
    await asyncio.sleep(10.0)  # Здоровый сон на 10 секунд
    await message.answer("Вы заблокированы")


@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    # Update: объект события от Telegram. Exception: объект исключения
    # Здесь можно как-то обработать блокировку, например, удалить пользователя из БД
    print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")

    # Такой хэндлер должен всегда возвращать True,
    # если дальнейшая обработка не требуется.
    return True


# EXCEPTION FOR BLOCK---------------------------------------------------------------------------------------------------

'''def is_emoji(s):
    count = 0
    for em in UNICODE_EMOJI_ENGLISH:
        count += s.count(em)
        if count > 1:
            return False
        return bool(count)
'''


def text_has_emoji(text):
    for character in text:
        if character in emoji.UNICODE_EMOJI_ENGLISH:
            return True
    return False


# ПРОВЕРКА ПАРОЛЯ ПРОВЕРКА ПАРОЛЯ ПРОВЕРКА ПАРОЛЯ ПРОВЕРКА ПАРОЛЯ ПРОВЕРКА ПАРОЛЯ ПРОВЕРКА ПАРОЛЯ ПРОВЕРКА ПАРОЛЯ ПРОВЕР
@dp.message_handler(commands="pcfat")  # проверка
async def CHECKPASS(message: types.Message):  # await теперь обязателен
    await message.answer("Введите пароль")
    if message.text != "Отмена":
        bot.register_next_step_handler(message, check_password)
    else:
        pass


async def check_password(message: types.Message):
    password_to_check = message.text

    if password_to_check == password:
        await message.answer("right")
        AUTHORIZATION_STATE = True

    elif message.text == "Отмена":
        pass
    else:
        await message.answer("wrong")
        AUTHORIZATION_STATE = False


@dp.message_handler(commands="logout")
async def OUT(message: types.Message):  # await теперь обязателен
    await message.answer("Вы хотите выйти?")
    if message.text != "Нет":
        pass
    elif message.text == "Да":
        AUTHORIZATION_STATE = False


# ПРОВЕРКА ПАРОЛЯ ПРОВЕРКА ПАРОЛЯ ПРОВЕРКА ПАРОЛЯ ПРОВЕРКА ПАРОЛЯ ПРОВЕРКА ПАРОЛЯ ПРОВЕРКА ПАРОЛЯ ПРОВЕРКА ПАРОЛЯ ПРОВЕР
# СТАТУС СТУДЕНТ СТАТУС СТУДЕНТ СТАТУС СТУДЕНТ СТАТУС СТУДЕНТ СТАТУС СТУДЕНТ СТАТУС СТУДЕНТ СТАТУС СТУДЕНТ СТАТУС СТУДЕН
if AUTHORIZATION_STATE == False:
    @dp.message_handler(commands="start")  # новый обработчик
    async def MENU(message: types.Message):  # await теперь обязателен
        if AUTHORIZATION_STATE is False:
            await message.answer("\t Здравствуй!🤖 Бот для учебы, вот список команд:"
                                 " \n /start - начало работы \n /help - 🛠 помощь \n /faq - ⁉ часто задаваемые вопросы \n"
                                 " /educationmaterial - 📚️ учебный материал \n"
                                 " /testcheck - 🧩 тесты для самоподготовки\n", reply_markup=nav.mainMenu)
        else:
            await message.answer("\t Здравствуй!🤖 Бот для учебы, вот список команд:"
                                 " \n /start - начало работы \n /help - 🛠 помощь \n /faq - ⁉ часто задаваемые вопросы \n"
                                 " /remindlesson - 🔔 напомнить о занятии \n /reminddeadline - 🔔 напомнить о дедлайне \n "
                                 "/educationresult - 🎓 успеваемость\n"
                                 " /educationmaterial - 📚️ учебный материал \n"
                                 " /testcheck - 🧩 тесты для самоподготовки\n"
                                 " /congratsstudent -  🏆 топ учащихся\n", reply_markup=nav.mainMenu)


    # Команды -------------------------------------------------------------------------------------------------------------

    # Команды -------------------------------------------------------------------------------------------------------------
    # Output функции ------------------------------------------------------------------------------------------------------
    # чтобы работало и меню и команды
    async def helpOut(message):
        await message.reply("help  is working")


    async def faqOut(message):
        await message.reply("faq is working")


    async def remlesOut(message):
        await message.reply("remind lesson is working")


    async def remdeadOut(message):
        await message.reply("remind deadline is working")


    async def testcheckOut(message):
        await message.reply("test is working:")


    async def eduresOut(message):
        await message.reply("education result is working")


    async def edumatOut(message):
        await message.reply("education material is working")


    async def congstuOut(message):
        await message.reply("congrats is working")


    # Output функции ---------------------------------------------------------------------------------------------------
    # Кнопки -----------------------------------------------------------------------------------------------------------
    async def StudBUTTON(message: types.Message):
        if AUTHORIZATION_STATE is False:
            if message.text == '🛠 Помощь':  # кнопочки, текст внутри message  не трогать
                await message.reply("help  is working")
            elif message.text == '⁉ Частые вопросы':
                await faqOut(message)
            elif message.text == '🧩 Тесты':
                await testcheckOut(message)
            elif message.text == '📚️ Учебный материал':
                await edumatOut(message)
            elif message.text == 'Другое ➡':
                await message.reply("Другое ➡", reply_markup=nav.otherMenu)
            elif message.text == '⬅ Главное меню':
                await message.reply("⬅ Главное меню", reply_markup=nav.mainMenu)
        else:
            if message.text == '🛠 Помощь':  # кнопочки, текст внутри message  не трогать
                await message.reply("help  is working")
            elif message.text == '⁉ Частые вопросы':
                await faqOut(message)
            elif message.text == '🧩 Тесты':
                await testcheckOut(message)
            elif message.text == '🔔 Напомнить о занятии':
                await remlesOut(message)
            elif message.text == '🔔 Напомнить о дедлайне':
                await remdeadOut(message)
            elif message.text == '🎓 Успеваемость':
                await eduresOut(message)
            elif message.text == '📚️ Учебный материал':
                await edumatOut(message)
            elif message.text == '🏆 Топ':
                await congstuOut(message)
            elif message.text == 'Другое ➡':
                await message.reply("Другое ➡", reply_markup=nav.otherMenu)
            elif message.text == '⬅ Главное меню':
                await message.reply("⬅ Главное меню", reply_markup=nav.mainMenu)


    # СТАТУС СТУДЕНТ СТАТУС СТУДЕНТ СТАТУС СТУДЕНТ СТАТУС СТУДЕНТ СТАТУС СТУДЕНТ СТАТУС СТУДЕНТ СТАТУС СТУДЕНТ СТАТУС СТУДЕН

    # СТАТУС ПРЕПОДАВАТЕЛЬ СТАТУС ПРЕПОДАВАТЕЛЬ СТАТУС ПРЕПОДАВАТЕЛЬ СТАТУС ПРЕПОДАВАТЕЛЬ СТАТУС ПРЕПОДАВАТЕЛЬ СТАТУС ПРЕПОД
    # if AUTHORIZATION_STATE == True:
    # @dp.message_handler(commands="start")  # новый обработчик
    # async def MENU(message: types.Message):  # await теперь обязателен

    # await message.answer("\t Здравствуй!🤖 Бот для учебы, вот список команд:"
    #                    " \n /start - начало работы \n /help - 🛠 помощь \n /faq - ⁉ часто задаваемые вопросы \n"
    #                   " /remindlesson - 🔔 напомнить о занятии \n /reminddeadline - 🔔 напомнить о дедлайне \n "
    #                  "/educationresult - 🎓 успеваемость\n"
    #                 " /educationmaterial - 📚️ учебный материал \n"
    #                " /testcheck - 🧩 тесты для самоподготовки\n"
    #               " /congratsstudent -  🏆 топ учащихся\n", reply_markup=nav.mainMenu)

    # Команды -------------------------------------------------------------------------------------------------------------
    @dp.message_handler(commands="help")  # напомнить о занятии
    async def HELP(message: types.Message):  # await теперь обязателен
        await helpOut(message)


    @dp.message_handler(commands="remindlesson")  # напомнить о занятии
    async def FAQ(message: types.Message):  # await теперь обязателен
        await faqOut(message)


    @dp.message_handler(commands="remindlesson")  # напомнить о занятии
    async def REMINDLES(message: types.Message):  # await теперь обязателен
        await remlesOut(message)


    @dp.message_handler(commands="reminddeadline")  # напомнить о дедлайне
    async def REMINDED(message: types.Message):  # await теперь обязателен
        await remdeadOut(message)


    @dp.message_handler(commands="testcheck")  # тесты для самопроверки
    async def TESTCHECK(message: types.Message):  # await тeперь обязателен
        await testcheckOut(message)


    @dp.message_handler(commands="educationresult")  # об успеваемости
    async def EDRESUL(message: types.Message):  # await тeперь обязателен
        await eduresOut(message)


    @dp.message_handler(commands="educationmaterial")  # учебный материал
    async def EDMAT(message: types.Message):  # await тeперь обязателен
        await edumatOut(message)


    @dp.message_handler(commands="congratsstudent")  # поздравление если ты харош
    async def CONGRATS(message: types.Message):  # await тeперь обязателен
        await congstuOut(message)

# Команды -------------------------------------------------------------------------------------------------------------
# Output функции ------------------------------------------------------------------------------------------------------


# Output функции ---------------------------------------------------------------------------------------------------
# Кнопки -----------------------------------------------------------------------------------------------------------
# async def BUTTON(message: types.Message):
#   if message.text == '🛠 Помощь':  # кнопочки, текст внутри message  не трогать
#      await message.reply("help  is working")
# elif message.text == '⁉ Частые вопросы':
#    await faqOut(message)
# elif message.text == '🧩 Тесты':
#   await testcheckOut(message)
# elif message.text == '🔔 Напомнить о занятии':
#   await remlesOut(message)
# elif message.text == '🔔 Напомнить о дедлайне':
#   await remdeadOut(message)
# elif message.text == '🎓 Успеваемость':
#   await eduresOut(message)
# elif message.text == '📚️ Учебный материал':
#   await edumatOut(message)
# elif message.text == '🏆 Топ':
#   await congstuOut(message)
# elif message.text == 'Другое ➡':
#   await message.reply("Другое ➡", reply_markup=nav.otherMenu)
# elif message.text == '⬅ Главное меню':
#   await message.reply("⬅ Главное меню", reply_markup=nav.mainMenu)

# СТАТУС ПРЕПОДАВАТЕЛЬ СТАТУС ПРЕПОДАВАТЕЛЬ СТАТУС ПРЕПОДАВАТЕЛЬ СТАТУС ПРЕПОДАВАТЕЛЬ СТАТУС ПРЕПОДАВАТЕЛЬ СТАТУС ПРЕПОД

@dp.message_handler()
async def SCRIPT(message: types.Message):
    if str(message.text[
           :10]).lower() == 'статистика':
        # код Полины
        '''inp = message.text.split(' ')
        if 'txt' in inp or 'тхт' in inp:
            tg_analytic.analysis(inp, message.chat.id)
            with open('%s.txt' % message.chat.id, 'r', encoding='UTF-8') as file:
                await message.answer_document(file)
                tg_analytic.remove(message.chat.id)
        else:
            messages = tg_analytic.analysis(inp, message.chat.id)
            await message.answer(message.chat.id, messages)'''

    elif "/" not in str(message.text):
        if text_has_emoji(str(message.text)) is False:
            await chat(message)  # Код Давида
        elif AUTHORIZATION_STATE == True:
            await StudBUTTON(message)  # Кнопки Ангелины
        elif AUTHORIZATION_STATE == False:
            await StudBUTTON(message)  # Кнопки Ангелины
    else:
        pass


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

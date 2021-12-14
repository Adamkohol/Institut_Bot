import logging
import asyncio

import emoji
from aiogram.utils.exceptions import BotBlocked
from aiogram import Bot, executor, types
from aiogram.dispatcher import Dispatcher
from os import getenv
from sys import exit
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

nltk.download('punkt')
stemmer = LancasterStemmer()

with open('intents.json', encoding='utf-8') as file:
    data = json.load(file)

try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

tensorflow.compat.v1.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
model.save("model.tflearn")

try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)


bot_token = getenv("BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

print("PROGRAM START")
# пример обработчика ошибки


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



# USLOVIE-----------------------------------------------------------------------------------------------------------
@dp.message_handler()
async def SCRIPT(message: types.Message):
    inp = str(message)

    results = model.predict([bag_of_words(inp, words)])[0]
    results_index = numpy.argmax(results)
    tag = labels[results_index]

    if message.text[:(10)] == 'Статистика': # ТУТ НЕ РАБОТАЕТ ВООБЩЕ НИЧЕГО КРОМЕ СКРИПТА ВНЕ ЕГО И В НЕМ НЕ РАБОТАЕТ
        inp = message.text.split(' ')
        if 'txt' in inp or 'тхт' in inp:
            tg_analytic.analysis(inp, message.chat.id)
            with open('%s.txt' % message.chat.id, 'r', encoding='UTF-8') as file:
                await message.answer_document(file)
                tg_analytic.remove(message.chat.id)
        else:
            messages = tg_analytic.analysis(inp, message.chat.id)
            await message.answer(message.chat.id, messages)
    else:
        if results[results_index] > 0.7:
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']

            await message.answer(random.choice(responses))
        else:
            await message.answer("Я не понял вас. Попробуйте снова")

# USLOVIE---------------------------------------------------------------------------------------------------------


# MENU----------------------------------------------------------------------------------------------------------------

@dp.message_handler(commands="start")  # новый обработчик
async def MENU(message: types.Message):  # await теперь обязателен
    await message.answer("\t Здравствуй!🤖 Бот для учебы, вот список команд:"
                        " \n /start - начало работы \n /help - 🛠 помощь \n /faq - ⁉ часто задаваемые вопросы \n"
                        " /remindlesson - 🔔 напомнить о занятии \n /reminddeadline - 🔔 напомнить о дедлайне \n "
                        "/educationresult - 🎓 успеваемость\n"
                        " /educationmaterial - 📚️ учебный материал \n"
                        " /testcheck - 🧩 тесты для самоподготовки\n"
                        " /congratsstudent -  🏆 топ учащихся\n", reply_markup=nav.mainMenu)

# команды
@dp.message_handler(commands="help")  #  помощь
async def HELP(message: types.Message):
    await helpOut(message)


@dp.message_handler(commands="faq")  # типичные вопросы
async def FAQ(message: types.Message):  # await теперь обязателен
    await faqOut(message)


@dp.message_handler(commands="remindlesson")  # напомнить о занятии
async def REMINDLES(message: types.Message):  # await теперь обязателен
    await remlesOut(message)


@dp.message_handler(commands="reminddeadline")  # напомнить о дедлайне
async def REMINDED(message: types.Message):  # await теперь обязателен
    await remdeadOut(message)


@dp.message_handler(commands="testcheck")   # тесты для самопроверки
async def TESTCHECK(message: types.Message):  # await тeперь обязателен
    await testcheckOut(message)


@dp.message_handler(commands="educationresult")   # об успеваемости
async def EDRESUL(message: types.Message):  # await тeперь обязателен
    await eduresOut(message)


@dp.message_handler(commands="educationmaterial")  # учебный материал
async def EDMAT(message: types.Message):  # await тeперь обязателен
    await edumatOut(message)


@dp.message_handler(commands="congratsstudent")  # поздравление если ты харош
async def CONGRATS(message: types.Message):  # await тeперь обязателен
    await congstuOut(message)


@dp.message_handler()
async def BUTTON(message: types.Message):
    if message.text == '🛠 Помощь':  #кнопочки, текст внутри message  не трогать
        await helpOut(message)
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

# MENU-----------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

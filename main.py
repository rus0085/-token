import sqlite3
from aiogram import types
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.types import CallbackQuery
import random
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle
import datetime
import time
import datetime
hideBoard = types.ReplyKeyboardRemove()


token = '***************'


bot = Bot(token)
dp = Dispatcher(bot, storage=MemoryStorage())

class FSMrass(StatesGroup):
    api = State()
    base = State()
    ras = State()
    proverka_ras = State()


@dp.message_handler(commands=["start"])
async def start(message):

    await bot.send_message(message.from_user.id,"Введите токен бота")
    await FSMrass.api.set()


@dp.message_handler(state = FSMrass.api)
async def api(message,state: FSMContext):
  try:
    await state.update_data(api=message.text)
    await bot.send_message(message.from_user.id, "Пришлите базу пользователей")
    await FSMrass.base.set()
  except:
      await state.finish()
      await bot.send_message(message.from_user.id, "что то не так")




@dp.message_handler(content_types=types.ContentType.ANY, state = FSMrass.base)
async def base(message,state: FSMContext):
    try:
        id = message["document"]["file_id"]
        destination = fr"/root/rassil/{id}.db"
        await bot.download_file_by_id(file_id= id, destination=destination)
        await state.update_data(base=id)
        await bot.send_message(message.from_user.id, "Перешлите сообщение для рассылки")
        await FSMrass.ras.set()
    except:
        await state.finish()
        await bot.send_message(message.from_user.id, "что то не так")









@dp.message_handler(content_types=types.ContentType.ANY, state = FSMrass.ras)
async def post(message:types.message.Message, state: FSMContext):
  try:
    markup1 = types.InlineKeyboardMarkup()
    try:
     a = message["reply_markup"]['inline_keyboard']

     for i in range(10):

        try:
            y = str(a[i])
            i1 = y.split('"')
            p = []
            for o in range(3,60,8):
                try:
                    btn1 = types.InlineKeyboardButton(text=i1[o], url=i1[o+4])
                    p.append(btn1)
                except:
                    break
            try:
                    markup1.row(p[0],p[1],p[2],p[3],p[4],p[5])
            except:
                try:
                            markup1.row(p[0],p[1],p[2],p[3],p[4])
                except:
                    try:
                                    markup1.row(p[0],p[1],p[2],p[3])
                    except:
                        try:
                                            markup1.row(p[0],p[1],p[2])
                        except:
                            try:
                                                    markup1.row(p[0],p[1])
                            except:
                                try:
                                                            markup1.row(p[0])
                                except:
                                    1
        except:
            break
    except:
        1
    await state.update_data(chat_id =message.chat.id)
    await state.update_data(message_id= message.message_id)
    await state.update_data(markup= markup1)
    #await bot.copy_message(chat_id=message.chat.id, from_chat_id=message.chat.id, message_id=message.message_id ,reply_markup=markup1)
    try:
        id = message["video"]["file_id"]
        destination = fr"/root/rassil/{id}.mp4"
        #destination = fr"C:\Users\****\PycharmProjects\rassilka_bot\{id}.mp4"
        await bot.download_file_by_id(file_id=id, destination=destination)
        await state.update_data(video=id )
    except:
        1

    try:
        id = message["photo"][2]["file_id"]
        #destination = fr"C:\Users\****\PycharmProjects\rassilka_bot\{id}.jpg"
        destination = fr"/root/rassil/{id}.jpg"
        await bot.download_file_by_id(file_id=id, destination=destination)
        await state.update_data(photo=id )
    except:
        1
    text = message["caption"]
    text1 = message.text
    await state.update_data(text=text)
    await state.update_data(text1=text1)
    data = await state.get_data()

    try:
        id = data["photo"]
        await bot.send_photo(chat_id=message.from_user.id, photo=open(fr"/root/rassil/{id}.jpg", "rb"), reply_markup=data["markup"],
                             caption=data["text"])
    except:
        1
    try:
        id = data["video"]
        await bot.send_video(chat_id=message.from_user.id, video=open(fr"/root/rassil/{id}.mp4", "rb"), reply_markup=data["markup"],
                             caption=data["text"])
    except:
        1
    try:
        await bot.send_message(chat_id=message.from_user.id, text = text1, reply_markup=data["markup"])
    except:
        1

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Да")
    btn2 = types.KeyboardButton("Нет")
    markup.add(btn1, btn2)
    await bot.send_message(message.from_user.id, "Верно?", reply_markup=markup)
    await FSMrass.proverka_ras.set()

  except:
      await state.finish()
      await bot.send_message(message.from_user.id, "что то не так")

@dp.message_handler(content_types=types.ContentType.ANY, state = FSMrass.proverka_ras)
async def prov(message,state: FSMContext):

    if message.text == "Да":
        await bot.send_message(message.from_user.id, "Хорошо, начинаю рассылку...", reply_markup=hideBoard)
        await rassilka(message,state)

    elif message.text == "Нет":
        await state.finish()
        await bot.send_message(message.from_user.id, "Тогда попробуйте заново:)" )



async def rassilka(message,state):
    data = await state.get_data()

    token1 = data["api"]
    bot1 = Bot(token1)
    dp1 = Dispatcher(bot1)

    id = data["base"]
    connector = sqlite3.connect(fr"/root/rassil/{id}.db")
    cursor = connector.cursor()
    cursor.execute("SELECT * FROM users")
    r = cursor.fetchall()


    try:
        if len(data["video"]) >1:
            id = data["video"]
            for i in range(len(r)):
                    try:
                        await bot1.send_video(chat_id=r[i][0], video= open(fr"/root/rassil/{id}.mp4", "rb"), reply_markup=data["markup"],caption=data["text"])
                    except:
                        1
    except:
        try:
            if len(data["photo"]) > 1:
                id = data["photo"]
                for i in range(len(r)):
                    try:
                        await bot1.send_photo(chat_id=r[i][0], photo=open(fr"/root/rassil/{id}.jpg", "rb"),
                                              reply_markup=data["markup"], caption=data["text"])
                    except:
                        1
        except:
            try:

                textpr = data["text1"]
                if len(textpr) > 0:
                    for i in range(len(r)):
                        try:
                            await bot1.send_message(chat_id=r[i][0], reply_markup=data["markup"], text=textpr)
                        except:
                            1
            except:
                1




    await bot.send_message(message.from_user.id, "выполнено", reply_markup=hideBoard)
    await state.finish()






executor.start_polling(dp, skip_updates=True)

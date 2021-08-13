from aiogram import Bot, Dispatcher, executor, types
from config import db_login, db_password, db_host, db_name, telegram_token
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import pymongo
from loguru import logger
from datetime import datetime
import pytz

client = pymongo.MongoClient(f"mongodb://{db_login}:{db_password}@{db_host}/{db_name}?authSource=admin")
db = client["joker_database"]
jokes_collection = db["jokes"]
bjokes_collection = db["jokes_b_category"]
info_collection = db["info"]

bot = Bot(token=telegram_token)
dp = Dispatcher(bot)

classic_jokes_category_button = KeyboardButton("Классические")  # create button
jokes_b_category_button = KeyboardButton("Категория Б")
# add_new_joke = KeyboardButton("Предложка")
info_button = KeyboardButton("Информация")

menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)  # create keyboard for button
menu_keyboard.add(classic_jokes_category_button, jokes_b_category_button, info_button)
# menu_keyboard.add(add_new_joke)

random_joke_button = KeyboardButton("Пошути")
back_to_menu_button = KeyboardButton("Меню")

classic_jokes_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
classic_jokes_keyboard.add(random_joke_button, back_to_menu_button)

random_bjoke_button = KeyboardButton("Пошyти")

jokes_b_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
jokes_b_keyboard.add(random_bjoke_button, back_to_menu_button)


# add_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
# add_keyboard.add(back_to_menu_button)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Hola, amigo!", reply_markup=menu_keyboard)


@dp.message_handler()
async def get_random_joke(message: types.Message):
    message_from = message["from"]

    if (message["text"] == "Информация") and (message_from["id"] == 76939702):
        box = info_collection.find().sort([("date", pymongo.ASCENDING)])
        box = [str(el["category"]) + ": {" +
               str(el["first_name"]) + ", " +
               str(el["username"]) + ", " +
               str(el["user_id"]) + ", " +
               str(el["time"]) + "}" for el in box]
        info = "\n".join(box)
        await bot.send_message(message.from_user.id, str(info))

    elif(message["text"] == "Информация") and (message_from["id"] != 76939702):
        await bot.send_message(message.from_user.id, "Кнопка доступна только авторизованным пользователям")

    elif message["text"] == "Меню":
        await bot.send_message(message.from_user.id, "Меню", reply_markup=menu_keyboard)

    elif message["text"] == "Классические":
        await bot.send_message(message.from_user.id, "Классические", reply_markup=classic_jokes_keyboard)

    elif message["text"] == "Пошути":
        random_joke = jokes_collection.aggregate([{"$sample": {"size": 1}}])
        random_joke = {"content": el["content"] for el in random_joke}
        random_joke = random_joke["content"]

        category = "Классические"
        users_info(message, category)

        if len(random_joke) > 4096:
            trim_joke = (random_joke[0+i:4096+i] for i in range(0, len(random_joke), 4096))
            for element in trim_joke:
                await bot.send_message(message.from_user.id, element)

        else:
            await bot.send_message(message.from_user.id, random_joke)

    elif message["text"] == "Категория Б":
        await bot.send_message(message.from_user.id, "Категория Б", reply_markup=jokes_b_keyboard)

    elif message["text"] == "Пошyти":
        random_joke = bjokes_collection.aggregate([{"$sample": {"size": 1}}])
        random_joke = {"content": el["content"] for el in random_joke}
        random_joke = random_joke["content"]

        category = "Категория Б"
        users_info(message, category)

        if len(random_joke) > 4096:
            trim_joke = (random_joke[0 + i:4096 + i] for i in range(0, len(random_joke), 4096))
            for element in trim_joke:
                await bot.send_message(message.from_user.id, element)

        else:
            await bot.send_message(message.from_user.id, random_joke)

    # elif message["text"] == "Предложка":
    #     await bot.send_message(message.from_user.id, "@КАТЕГОРИЯ, АНЕК", reply_markup=add_keyboard)

    else:
        await bot.send_message(message.from_user.id, "Пользуйся кнопками! \nДля рестарта жми > /start <")


def users_info(message, category):
    info_from = message["from"]

    info_id = info_from["id"]
    info_first_name = info_from["first_name"]
    info_username = info_from["username"]
    utc_dt = datetime.utcnow()
    msc_tz = pytz.timezone('Europe/Moscow')
    time = utc_dt.replace(tzinfo=pytz.utc).astimezone(msc_tz)
    time = msc_tz.normalize(time)
    time = str(time)
    time = time[11:16]

    user_info_container = {
        "user_id": info_id,
        "first_name": info_first_name,
        "username": info_username,
        "time": time,
        "category": category
    }
    info_collection.insert_one(user_info_container)

    for_logger = {
        "first_name": info_first_name,
        "username": info_username
    }
    logger.info(for_logger)


if __name__ == '__main__':
    executor.start_polling(dp)

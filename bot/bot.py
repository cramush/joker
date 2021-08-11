from aiogram import Bot, Dispatcher, executor, types
from config import db_login, db_password, db_host, db_name, telegram_token
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import pymongo
from loguru import logger

client = pymongo.MongoClient(f"mongodb://{db_login}:{db_password}@{db_host}/{db_name}?authSource=admin")
db = client["joker_database"]
jokes_collection = db["jokes"]
info_collection = db["info"]

bot = Bot(token=telegram_token)
dp = Dispatcher(bot)

random_joke_button = KeyboardButton('Пошути')  # create button

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)  # create keyboard for button
keyboard.add(random_joke_button)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Жми на кнопку, шутить буду.", reply_markup=keyboard)


@dp.message_handler()
async def get_random_joke(message: types.Message):
    message_from = message["from"]

    if (message["text"] == "/info") and (message_from["id"] == 76939702):
        box = info_collection.find().sort([("date", pymongo.ASCENDING)])
        box = [str(el["content"]) + ": {" +
               str(el["first_name"]) + ", " +
               str(el["username"]) + ", " +
               str(el["user_id"]) + ", " +
               str(el["time"]) + "}" for el in box]
        info = "\n".join(box)
        await bot.send_message(message.from_user.id, str(info))

    else:
        random_joke = jokes_collection.aggregate([{"$sample": {"size": 1}}])
        random_joke = {"content": el["content"] for el in random_joke}
        random_joke = random_joke["content"]

        users_info(message)

        if len(random_joke) > 4096:
            trim_joke = (random_joke[0+i:4096+i] for i in range(0, len(random_joke), 4096))
            for element in trim_joke:
                await bot.send_message(message.from_user.id, element)

        else:
            await bot.send_message(message.from_user.id, random_joke)


def users_info(message):
    info_from = message["from"]

    info_id = info_from["id"]
    info_first_name = info_from["first_name"]
    info_username = info_from["username"]
    info_date = message["date"]
    time = str(info_date)
    hours = int(time[11:13]) + 3
    minutes = time[13:16]
    time = str(hours) + minutes
    info_text = message["text"]

    user_info_container = {
        "user_id": info_id,
        "first_name": info_first_name,
        "username": info_username,
        "time": time,
        "content": info_text
    }
    info_collection.insert_one(user_info_container)

    for_logger = {
        "first_name": info_first_name,
        "username": info_username
    }
    logger.info(for_logger)


if __name__ == '__main__':
    executor.start_polling(dp)

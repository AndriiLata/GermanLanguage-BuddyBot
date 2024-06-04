import os
import telebot
from telebot import types
from telebot.types import Message

import database

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')
# check if bot token is none or empty
if BOT_TOKEN is None or BOT_TOKEN == '':
    print('Bot token is missing')
    exit()
bot = telebot.TeleBot(BOT_TOKEN)


# Dictionary to store user data
user_data = {}

# States
STATE_ASK_FOR_NAME = 0
STATE_ASK_FOR_GERMAN_LEVEL = 1
STATE_ASK_FOR_PICTURE = 2
STATE_ASK_FOR_INFO = 3
STATE_PROFILE_COMPLETE = 4


@bot.message_handler(commands=['start'])
def start(message: Message):
    user_data['state'] = STATE_ASK_FOR_NAME
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("Start")
    markup.add(item)
    bot.send_message(message.chat.id, "To get started please enter your name.", reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(func=lambda message: user_data['state'] == STATE_ASK_FOR_NAME)
def handle_name(message: Message):
    user_data['name'] = message.text
    user_data['state'] = STATE_ASK_FOR_GERMAN_LEVEL
    bot.send_message(message.chat.id, f"Thanks {message.text}, now please select your german level:",
                     reply_markup=create_level_keyboard())


def create_level_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    levels = ['A1 - A2', 'B1 - B2', 'C1', 'Native Speaker']
    markup.add(*[types.KeyboardButton(level) for level in levels])
    return markup


# Handle language level selection
@bot.message_handler(func=lambda message: user_data['state'] == STATE_ASK_FOR_GERMAN_LEVEL)
def handle_language_level(message: Message):
    user_data['language_level'] = message.text
    user_data['state'] = STATE_ASK_FOR_PICTURE
    name = user_data['name']

    bot.send_message(message.chat.id, f"Great! "
                                      f"{name}, before we start matching you, please upload a picture of yourself.",
                     reply_markup=types.ReplyKeyboardRemove())


#TODO: Handle picture upload
@bot.message_handler(content_types=['photo'])
def handle_photo(message: Message):
    user_data['state'] = STATE_ASK_FOR_INFO
    user_data['file_id'] = message.photo[-1].file_id

    name = user_data['name']
    language_level = user_data['language_level']
    file_id = user_data['file_id']

    bot.send_photo(message.chat.id, file_id,
                   caption=f"{name}, German level: {language_level}\n\n"
                           f"Now please write something about yourself to make your profile more personal.\n"
                           f"For example, what are you studying or where are you from\n\n ")


@bot.message_handler(func=lambda message: user_data['state'] == STATE_ASK_FOR_INFO)
def handle_info(message: Message):
    user_data['state'] = STATE_PROFILE_COMPLETE
    user_data['personal_info'] = message.text

    database.get_connection()
    database.create_table()
    database.insert_user_data(user_data)
# for loop to iterate over the user_data dictionary
    for key, value in user_data.items():
        print(key, value)

    bot.send_message(message.chat.id, "Thanks for sharing your information. Your profile is now complete. "
                                      "We will now match you with other users.")


bot.infinity_polling()
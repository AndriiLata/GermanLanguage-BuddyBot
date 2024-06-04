import os
import telebot
from telebot import types
from telebot.types import Message

import database
import match

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


database.get_connection()
database.create_table()
database.create_table_matches()


@bot.message_handler(func=lambda message: message.text == 'Stop ✋')
@bot.message_handler(commands=['start'])
def start(message: Message):
    user = database.search_me(message.chat.id)
    if user:
        my_profile(user[4], user[2], user[3], user[5], message)
    else:
        start(message)


def my_profile(file_id, name, language_level, info, message: Message):
    markup = types.ReplyKeyboardMarkup(row_width=1 ,resize_keyboard=True)
    edit_profile = types.KeyboardButton("Edit Profile")
    start_matching = types.KeyboardButton("Start Matching")
    markup.add(start_matching, edit_profile)
    bot.send_photo(message.chat.id, file_id,
                   caption=f"{name}, German level: {language_level}\n\n"
                           f"{info}\n",
                   reply_markup=markup)


def shown_profile(file_id, name, language_level, info, message: Message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    like = types.KeyboardButton("❤️")
    dislike = types.KeyboardButton("👎")
    myprofile = types.KeyboardButton("Stop ✋")
    markup.add(like, dislike, myprofile)
    bot.send_photo(message.chat.id, file_id,
                   caption=f"{name}, German level: {language_level}\n\n"
                           f"{info}\n",
                   reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Start Matching'
                                          or message.text == '❤️' or message.text == '👎')
def start_matching(message: Message):

    if message.text == '❤️':
        previous_profile = database.get_previous_profile(message.chat.id)
        if previous_profile:
            database.insert_match(message.chat.id, previous_profile[0])
            #TODO : bot.send_contact()
        else:
            print('No previous profile found')

    elif message.text == '👎':
        previous_profile = database.get_previous_profile(message.chat.id)
        if previous_profile:
            database.insert_match(message.chat.id, previous_profile[0])
        else:
            print('No previous profile found')

    me = database.search_me(message.chat.id)
    showed_user = match.get_user(me[3], message.chat.id)
    if showed_user:
        shown_profile(showed_user[4], showed_user[2], showed_user[3], showed_user[5], message)
        chat_id_from_showed_user = showed_user[6]
        database.insert_previous_profile(message.chat.id, chat_id_from_showed_user)
    else:
        bot.send_message(message.chat.id, "You have reached your daily limit. Please try again tomorrow.")


@bot.message_handler(func=lambda message: message.text == 'Edit Profile')
def start(message: Message):
    database.delete_user(message.chat.id)
    user_data['state'] = STATE_ASK_FOR_NAME
    bot.send_message(message.chat.id, "To get started please enter your name.")


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
                           f"For example, what you are studying or where you are from\n\n ")


@bot.message_handler(func=lambda message: user_data['state'] == STATE_ASK_FOR_INFO)
def handle_info(message: Message):
    user_data['state'] = STATE_PROFILE_COMPLETE
    user_data['personal_info'] = message.text
    user_data['chat_id'] = message.chat.id

    database.insert_user_data(user_data)

    my_profile(user_data['file_id'], user_data['name'], user_data['language_level'], user_data['personal_info'], message)


bot.infinity_polling()
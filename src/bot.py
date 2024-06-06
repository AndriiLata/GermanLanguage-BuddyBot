import os, sys
import telebot
from telebot import types
from telebot.types import Message
from telebot.apihelper import ApiTelegramException

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
STATE_MOBILE_NUMBER = 5


database.get_connection()
database.create_table()
database.create_table_matches()


@bot.message_handler(func=lambda message: message.text == 'Stop ✋')
@bot.message_handler(commands=['start'])
def start(message: Message):

    user = database.search_me(message.chat.id)
    if user:

        my_profile(user[5], user[3], user[4], user[6], message)

    else:
        start(message)


def my_profile(file_id, name, language_level, info, message: Message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
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
        previous_profile = database.get_previous_profile(message.chat.id) # this is only the ID of the previous user
        if previous_profile:
            database.insert_match(message.chat.id, previous_profile[0])

            my_phone_number = database.search_me(message.chat.id)[8]
            my_name = database.search_me(message.chat.id)[3]

            his_name = database.search_me(previous_profile[0])[3]

            try:
                bot.send_contact(previous_profile[0], my_phone_number, my_name)
                bot.send_message(previous_profile[0], f"{my_name} from Munich liked you! ❤️"
                                                      f"\nText him/her to start practicing german together 🇩🇪🚀")
                bot.send_message(message.chat.id, f"Your contact has been shared with {his_name}")
            except ApiTelegramException as e:
                bot.send_message(message.chat.id, f"Something went wrong. Please try again later.")
        else:
            print('No previous profile found')

    elif message.text == '👎':
        previous_profile = database.get_previous_profile(message.chat.id)
        if previous_profile:
            database.insert_match(message.chat.id, previous_profile[0])
        else:
            print('No previous profile found')

    me = database.search_me(message.chat.id)
    showed_user = match.get_user(me[4], message.chat.id)
    if showed_user:
        shown_profile(showed_user[5], showed_user[3], showed_user[4], showed_user[6], message)
        chat_id_from_showed_user = showed_user[2]
        database.insert_previous_profile(message.chat.id, chat_id_from_showed_user)
    else:
        bot.send_message(message.chat.id, "You have reached your daily limit. Please try again tomorrow.")


@bot.message_handler(func=lambda message: message.text == 'Edit Profile')
def start(message: Message):
    database.delete_user(message.chat.id)

    if message.chat.id not in user_data:
        user_data[message.chat.id] = {}

    user_data[message.chat.id]['state'] = STATE_ASK_FOR_NAME
    bot.send_message(message.chat.id, "To get started please enter your name.", reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(func=lambda message: user_data[message.chat.id]['state'] == STATE_ASK_FOR_NAME)
def handle_name(message: Message):
    user_data[message.chat.id]['name'] = message.text
    user_data[message.chat.id]['state'] = STATE_ASK_FOR_GERMAN_LEVEL
    bot.send_message(message.chat.id, f"Thanks {message.text}, now please select your german level:",
                     reply_markup=create_level_keyboard())


def create_level_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    levels = ['A1 - A2', 'B1 - B2', 'C1', 'Native Speaker']
    markup.add(*[types.KeyboardButton(level) for level in levels])
    return markup


# Handle language level selection
@bot.message_handler(func=lambda message: user_data[message.chat.id]['state'] == STATE_ASK_FOR_GERMAN_LEVEL)
def handle_language_level(message: Message):
    user_data[message.chat.id]['language_level'] = message.text
    user_data[message.chat.id]['state'] = STATE_ASK_FOR_PICTURE
    name = user_data[message.chat.id]['name']

    bot.send_message(message.chat.id, f"Great! "
                                      f"{name}, before we start matching you, please upload a picture of yourself.",
                     reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(content_types=['photo'])
def handle_photo(message: Message):
    user_data[message.chat.id]['state'] = STATE_ASK_FOR_INFO
    user_data[message.chat.id]['file_id'] = message.photo[-1].file_id

    name = user_data[message.chat.id]['name']
    language_level = user_data[message.chat.id]['language_level']
    file_id = user_data[message.chat.id]['file_id']

    bot.send_photo(message.chat.id, file_id,
                   caption=f"{name}, German level: {language_level}\n\n"
                           f"Now please write something about yourself to make your profile more personal.\n"
                           f"For example, what you are studying or where you are from\n\n ")


@bot.message_handler(func=lambda message: user_data[message.chat.id]['state'] == STATE_ASK_FOR_INFO)
def handle_info(message: Message):
    user_data[message.chat.id]['state'] = STATE_PROFILE_COMPLETE
    user_data[message.chat.id]['personal_info'] = message.text

    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = types.KeyboardButton("Send Phone Number", request_contact=True)
    markup.add(button)

    bot.send_message(message.chat.id, "Your profile has been created successfully.\n"
                                      "To be able to use the bot, you need to share your contact with the button below",
                     reply_markup=markup)


# ask for phone number
@bot.message_handler(content_types=['contact'])
def handle_phone_number(message: Message):
    user_data[message.chat.id]['state'] = STATE_MOBILE_NUMBER
    user_data[message.chat.id]['phone_number'] = message.contact.phone_number
    user_data[message.chat.id]['chat_id'] = message.chat.id

    database.insert_user_data(user_data[message.chat.id])

    my_profile(user_data[message.chat.id]['file_id'], user_data[message.chat.id]['name'], user_data[message.chat.id]['language_level'], user_data[message.chat.id]['personal_info'], message)


bot.infinity_polling()
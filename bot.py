import os
import telebot
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')


# check if bot token is none or empty
if BOT_TOKEN is None or BOT_TOKEN == '':
    print('Bot token is missing')
    exit()


bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I am a bot.")


bot.infinity_polling()
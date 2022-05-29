from googletrans import Translator
from langdetect import detect
import telebot
import config
import logging
import emoji
import re

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
bot = telebot.TeleBot(config.telegram["token"], threaded=False)
translator = Translator(service_urls=config.google["service_urls"])

def remove_emoji(text):
    result = emoji.demojize(text)
    result = re.sub(':.*?:', '', result)
    return result

def translate(text):
    cleantext = remove_emoji(text)
    if detect(cleantext):
        result = translator.translate(cleantext, dest='en')
        return result.text
    else:
        return None

def detect_en(text):
    if detect(text) == 'ru':
        return True
    else:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Hello {message.from_user.first_name}, welcome to Google Translate bot!')

@bot.channel_post_handler(func=lambda message: True, content_types=["text"])
def channel_text_post(message):
    try:
        if detect_en(remove_emoji(message.text)):
            bot.reply_to(message, translate(message.text), disable_notification=True)
        else:
            pass
    except:
        logger.error("Fatal error in channel handler", exc_info=True)

@bot.channel_post_handler(func=lambda message: True, content_types=["photo", "video", "document"])
def channel_media_post(message):
    try:
        if detect_en(remove_emoji(message.text)):
            bot.reply_to(message, translate(message.caption), disable_notification=True)
        else:
            pass
    except:
        logger.error("Fatal error in channel handler", exc_info=True)

@bot.message_handler(func=lambda message: True, content_types=["text"])
def message_text_handler(message):
    try:
        if detect_en(remove_emoji(message.text)):
            bot.reply_to(message, translate(message.text))
        else:
            pass
    except:
        logger.error("Fatal error in message handler", exc_info=True)

@bot.message_handler(func=lambda message: True, content_types=["photo", "video", "document"])
def message_media_handler(message):
    try:
        if detect_en(remove_emoji(message.text)):
            bot.reply_to(message, translate(message.caption))
        else:
            pass
    except:
        logger.error("Fatal error in message handler", exc_info=True)

bot.infinity_polling()
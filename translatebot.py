from googletrans import Translator
from langdetect import detect
import telebot
import config
import logging
import emoji
import re


logging.basicConfig(filename='bot.log',level=logging.ERROR)
logger = logging.getLogger(__name__)
bot = telebot.TeleBot(config.telegram["token"])
translator = Translator(service_urls=config.google["service_urls"])


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Hello {message.from_user.first_name}, welcome to Google Translate bot!')

@bot.channel_post_handler(func=lambda message: True, content_types=["text"])
def message(message):
    try:
        bot.send_message(message.chat.id, translate(message.text))
    except:
        logger.error("Fatal error in channel handler", exc_info=True)

@bot.channel_post_handler(func=lambda message: True, content_types=["photo", "video"])
def message(message):
    try:
        bot.send_message(message.chat.id, translate(message.caption))
    except:
        logger.error("Fatal error in channel handler", exc_info=True)

@bot.message_handler(func=lambda message: True, content_types=["text"])
def message(message):
    try:
        bot.send_message(message.chat.id, translate(message.text))
    except:
        logger.error("Fatal error in message handler", exc_info=True)

@bot.message_handler(func=lambda message: True, content_types=["photo", "video"])
def message(message):
    try:
        bot.send_message(message.chat.id, translate(message.caption))
    except:
        logger.error("Fatal error in message handler", exc_info=True)

def remove_emoji(text):
    result = emoji.demojize(text)
    result = re.sub(':.*?:', '', result)
    return result

def translate(text):
    cleantext = remove_emoji(text)
    if detect(cleantext) != 'en':
        result = translator.translate(cleantext, dest='en')
        return result.text
    else:
        return


def main():
    bot.polling(timeout=30)


if __name__ == '__main__':
    main()

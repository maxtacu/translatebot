from googletrans import Translator
from langdetect import detect
import telebot
import config
import logging
import emoji
import re
from flask import Flask, request


secret = 'translatebot'
url = 'https://tmax.pythonanywhere.com/' + secret

logging.basicConfig(filename='bot.log',level=logging.ERROR)
logger = logging.getLogger(__name__)
bot = telebot.TeleBot(config.telegram["token"], threaded=False)
bot.remove_webhook()
bot.set_webhook(url=url, max_connections=10, allowed_updates=["message", "channel_post"])
translator = Translator(service_urls=config.google["service_urls"])

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

app = Flask(__name__)
@app.route('/'+secret, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200

@app.route('/', methods=['GET'])
def healthcheck():
    return 'ok', 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Hello {message.from_user.first_name}, welcome to Google Translate bot!')

@bot.channel_post_handler(func=lambda message: True, content_types=["text"])
def channel_text_post(message):
    try:
        bot.send_message(message.chat.id, translate(message.text), disable_notification=True)
    except:
        logger.error("Fatal error in channel handler", exc_info=True)

@bot.channel_post_handler(func=lambda message: True, content_types=["photo", "video", "document"])
def channel_media_post(message):
    try:
        bot.send_message(message.chat.id, translate(message.caption), disable_notification=True)
    except:
        logger.error("Fatal error in channel handler", exc_info=True)

@bot.message_handler(func=lambda message: True, content_types=["text"])
def message_text_handler(message):
    try:
        bot.send_message(message.chat.id, translate(message.text))
    except:
        logger.error("Fatal error in message handler", exc_info=True)

@bot.message_handler(func=lambda message: True, content_types=["photo", "video", "document"])
def message_media_handler(message):
    try:
        bot.send_message(message.chat.id, translate(message.caption))
    except:
        logger.error("Fatal error in message handler", exc_info=True)





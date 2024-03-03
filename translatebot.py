from googletrans import Translator
import telebot
import config
import logging
import emoji
import re
import deepl

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
bot = telebot.TeleBot(config.telegram["token"], threaded=False)

google_translator = Translator(service_urls=config.google["service_urls"])
deepl_translator = deepl.Translator(config.telegram["deepl_api_key"])

CAPTION_LIMIT = 1024
TEXT_LIMIT = 4096

def remove_emoji(text):
    result = emoji.demojize(text)
    result = re.sub(':.*?:', '', result)
    return result

def google_translate(text):
    result = google_translator.translate(text, dest='en')
    return result.text
    
def deepl_translate(text):
    result = deepl_translator.translate_text(text, target_lang='EN-GB')
    return result.text

def detect_ru(text):
    if google_translator.detect(text).lang == 'en':
        return False
    else:
        return True

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.username:
        logger.info(f"User {message.from_user.username} started the bot")
    else:
        logger.info(f"User {message.from_user.id} started the bot")
    bot.send_message(message.chat.id, f'Hello {message.from_user.first_name}, welcome to Google Translate bot!')

@bot.channel_post_handler(func=lambda message: True, content_types=["text"])
def channel_text_post(message):
    logger.info(f"Received message from channel {message.chat.id}")
    try:
        if detect_ru(remove_emoji(message.text)):
            translated_text = deepl_translate(message.text)
            joint_translated_text = f"{message.text}\n---\n{translated_text}"
            if len(joint_translated_text) < TEXT_LIMIT:
                bot.edit_message_text(message_id=message.message_id, chat_id=message.chat.id, text=joint_translated_text)
            else:
                logger.debug("Translated message too long, sending as a separate message")
                bot.send_message(chat_id=message.chat.id, text=translated_text)
        else:
            pass
    except:
        logger.error("Fatal error in channel handler", exc_info=True)

@bot.channel_post_handler(func=lambda message: True, content_types=["photo", "video", "document"])
def channel_media_post(message):
    logger.info(f"Received media message from channel {message.chat.id}")
    try:
        if detect_ru(message.caption):
            translated_text = deepl_translate(message.caption)
            joint_translated_text = f"{message.caption}\n---\n{translated_text}"
            if len(joint_translated_text) < CAPTION_LIMIT:
                bot.edit_message_caption(message_id=message.message_id, chat_id=message.chat.id, caption=joint_translated_text)
            else:
                logger.debug("Translated caption too long, sending as a separate message")
                bot.send_message(chat_id=message.chat.id, text=translated_text)            
        else:
            pass
    except:
        logger.error("Fatal error in channel handler", exc_info=True)

@bot.message_handler(func=lambda message: True, content_types=["text"])
def message_text_handler(message):
    if message.from_user.username:
        logger.info(f"Received message from {message.from_user.username}")
    else:
        logger.info(f"Received message from {message.from_user.id}")
    try:
        if detect_ru(remove_emoji(message.text)):
            bot.reply_to(message, google_translate(message.text))
        else:
            pass
    except:
        logger.error("Fatal error in message handler", exc_info=True)

@bot.message_handler(func=lambda message: True, content_types=["photo", "video", "document"])
def message_media_handler(message):
    if message.from_user.username:
        logger.info(f"Received message from {message.from_user.username}")
    else:
        logger.info(f"Received message from {message.from_user.id}")
    try:
        if detect_ru(remove_emoji(message.text)):
            bot.reply_to(message, google_translate(message.caption))
        else:
            pass
    except:
        logger.error("Fatal error in message handler", exc_info=True)

bot.infinity_polling(skip_pending=True, timeout=30)
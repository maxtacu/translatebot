from googletrans import Translator
import telebot
import config

bot = telebot.TeleBot(config.telegram["token"])
translator = Translator(service_urls=config.google["service_urls"])


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Hello {message.from_user.first_name}, welcome to Google Translate bot!')

@bot.channel_post_handler(func=lambda message: True, content_types=["text"])
def message(message):
    bot.send_message(message.chat.id, translate(message.text))

@bot.channel_post_handler(func=lambda message: True, content_types=["photo", "video"])
def message(message):
    bot.send_message(message.chat.id, translate(message.caption))

@bot.message_handler(func=lambda message: True, content_types=["text"])
def message(message):
    bot.send_message(message.chat.id, translate(message.text))

@bot.message_handler(func=lambda message: True, content_types=["photo", "video"])
def message(message):
    bot.send_message(message.chat.id, translate(message.caption))

def translate(text):
    try:
        result = translator.translate(text, dest='en')
        return result.text
    except Exception as e:
        print(e)

def main():
    bot.polling(timeout=30)


if __name__ == '__main__':
    main()

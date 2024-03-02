# Telegram "Google Translate" bot written in Python

This bot was inspired by a wish to make my personal blog-channel understandable for my english-speaking colleagues and friends. 

Bot translates any text from any language to English. This text could be a 
direct message, channel post or any photo/video caption. 

Translated message will be without any emojis if any exists in the source text.

You can't change the language this bot translates to (only to English). 

To use this bot just install requirements:
```
pip install -r requirements.txt
```
Set your bot telegram token as environment variable:
```
export TOKEN='your-token-value'
```
Or you can set it explicitly in the `config.py` file.
And then run the python script:
```
python translatebot.py
```
Bot writes all occurred exceptions to the log file `bot.log`
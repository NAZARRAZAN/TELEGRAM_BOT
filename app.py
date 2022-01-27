import requests
import json
import telebot

from config import TOKEN, keys
from extensions import Convertation, APIExeption

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start", "help"])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу введите комманду боту в следующем фотмате:\n<имя валюты> \
        <имя валюты, в которой надо узнать цену первой валюты> \
        <количество первой валюты>"
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты"
    for k in keys.keys():
        text = "\n".join((text, k))
    bot.reply_to(message, text)

@bot.message_handler(content_types=["text"])
def convert(message: telebot.types.Message):
    try:
        n_vords = message.text.split(" ")

        if len(n_vords) != 3:
            raise APIExeption("Ошибка при вводе данных, должно быть 3 слова")

        quote, base, amount = n_vords
        total_base = Convertation.get_price(quote, base, amount)
    except APIExeption as e:
        bot.reply_to(message, f"USER FAIL\n {e}")
    except Exception as e:
        bot.reply_to(message, f"SYSTEM FAIL\n {e}")
    else:
        text = f"{amount} {quote} = {total_base} {base}"
        bot.reply_to(message, text)

bot.polling()
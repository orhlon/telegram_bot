#t.me/friday_from_robinson_crusoe_bot

import telebot
import requests
import json
from config import TOKEN

class ConvertException(Exception):
    pass

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    bot.reply_to(message, 'Доступные команды:\n/values\n/convert')
    bot.send_message(message.chat.id, 'Введите валюту, валюту в какую перевести и количество\nНапример: usd eur 1')

    
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    bot.reply_to(message, 'Доступные валюты: \nUSD\nEUR\nRUB')
    
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    curr_check = ['usd', 'eur', 'rub']
    currencies = {0: '', 1: '', 2: 0}
    format_correct = False
    sep_raw_input = message.text.split(' ')
    if len(sep_raw_input) == 3:
        if sep_raw_input[0] in curr_check:
            if sep_raw_input[1] in curr_check:
                if sep_raw_input[1] != sep_raw_input[0]:
                    if isinstance(int(sep_raw_input[2]), int):
                        currencies[0] = sep_raw_input[0]
                        currencies[1] = sep_raw_input[1]
                        currencies[2] = sep_raw_input[2]
                        format_correct = True
                    else:
                        bot.send_message(message.chat.id, 'Количество должно быть числом')
                else:
                    bot.send_message(message.chat.id, 'Введены одинаковые валюты')
            else:
                bot.send_message(message.chat.id, 'Опечатка')
        else:
            bot.send_message(message.chat.id, 'Опечатка')
    else:
        bot.send_message(message.chat.id, 'Должно быть 3 параметра')

    if format_correct:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={currencies[1]}&from={currencies[0]}&amount={currencies[2]}"
        headers= {"apikey": "QI9Nc50kmTTE4xubAKJPqSUVA7FX4WpA"}
        response = requests.request("GET", url, headers=headers)
        result = str(json.loads(response.content))
        result = result.split()
        end_res = result[-1].replace('}', '')
        bot.send_message(message.chat.id, f'{currencies[2]} {currencies[0]} = {end_res} {currencies[1]}')
bot.polling()

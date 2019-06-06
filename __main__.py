from __future__ import print_function, division
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import os
import time
import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint
import apiai, json
TOKEN = os.environ["TOKEN"]
API_TOKEN = os.environ["API_TOKEN"]

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

def get_gif():
    GIF_TOKEN = os.environ["GIF_TOKEN"]
    api_instance = giphy_client.DefaultApi()
    api_key = GIF_TOKEN
    tag = 'fail'
    rating = 'g'
    fmt = 'json'
    try:
        api_response = api_instance.gifs_random_get(api_key, tag=tag, rating=rating, fmt=fmt)
        pprint(api_response.data.image_url)
        return api_response.data.image_url
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_random_get: %s\n" % e)

def send_gif(bot, update):
    ares = get_gif()
    print(ares)
    bot.send_animation(chat_id = update.message.chat_id, animation=ares.replace("'", ""))


def send_weather(bot, update):
    from Weather2 import weather_func
    bot.send_message(chat_id=update.message.chat_id, text='Отправь мне название города, погоду в котором ты хочешь узнать!')
    bot.send_photo(chat_id=update.message.chat_id, photo=weather_func(textMessage(bot, update))[1])
    bot.send_message(chat_id=update.message.chat_id, text=weather_func(textMessage(bot, update))[0])
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Тебя приветствует PocketBuddy, твой карманный помошник и личный Telegram-проводник! \nОзнакомиться с доступными функциями ты сможешь, отправив /functions')
def functionCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Список функций: \n/gif - Команда, которая поднимет тебе настроение!")
def textMessage(bot, update):
    request = apiai.ApiAI(API_TOKEN).text_request()
    request.lang = 'ru'
    request.session_id = 'RUPB_bot'
    request.query = update.message.text
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']

    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
        return update.message.text
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Что ты сказал?')
        return update.message.text

function_Command_handler = CommandHandler('functions', functionCommand)
weather_command_handler = CommandHandler('weather', send_weather)
start_command_handler = CommandHandler('start', startCommand)
gif_command_handler = CommandHandler('gif', send_gif)
text_message_handler = MessageHandler(Filters.text, textMessage)
dispatcher.add_handler(function_Command_handler)
dispatcher.add_handler(gif_command_handler)
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(weather_command_handler)
dispatcher.add_handler(text_message_handler)

updater.start_polling(clean=True)

updater.idle()


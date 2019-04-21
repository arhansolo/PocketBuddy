import telebot
import apiai, json
import time
import os
TOKEN = os.environ["TOKEN"]
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Приветствую тебя, странник!")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    API_TOKEN = os.environ["API_TOKEN"]
    request = apiai.ApiAI(API_TOKEN).text_request()
    request.lang = 'ru'
    request.session_id = "RUPB_bot"
    request.query = bot.message_handler(message.text)
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!')




bot.polling(none_stop=True)
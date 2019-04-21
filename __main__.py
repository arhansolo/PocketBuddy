import telebot
import time
import os
TOKEN = os.environ["TOKEN"]
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Приветствую тебя, странник!")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.polling(none_stop=True)
import os

import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot("1892091599:AAH2J2nudTs0xffaZbR_4beAuu_3jNZWRK4")


@bot.callback_query_handler(func=lambda call: "id_azione_1" == call.data)
def azione1(message):
    print(message)
    bot.send_message(message.message.chat.id, "Hai tappato l'azione 1")


@bot.callback_query_handler(func=lambda call: "id_azione_2" == call.data)
def azione2(message):
    print(message)
    bot.send_message(message.message.chat.id, "Hai tappato l'azione 2")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['keyboard'])
def keyboard(message):
    markup = ReplyKeyboardMarkup(row_width=2)
    itembtn1 = KeyboardButton('Angelo')
    itembtn2 = KeyboardButton('Carlo')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Come mi chiamo io che sto parlando?", reply_markup=markup)


@bot.message_handler(func=lambda m: "python" in m.text)
def fun2(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Azione 1", callback_data="id_azione_1"),
               InlineKeyboardButton("Azione 2", callback_data="id_azione_2"))

    bot.send_message(message.chat.id, "CIAO RAGAZZI", reply_markup=markup)


@bot.message_handler(func=lambda m: "py" in m.text)
def fun3(message):
    bot.reply_to(message, "Cijhdfbjkbskjfdb")


@bot.message_handler(func=lambda m: True)
def fun_generale(message):
    if "Angelo" in message.text:
        bot.reply_to(message, "Si mi chiamo Angelo")
    else:
        bot.reply_to(message, "No, non mi chiamo cosi")


if __name__ == '__main__':
    bot.polling()

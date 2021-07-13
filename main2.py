import os

import telebot
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot("1892091599:AAH2J2nudTs0xffaZbR_4beAuu_3jNZWRK4")

"""
This will handle all the callback input
"""
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "1":
            keyboard = types.InlineKeyboardMarkup(row_width=3)
            a = types.InlineKeyboardButton(text=" ", callback_data="2")
            b = types.InlineKeyboardButton(text=" ", callback_data="2")
            c = types.InlineKeyboardButton(text=" ", callback_data="2")
            d = types.InlineKeyboardButton(text=" ", callback_data="2")
            e = types.InlineKeyboardButton(text=" ", callback_data="2")
            f = types.InlineKeyboardButton(text=" ", callback_data="2")
            g = types.InlineKeyboardButton(text=" ", callback_data="2")
            h = types.InlineKeyboardButton(text=" ", callback_data="2")
            i = types.InlineKeyboardButton(text=" ", callback_data="2")
            keyboard.add(a, b, c, d, e, f, g, h, i)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="X", reply_markup=keyboard)
        if call.data == "2":
            keyboard = types.InlineKeyboardMarkup(row_width=3)
            a = types.InlineKeyboardButton(text="X", callback_data="3")
            b = types.InlineKeyboardButton(text=" ", callback_data="3")
            c = types.InlineKeyboardButton(text=" ", callback_data="3")
            d = types.InlineKeyboardButton(text=" ", callback_data="3")
            e = types.InlineKeyboardButton(text=" ", callback_data="3")
            f = types.InlineKeyboardButton(text=" ", callback_data="3")
            g = types.InlineKeyboardButton(text=" ", callback_data="3")
            h = types.InlineKeyboardButton(text=" ", callback_data="3")
            i = types.InlineKeyboardButton(text=" ", callback_data="3")
            keyboard.add(a, b, c, d, e, f, g, h, i)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="0", reply_markup=keyboard)
        if call.data == "3":
            keyboard = types.InlineKeyboardMarkup(row_width=3)
            a = types.InlineKeyboardButton(text=" ", callback_data="1")
            b = types.InlineKeyboardButton(text=" ", callback_data="1")
            c = types.InlineKeyboardButton(text=" ", callback_data="1")
            d = types.InlineKeyboardButton(text=" ", callback_data="1")
            e = types.InlineKeyboardButton(text="0", callback_data="1")
            f = types.InlineKeyboardButton(text=" ", callback_data="1")
            g = types.InlineKeyboardButton(text=" ", callback_data="1")
            h = types.InlineKeyboardButton(text=" ", callback_data="1")
            i = types.InlineKeyboardButton(text=" ", callback_data="1")
            keyboard.add(a, b, c, d, e, f, g, h, i)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="X", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: "id_azione_1" == call.data)
def azione1(message):
    #print(message)
    bot.send_message(message.message.chat.id, "Hai tappato l'azione 1")


@bot.callback_query_handler(func=lambda call: "id_azione_2" == call.data)
def azione2(message):
    #print(message)
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


@bot.message_handler(commands=['try'])#func=lambda m: "python" in m.text)
def fun2(message):
    print("Sei dentro")
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Azione 1", callback_data="1"),
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

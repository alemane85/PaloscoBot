import os
import telebot
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import MyCsv

bot = telebot.TeleBot("1892091599:AAH2J2nudTs0xffaZbR_4beAuu_3jNZWRK4")
art_lastrine= MyCsv.MyCsvFile()
art_lastrine.load(f"{os.path.dirname(os.path.realpath(__file__))}\data\ART-LASTRINA.txt")
art_lastrine.Create_dictionary()
print(art_lastrine)

"""
MESSAGGIO INIZIALE ATTIVATO DA /start
"""
@bot.message_handler(commands=['start'])
def cut_routine_start(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button_list=[]
    print(art_lastrine.dict_filter['COLORE'])
    for element in art_lastrine.dict_filter['COLORE']:
        print(element)
        keyboard.add(types.InlineKeyboardButton(text=element, callback_data=element))
    #a = types.InlineKeyboardButton(text="MESCOLA ", callback_data="MESCOLA")
    #b = types.InlineKeyboardButton(text="LASTRA", callback_data="LASTRA")
    #c = types.InlineKeyboardButton(text="LASTRINA", callback_data="LASTRINA")
    name = message.from_user.username
    bot.send_message(chat_id=message.chat.id, text=f"Ciao {name} Cosa hai prodotto?",reply_markup=keyboard)

"""
MESSAGGIO DI HELP ATTIVATO DA /help
"""
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Help in fase di costruzione")



"""
GESTIONE DI TUTTE LE CALLBACK GENRATE DALLA PRESSIONE DI UN TASTO SULLA
InlineKeyboardMarkup
"""
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        call_list=call.data.split('-')
        for call_element in call_list:
            pass
        if call.data == "LASTRINA":
            keyboard = types.InlineKeyboardMarkup(row_width=3)
            a = types.InlineKeyboardButton(text="160", callback_data="160")
            b = types.InlineKeyboardButton(text="200", callback_data="200")
            c = types.InlineKeyboardButton(text="250", callback_data="250")
            d = types.InlineKeyboardButton(text="300", callback_data="300")
            e = types.InlineKeyboardButton(text="350", callback_data="350")
            f = types.InlineKeyboardButton(text="400", callback_data="400")
            keyboard.add(a, b, c, d, e, f)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="DENSITA' MESCOLA?", reply_markup=keyboard)
        if call.data == "160":
            keyboard = types.InlineKeyboardMarkup(row_width=3)
            a = types.InlineKeyboardButton(text="FF", callback_data="3")
            b = types.InlineKeyboardButton(text="F", callback_data="3")
            c = types.InlineKeyboardButton(text="MF", callback_data="3")
            d = types.InlineKeyboardButton(text="M", callback_data="3")
            e = types.InlineKeyboardButton(text="MG", callback_data="3")
            f = types.InlineKeyboardButton(text="G", callback_data="3")
            keyboard.add(a, b, c, d, e, f)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="POROSITA' MESCOLA?", reply_markup=keyboard)
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

"""
COMMENTATO PERCHE' NON UTLIZZATO

@bot.callback_query_handler(func=lambda call: "id_azione_1" == call.data)
def azione1(message):
    #print(message)
    bot.send_message(message.message.chat.id, "Hai tappato l'azione 1")


@bot.callback_query_handler(func=lambda call: "id_azione_2" == call.data)
def azione2(message):
    #print(message)
    bot.send_message(message.message.chat.id, "Hai tappato l'azione 2")

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
"""

if __name__ == '__main__':
    bot.polling()
    print("BOT PARTITO")

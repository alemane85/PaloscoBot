import os
import telebot
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import MyCsv
from datetime import datetime

bot = telebot.TeleBot("1892091599:AAH2J2nudTs0xffaZbR_4beAuu_3jNZWRK4")
cutting_file= MyCsv.MyCsvFile()
cutting_file.load(f"{os.path.dirname(os.path.realpath(__file__))}\data\ART-LASTRINA.txt")
all_data=""
print(all_data)
"""
MESSAGGIO INIZIALE ATTIVATO DA /start
"""
@bot.message_handler(commands=['start'])
def start(message):
    global all_data
    all_data=""
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text='MESCOLA', callback_data='PRODOTTO=MESCOLA'))
    keyboard.add(types.InlineKeyboardButton(text='TAGLIO', callback_data='PRODOTTO=TAGLIO'))
    name = message.from_user.username
    bot.send_message(chat_id=message.chat.id, text=f"Ciao {name} Cosa hai prodotto?",reply_markup=keyboard)

"""
MESSAGGIO DI HELP ATTIVATO DA /help
"""
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Help in fase di costruzione")

def callback_to_dictionary(data):
    dictionary={}
    call_list=data.split('-')
    for element in call_list:
        duo=element.split('=')
        dictionary[duo[0]]=duo[1]

    return dictionary

def next_value(call,tab,selection):
    name = call.from_user.username
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    """stampa a console input dell'utente con data e ora"""
    print(f"{time} | User: {name} -> {all_data}")
    """Ricorda nel messaggio le selezioni effettuate"""
    msg_text="Hai selezionato:\n"
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    filtered_tab=tab
    filter_key=0
    for key in selection.keys():
        if not selection[key]=="[0]":
            msg_text+=f"{key} = {selection[key]}\n"
            filtered_tab=filtered_tab.filter_by(key,selection[key])
        else:
            filter_key=key
    for element in filtered_tab.dict_filter[filter_key]:
        duo=call.data.split("=[0]")
        callback_text=f"{duo[0]}={element}"
        keyboard.add(types.InlineKeyboardButton(text=element, callback_data=callback_text))
    msg_text+=f"{name} ora seleziona un valore per {filter_key}:"
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg_text,reply_markup=keyboard)

def next_filter(call,tab,selection):
    name = call.from_user.username
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    """stampa a console input dell'utente con data e ora"""
    print(f"{time} | User: {name} -> {all_data}")
    """Ricorda nel messaggio le selezioni effettuate"""
    msg_text="Hai selezionato:\n"
    filtered_tab=tab
    for key in selection.keys():
        msg_text+=f"{key} = {selection[key]}\n"
        filtered_tab=filtered_tab.filter_by(key,selection[key])
    if filtered_tab.rows_number()==1:
        print("abbiamo finito mi sa!")
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for element in tab.dictionary.keys():
        if not element in selection.keys():
                callback_text=f"-{element}=[0]"
                print(callback_text)
                keyboard.add(types.InlineKeyboardButton(text=element, callback_data=callback_text))
    msg_text+=f"{name} ora filtra per:"
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg_text,reply_markup=keyboard)

def dictionary_to_callback(selection):
    new_string=""
    lastkey=list(selection.keys())[-1]
    for key in selection.keys():
        if key==lastkey:
            new_string+=f"{key}={selection[key]}"
        else:
            new_string+=f"{key}={selection[key]}-"
    return new_string
"""
GESTIONE DI TUTTE LE CALLBACK GENRATE DALLA PRESSIONE DI UN TASTO SULLA
InlineKeyboardMarkup
"""
@bot.callback_query_handler(func=lambda call: True)
def routine(call):
    global all_data
    all_data+=call.data
    """Crea dizionario sulla base di quanto selezionato"""
    selection=callback_to_dictionary(all_data)
    all_data=dictionary_to_callback(selection)
    print("selection")
    print(selection)
    print("all_data")
    print(all_data)
    if selection["PRODOTTO"]=="TAGLIO":
        lastkey=list(selection.keys())[-1]
        if selection[lastkey]=="[0]":
            next_value(call,cutting_file.tab,selection)
        else:
            next_filter(call,cutting_file.tab,selection)

if __name__ == '__main__':
    print("BOT PARTITO")
    bot.polling()

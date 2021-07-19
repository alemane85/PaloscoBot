import os
import telebot
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import MyCsv
from datetime import datetime

"""VARIABILI GLOBALI"""
bot = telebot.TeleBot("1892091599:AAH2J2nudTs0xffaZbR_4beAuu_3jNZWRK4")
cutting_file= MyCsv.MyCsvFile()
cutting_file.load(f"{os.path.dirname(os.path.realpath(__file__))}\data\ART-LASTRINA.txt")
all_data=""

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
    keyboard = types.InlineKeyboardMarkup()
    filtered_tab=tab
    filter_key=0
    for key in selection.keys():
        if not selection[key]=="[0]":
            msg_text+=f"{key} = {selection[key]}\n"
            filtered_tab=filtered_tab.filter_by(key,selection[key])
        else:
            filter_key=key
    counter=0
    button_list=[]
    for element in filtered_tab.dict_filter[filter_key]:
        duo=call.data.split("=[0]")
        callback_text=f"{duo[0]}={element}"
        button_list.append(types.InlineKeyboardButton(text=element, callback_data=callback_text))
        counter+=1
    if (counter%2)==0:
        for i in range(0,counter-1,2):
            keyboard.add(button_list[i],button_list[i+1])
    else:
        for i in range(0,counter-2,2):
            keyboard.add(button_list[i],button_list[i+1])
        keyboard.add(button_list[counter-1])
    keyboard.add(types.InlineKeyboardButton(text="↪️INDIETRO", callback_data="[BACK]"))
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
    """Se dopo i filtri applicati la nuova tabella ha un solo elemento
    passiamo a definire la quantità"""
    if filtered_tab.rows_number()==1:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(text="✅ CONFERMA", callback_data="QUANTITA=0"))
        keyboard.add(types.InlineKeyboardButton(text="↪️ INDIETRO", callback_data="[BACK]"))
        art=""
        for key in filtered_tab.dictionary.keys():
            art+=f"{key}: {filtered_tab.dictionary[key][0]}\n"
        msg_text=f"Ho trovato il seguente Articolo:\n\n{art}\n- ✅ CONFERMA per inserire la quantità\n- ↪️ INDIETRO per modificare"
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for element in tab.dictionary.keys():
            if not element in selection.keys():
                num_filtri=len(list(filtered_tab.dict_filter[element]))
                if not num_filtri==1:
                    callback_text=f"-{element}=[0]"
                    keyboard.add(types.InlineKeyboardButton(text=f"{element}- {num_filtri} voci", callback_data=callback_text))
        keyboard.add(types.InlineKeyboardButton(text="↪️INDIETRO", callback_data="[BACK]"))
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

def go_back(data):
    list=data.split("-")
    del list[-1]
    string="-".join(list)
    return string

def quantity_menu(call):
    name = call.from_user.username
    duo=call.data.split("=")
    value=int(duo[1])
    keyboard = types.InlineKeyboardMarkup()
    button_list=[]
    button_list.append(types.InlineKeyboardButton(text='-1', callback_data=f"{duo[0]}={str(value-1)}"))
    button_list.append(types.InlineKeyboardButton(text='+1', callback_data=f"{duo[0]}={str(value+1)}"))
    keyboard.add(button_list[0],button_list[1])
    button_list=[]
    button_list.append(types.InlineKeyboardButton(text='-5', callback_data=f"{duo[0]}={str(value-5)}"))
    button_list.append(types.InlineKeyboardButton(text='+5', callback_data=f"{duo[0]}={str(value+5)}"))
    keyboard.add(button_list[0],button_list[1])
    button_list=[]
    button_list.append(types.InlineKeyboardButton(text='-10', callback_data=f"{duo[0]}={str(value-10)}"))
    button_list.append(types.InlineKeyboardButton(text='+10', callback_data=f"{duo[0]}={str(value+10)}"))
    keyboard.add(button_list[0],button_list[1])
    button_list=[]
    button_list.append(types.InlineKeyboardButton(text='-50', callback_data=f"{duo[0]}={str(value-50)}"))
    button_list.append(types.InlineKeyboardButton(text='+50', callback_data=f"{duo[0]}={str(value+50)}"))
    keyboard.add(button_list[0],button_list[1])
    button_list=[]
    button_list.append(types.InlineKeyboardButton(text='-100', callback_data=f"{duo[0]}={str(value-100)}"))
    button_list.append(types.InlineKeyboardButton(text='+100', callback_data=f"{duo[0]}={str(value+100)}"))
    keyboard.add(button_list[0],button_list[1])
    button_list=[]
    button_list.append(types.InlineKeyboardButton(text='-500', callback_data=f"{duo[0]}={str(value-500)}"))
    button_list.append(types.InlineKeyboardButton(text='+500', callback_data=f"{duo[0]}={str(value+500)}"))
    keyboard.add(button_list[0],button_list[1])
    keyboard.add(types.InlineKeyboardButton(text="✅ CONFERMA", callback_data=f"CONFERMATO={str(value)}"))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Ciao {name} hai prodotto: {str(value)}",reply_markup=keyboard)

"""
GESTIONE DI TUTTE LE CALLBACK GENERATE DALLA PRESSIONE DI UN TASTO SULLA
InlineKeyboardMarkup
"""
@bot.callback_query_handler(func=lambda call: True)
def routine(call):
    global all_data
    name = call.from_user.username
    """Se la callback contiene QUANTITA allora passiamo al menu di selezione della stessa"""
    if "QUANTITA" in call.data:
        quantity_menu(call)
        return
    """Se la callback contiene [BACK] allora si torna indietro di uno step"""
    if call.data=="[BACK]":
        all_data=go_back(all_data)
        """Se la callback contiene [BACK] e perdiamo tutti i dati filtrati allora torniamo al menu principale"""
        if all_data=="":
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text='MESCOLA', callback_data='PRODOTTO=MESCOLA'))
            keyboard.add(types.InlineKeyboardButton(text='TAGLIO', callback_data='PRODOTTO=TAGLIO'))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Ciao {name} Cosa hai prodotto?",reply_markup=keyboard)
            return
    else:
        all_data+=call.data
    """Crea dizionario sulla base di quanto selezionato"""
    selection=callback_to_dictionary(all_data)
    """Normalizziamo la stringa di all_data togliendo le selezioni di soli filtri"""
    all_data=dictionary_to_callback(selection)
    """Se siamo nella selezione di un prodotto di taglio"""
    if selection["PRODOTTO"]=="TAGLIO":
        lastkey=list(selection.keys())[-1]
        """In base all'ultima selezione decidiamo se fornire un menu di nuovi filtri o di selezione valori"""
        if selection[lastkey]=="[0]":
            next_value(call,cutting_file.tab,selection)
        else:
            next_filter(call,cutting_file.tab,selection)

if __name__ == '__main__':
    print("BOT PARTITO")
    bot.polling()

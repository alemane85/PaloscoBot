from flask import Flask,request
import telebot
import threading
from time import sleep
import os
import art
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime
from MyRoutine import MyRoutine
from MyRoutine import MyCutRoutine
from colorama import Fore,init,Style
from pyngrok import ngrok
import logging

# Open a HTTP tunnel on the default port 80
# <NgrokTunnel: "http://<public_sub>.ngrok.io" -> "http://localhost:80">
https_tunnel = str(ngrok.connect("5000",bind_tls=True)).split('"')[1]

bot = telebot.TeleBot("1892091599:AAH2J2nudTs0xffaZbR_4beAuu_3jNZWRK4")
bot.set_webhook(url=https_tunnel)
app=Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app.logger.disabled = True
log.disabled = True


routines=[]
in_cut_file=f"{os.path.dirname(os.path.realpath(__file__))}\data\TAGLI2.txt"
out_cut_file=f"{os.path.dirname(os.path.realpath(__file__))}\data\TAGLI_DA_BOLLARE2.txt"


@app.route('/', methods=["POST"])
def webhook():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "ok"

@bot.message_handler(commands=['start'])
def command_start(message):
    print("\n")
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text='MESCOLA', callback_data='PRODOTTO=MESCOLA'))
    keyboard.add(types.InlineKeyboardButton(text='TAGLIO', callback_data='PRODOTTO=TAGLIO'))
    name = message.from_user.username
    bot.send_message(chat_id=message.chat.id, text=f"Ciao {name} Cosa hai prodotto?",reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def call_routine(call):
    if call.data=='PRODOTTO=TAGLIO':
        exist=False
        for routine in routines:
            #SCORRO TUTTE LE ROUTINE GIA APERTE
            if routine.username==call.from_user.username:
                #SE GIA' APERTA ROUTINE CON QUEL NOME ALLORA RICOMINCIO LA ROUTINE E INTERROMPO IL CICLO
                routine.reset()
                time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                print(f"{Fore.YELLOW}{Style.BRIGHT}{time} | {routine.username} -> SESSION RESTART {routine.selection}")
                exist=True
                break
        if not exist:
            routines.append(MyCutRoutine(call.from_user.username,in_cut_file,out_cut_file))
            time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"{Fore.YELLOW}{Style.BRIGHT}{time} | {call.from_user.username} -> SESSION CREATED")
    for routine in routines:
        #SCORRO TUTTE LE ROUTINE GIA APERTE
        if routine.username==call.from_user.username:
            #SE GIA' APERTA ROUTINE CON QUEL NOME ALLORA LE AFFIDO LA CALL E INTERROMPO IL CICLO
            routine.handle_call(call,bot)
            break


logo=art.text2art("PaloscoBot 2.0",font='graffiti')
separator=f"{Fore.YELLOW}{Style.BRIGHT}\n****************************************************************************************************\n"
print(separator)
print(f"{Fore.CYAN}{Style.BRIGHT}{logo}")
print(separator)
time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
print(f"{Fore.YELLOW}{Style.BRIGHT}{time} | BOT WEBHOOK -> {https_tunnel}\n{Fore.RESET}{Style.RESET_ALL}")

if __name__ == "__main__":
    app.run()

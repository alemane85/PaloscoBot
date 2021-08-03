# FLASK IMPORTS
from flask import Flask,request

# NGROK IMPORTS
from pyngrok import ngrok,conf

# TELEGRAM BOT IMPORTS
import telebot
from telebot import types,apihelper
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

# MISCELLANEUS IMPORTS
import os
import art
from sys import exit
from colorama import Fore,init,Style
import logging
from datetime import datetime
import sys
from os.path import dirname

# SETTING DB AND LIB PATH
upper_path=f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}"
mydb_path=f"{upper_path}/db"
mylib_path=f"{upper_path}/lib"

# ADD MY LIB DIR TO PYTHON PATH SYSTEM
sys.path.append(mylib_path)

# MY OWN MODULE IMPORTS
from MyRoutine import MyRoutine
from MyRoutine import MyCutRoutine

# READ CONFIG FILE
cfg_path=f"{upper_path}/config.txt"
with open(cfg_path,"r") as cfg_file:
    cfg_rows=cfg_file.readlines()
    pwd=cfg_rows[0].split('=')[1].rstrip("\n")
    if pwd != "ok":
        exit()
    bot_token=cfg_rows[1].split('=')[1].rstrip("\n")
    ngrok_token=cfg_rows[2].split('=')[1].rstrip("\n")


# NGROK CONFIG
# SET REGION EU
conf.get_default().region = "eu"
# SET TOKEN
ngrok.set_auth_token(ngrok_token)
# OPEN NGROK HTTPS TUNNEL ON PORT 80
https_tunnel = str(ngrok.connect("80",bind_tls=True)).split('"')[1]
https_tunnel+="/PaloscoBot"

# TELEBOT CONFIG
# NEW BOT WITH TOKEN
bot = telebot.TeleBot(bot_token)
# SET TIME TO LIVE TO 5 MIN TO PREVENT TELEGRAM KICK OF THE BOT
apihelper.SESSION_TIME_TO_LIVE=300
# SET WEBHOOK TO THE NGROK HTTPS TUNNEL
bot.set_webhook(url=https_tunnel)
# TELEBOT LOGGER ENABLED BY UNCOMMENTING THIS 2 LINES
#telebot_logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

# FLASK CONFIG
app=Flask(__name__)
# DISABLE FLASK LOGGER - COMMENT THIS LINES TO ENABLE
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app.logger.disabled = True
log.disabled = True

# COLORAMA ACTIVATE
init()

# SET A EMPTY LIST OF ROUTINES
routines=[]
# SET CUTTING ROUTINES FILES
in_cut_file=f"{mydb_path}/TAGLI.txt"
out_cut_file=f"{mydb_path}/TAGLI_DA_BOLLARE.txt"
# SET MIXING ROUTINES FILES
in_mix_file=f"{mydb_path}/MESCOLE.txt"
out_mix_file=f"{mydb_path}/MESCOLE_DA_BOLLARE.txt"


# RECEIVE POST DATA IN JSON FORMAT AND GIVE IT TO THE BOT TO HANDLE
@app.route('/PaloscoBot', methods=["POST"])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        #print("\nIL BOT HA PROCESSATO I NUOVI MESSAGGI\n")
        return 'ok'
    else:
        flask.abort(403)

#HANDLE /START COMMAND
@bot.message_handler(commands=['start'])
def command_start(message):
    #print("\nCOMMAND START\n")
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text='MESCOLA', callback_data='PRODOTTO=MESCOLA'))
    keyboard.add(types.InlineKeyboardButton(text='TAGLIO', callback_data='PRODOTTO=TAGLIO'))
    name = message.from_user.username
    bot.send_message(chat_id=message.chat.id, text=f"Ciao {name} Cosa hai prodotto?",reply_markup=keyboard)

#HANDLE ANY CALLBACK QUERY
@bot.callback_query_handler(func=lambda call: True)
def call_routine(call):
    #print("\nCALLBACK HANDLER\n")
    #CREATE IF NOT EXIST THE RIGHT ROUTINE TO HANDLE NEW CALLBACK QUERIES FROM THE USER
    #OR RESET AN EXISTING ONE
    if call.data=='PRODOTTO=TAGLIO':
        exist=False
        for routine in routines:
            if routine.username==call.from_user.username:
                routine.reset()
                time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                print(f"{Fore.YELLOW}{Style.BRIGHT}{time} | {routine.username} -> SESSION RESTART {routine.selection}")
                exist=True
                break
        if not exist:
            routines.append(MyCutRoutine(call.from_user.username,in_cut_file,out_cut_file))
            time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"{Fore.YELLOW}{Style.BRIGHT}{time} | {call.from_user.username} -> SESSION CREATED")
    if call.data=='PRODOTTO=MESCOLA':
        exist=False
        for routine in routines:
            if routine.username==call.from_user.username:
                routine.reset()
                time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                print(f"{Fore.YELLOW}{Style.BRIGHT}{time} | {routine.username} -> SESSION RESTART {routine.selection}")
                exist=True
                break
        if not exist:
            routines.append(MyCutRoutine(call.from_user.username,in_cut_file,out_cut_file))
            time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"{Fore.YELLOW}{Style.BRIGHT}{time} | {call.from_user.username} -> SESSION CREATED")
    #THEN HANDLE THE CALLBACK QUERY TO THE RIGHT ROUTINE
    for routine in routines:
        if routine.username==call.from_user.username:
            routine.handle_call(call,bot)
            break
    #ANSWER THE QUERY WITH A VOID ANSWER TO LET TELEGRAM WORKING GOOD
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    #PRINT TO CHECK IF WE ANSWER TO EVERY CALLBACK
    print(f"{Fore.YELLOW}{Style.BRIGHT}{time} | BOT answer_callack_query -> {call.id}")
    bot.answer_callack_query(call.id)

#CREATE THE APP LOGO ON CONSOLE
logo=art.text2art("PaloscoBot 2.0",font='graffiti')
separator=f"{Fore.YELLOW}{Style.BRIGHT}\n****************************************************************************************************\n"
print(separator)
print(f"{Fore.CYAN}{Style.BRIGHT}{logo}")
print(separator)
time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
print(f"{Fore.YELLOW}{Style.BRIGHT}{time} | BOT WEBHOOK -> {https_tunnel}\n{Fore.RESET}{Style.RESET_ALL}")

if __name__ == "__main__":
    app.run(port=80)

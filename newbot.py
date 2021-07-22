"""
This is how I run my new bots created with pyTelegramBotAPI to avoid API errors,
like timeout errors or whenever my server can't reach Telegram servers (i.e. if net is down).
A while loop restarts the polling when it's ended due to an error.
A new bot object is created in each new loop execution, to avoid some errors.
We set all our message handlers in botactions() so the new bot object can use them.
Threading is not needed, but I prefer running the while True loop threaded so I can stop the bot
anytime with Ctrl+C, otherwise it can't be stopped easily. Killing the script is not nice and
I use databases in some bots, which should be closed beforehand.
"""

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



BOT_TOKEN = "1892091599:AAH2J2nudTs0xffaZbR_4beAuu_3jNZWRK4"
BOT_INTERVAL = 1
BOT_TIMEOUT = 5
routines=[]
in_cut_file=f"{os.path.dirname(os.path.realpath(__file__))}\data\TAGLI2.txt"
out_cut_file=f"{os.path.dirname(os.path.realpath(__file__))}\data\TAGLI_DA_BOLLARE2.txt"

#bot = None #Keep the bot object as global variable if needed

def bot_polling():
    #global bot #Keep the bot object as global variable if needed
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"{Fore.RED}{Style.BRIGHT}{time} | BOT -> POLLING STARTED")
    while True:
        try:
            time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"{Fore.RED}{Style.BRIGHT}{time} | BOT -> NEW ISTANCE STARTED")
            bot = telebot.TeleBot(BOT_TOKEN) #Generate new bot instance
            botactions(bot) #If bot is used as a global variable, remove bot as an input param
            bot.polling(none_stop=True, interval=BOT_INTERVAL, timeout=BOT_TIMEOUT)
        except Exception as ex: #Error in polling
            time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"{Fore.RED}{Style.BRIGHT}{time} | BOT -> ERROR: {ex}")
            print(f"{Fore.RED}{Style.BRIGHT}{time} | BOT -> POLLING FAILED")
            print(f"{Fore.RED}{Style.BRIGHT}{time} | BOT -> RESTART IN {BOT_TIMEOUT} SECONDS")
            bot.stop_polling()
            sleep(BOT_TIMEOUT)
        else: #Clean exit
            bot.stop_polling()
            time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"{Fore.RED}{Style.BRIGHT}{time} | BOT -> STOPPED")
            break #End loop


def botactions(bot):
    #Set all your bot handlers inside this function
    #If bot is used as a global variable, remove bot as an input param
    @bot.message_handler(commands=['start'])
    def command_start(message):
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
polling_thread = threading.Thread(target=bot_polling)
polling_thread.daemon = True
polling_thread.start()


#Keep main program running while bot runs threaded
if __name__ == "__main__":
    while True:
        try:
            sleep(120)
        except KeyboardInterrupt:
            break

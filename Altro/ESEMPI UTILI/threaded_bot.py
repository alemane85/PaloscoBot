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

BOT_TOKEN = ""
BOT_INTERVAL = 3
BOT_TIMEOUT = 30

#bot = None #Keep the bot object as global variable if needed

def bot_polling():
    #global bot #Keep the bot object as global variable if needed
    print("Starting bot polling now")
    while True:
        try:
            print("New bot instance started")
            bot = telebot.TeleBot(BOT_TOKEN) #Generate new bot instance
            botactions(bot) #If bot is used as a global variable, remove bot as an input param
            bot.polling(none_stop=True, interval=BOT_INTERVAL, timeout=BOT_TIMEOUT)
        except Exception as ex: #Error in polling
            print("Bot polling failed, restarting in {}sec. Error:\n{}".format(BOT_TIMEOUT, ex))
            bot.stop_polling()
            sleep(BOT_TIMEOUT)
        else: #Clean exit
            bot.stop_polling()
            print("Bot polling loop finished")
            break #End loop


def botactions(bot):
    #Set all your bot handlers inside this function
    #If bot is used as a global variable, remove bot as an input param
    @bot.message_handler(commands=["start"])
    def command_start(message):
        bot.reply_to(message, "Hi there!")


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
telebot_polling_template_GlobalBot.py
"""
This version is threaded, but the "bot" object is set as a global variable.
"""

import telebot
import threading
from time import sleep

BOT_TOKEN = ""
BOT_INTERVAL = 3
BOT_TIMEOUT = 30

bot = None

def bot_polling():
    global bot
    print("Starting bot polling now")
    while True:
        try:
            print("New bot instance started")
            bot = telebot.TeleBot(BOT_TOKEN) #Generate new bot instance
            botactions() #If bot is used as a global variable, remove bot as an input param
            bot.polling(none_stop=True, interval=BOT_INTERVAL, timeout=BOT_TIMEOUT)
        except Exception as ex: #Error in polling
            print("Bot polling failed, restarting in {}sec. Error:\n{}".format(BOT_TIMEOUT, ex))
            bot.stop_polling()
            sleep(BOT_TIMEOUT)
        else: #Clean exit
            bot.stop_polling()
            print("Bot polling loop finished")
            break #End loop


def botactions():
    #Set all your bot handlers inside this function
    #If bot is used as a global variable, remove bot as an input param
    @bot.message_handler(commands=["start"])
    def command_start(message):
        bot.reply_to(message, "Hi there!")


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
telebot_polling_template_NonThreaded.py
"""
This version is not threaded, however Haven't tried it.
"""

import telebot
from time import sleep

BOT_TOKEN = ""
BOT_INTERVAL = 3
BOT_TIMEOUT = 30

#bot = None #Keep the bot object as global variable if needed

def bot_polling():
    #global bot #Keep the bot object as global variable if needed
    print("Starting bot polling now")
    while True:
        try:
            print("New bot instance started")
            bot = telebot.TeleBot(BOT_TOKEN) #Generate new bot instance
            botactions(bot) #If bot is used as a global variable, remove bot as an input param
            bot.polling(none_stop=True, interval=BOT_INTERVAL, timeout=BOT_TIMEOUT)
        except Exception as ex: #Error in polling
            print("Bot polling failed, restarting in {}sec. Error:\n{}".format(BOT_TIMEOUT, ex))
            bot.stop_polling()
            sleep(BOT_TIMEOUT)
        else: #Clean exit
            bot.stop_polling()
            print("Bot polling loop finished")
            break #End loop


def botactions(bot):
    #Set all your bot handlers inside this function
    #If bot is used as a global variable, remove bot as an input param
    @bot.message_handler(commands=["start"])
    def command_start(message):
        bot.reply_to(message, "Hi there!")


bot_polling()

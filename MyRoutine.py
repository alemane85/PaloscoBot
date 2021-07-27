from MyTab import MyTab
from MyCsv import MyCsvFile
from datetime import datetime
from colorama import Fore,init,Style
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import os

#ALMOST VOID CLASS TO INHERIT
class MyRoutine():

    #Inizializzazione di tutte le variabili di classe
    def __init__(self,username,source_file,output_file):
        self.username=username
        self.verbose=True
        self.reset()
        self.output_file=output_file
        self.source_file=source_file
        file=MyCsvFile()
        file.load(source_file)
        self.source_tab=file.tab
        # CHANNEL USED TO LOG THE ADDED ITEM FROM USERS
        self.logging_channel_id="-1001532533639"


    #Reset di tutti gli attributi di classe
    def reset(self):
        self.selection={}
        self.filtered_tab=0
        self.filter_key=0
        self.msg_text=""
        self.error=0


    #Restituisce in forma di stringa una fotografia della classe in quel momento
    #utile in fase di controllo
    def __str__(self):
        string=f"MyRoutine.username={self.username}\n"
        for key in self.selection.keys():
            string+=f"MyRoutine.selection[{key}]={self.selection[key]}\n"
        string+=f"MyRoutine.filtered_tab=\n{self.filtered_tab}\n"
        string+=f"MyRoutine.source_tab=\n{self.source_tab}\n"
        string+=f"MyRoutine.source_file={self.source_file}\n"
        string+=f"MyRoutine.output_file_file={self.output_file}\n"
        string+=f"MyRoutine.error={self.error}"
        return string

class MyCutRoutine(MyRoutine):

    #INIT AND CALL SUPER INIT
    def __init__(self,username,source_file,output_file):
        super().__init__(username,source_file,output_file)
        self.newcut=False
        self.board_list=[1,5,10,50,100,500]
        qfile=MyCsvFile()
        qfile.load(f"{os.path.dirname(os.path.realpath(__file__))}\data\TAGLI_QUANTITA.txt")
        self.quantity_tab=qfile.tab

    #HANDLE QUANTITY PART OF THE ROUTINE
    def quantity_menu(self,bot,call):
        duo=call.data.split("=")
        self.newcut=False
        if "NUOVO"==duo[1]:
            value=0
            self.newcut=True
        else:
            value=int(duo[1])
        time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"{Fore.YELLOW}{Style.BRIGHT}{time} | {self.username} -> {self.selection} -> QUANTITA={duo[1]}")
        i=0
        for element in self.quantity_tab.dictionary["CODICE"]:
            if element==self.filtered_tab.dictionary["CODICE"][0]:
                standard_quantity=self.quantity_tab.dictionary["QUANTITA"][i]
                break
            i+=1
        art=""
        for key in self.filtered_tab.dictionary.keys():
            art+=f"{key}: {self.filtered_tab.dictionary[key][0]}\n"
        self.msg_text=f"Ho trovato il seguente Articolo:\n\n{art}\n- ✅ CONFERMA per memorizzare il taglio\n- ↪️ INDIETRO per modificare\n\n"
        self.msg_text+=f"QUANTITA: {str(value)}"
        keyboard = types.InlineKeyboardMarkup()
        for element in self.board_list:
            button_list=[]
            button_list.append(types.InlineKeyboardButton(text=f"-{element}", callback_data=f"{duo[0]}={str(value-element)}"))
            button_list.append(types.InlineKeyboardButton(text=f"+{element}", callback_data=f"{duo[0]}={str(value+element)}"))
            keyboard.add(button_list[0],button_list[1])
        keyboard.add(types.InlineKeyboardButton(text=f"Numero Standard ➡️ {standard_quantity}", callback_data=f"{duo[0]}={standard_quantity}"))
        keyboard.add(types.InlineKeyboardButton(text="✅ CONFERMA", callback_data=f"TAGLIO_CONFERMATO={str(value)}"))
        keyboard.add(types.InlineKeyboardButton(text="↪️INDIETRO", callback_data="[BACK]"))
        if self.newcut:
            old_msg_text=f"✅ Ho memorizzato il seguente Articolo:\n\n"
            old_msg_text+=f"🔴 CODICE : {self.filtered_tab.dictionary['CODICE'][0]}\n"
            old_msg_text+=f"🔴 QUANTITA: {self.selection['QUANTITA']}"
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=old_msg_text)
            bot.send_message(chat_id=call.message.chat.id,text=self.msg_text,reply_markup=keyboard)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=self.msg_text,reply_markup=keyboard)

    def filter_menu(self,bot,call):
        """Se dopo i filtri applicati la nuova tabella ha un solo elemento
        passiamo a definire la quantità"""
        keyboard = types.InlineKeyboardMarkup()
        if self.filtered_tab.rows_number()==1:
            keyboard.add(types.InlineKeyboardButton(text="✅ CONFERMA", callback_data="QUANTITA=0"))
            keyboard.add(types.InlineKeyboardButton(text="↪️ INDIETRO", callback_data="[BACK]"))
            art=""
            for key in self.filtered_tab.dictionary.keys():
                art+=f"{key}: {self.filtered_tab.dictionary[key][0]}\n"
            self.msg_text=f"Ho trovato il seguente Articolo:\n\n{art}\n- ✅ CONFERMA per inserire la quantità\n- ↪️ INDIETRO per modificare"
        else:
            for element in self.source_tab.dictionary.keys():
                if not element in self.selection.keys():
                    num_filtri=len(list(self.filtered_tab.dict_filter[element]))
                    if not num_filtri==1:
                        callback_text=f"{element}=[0]"
                        keyboard.add(types.InlineKeyboardButton(text=f"{element}- {num_filtri} voci", callback_data=callback_text))
            keyboard.add(types.InlineKeyboardButton(text="↪️INDIETRO", callback_data="[BACK]"))
            self.msg_text+=f"{self.username} ora filtra per:"
        if self.newcut:
            bot.send_message(chat_id=call.message.chat.id,text=self.msg_text,reply_markup=keyboard)
            self.newcut=False
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=self.msg_text,reply_markup=keyboard)

    def evaluate_data(self,call):
        #Ricorda nel messaggio le selezioni effettuate
        self.msg_text="Hai selezionato:\n\n"
        self.filtered_tab=self.source_tab
        for key in self.selection.keys():
            if not self.selection[key]=="[0]":
                self.msg_text+=f"{key} = {self.selection[key]}\n"
                self.filtered_tab=self.filtered_tab.filter_by(key,self.selection[key])
            else:
                self.filter_key=key

    def value_menu(self,bot,call):
        keyboard = types.InlineKeyboardMarkup()
        counter=0
        button_list=[]
        for element in self.filtered_tab.dict_filter[self.filter_key]:
            callback_text=f"{self.filter_key}={element}"
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
        self.msg_text+=f"{self.username} ora seleziona un valore per {self.filter_key}:"
        if self.newcut:
            bot.send_message(chat_id=call.message.chat.id,text=self.msg_text,reply_markup=keyboard)
            self.newcut=False
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=self.msg_text,reply_markup=keyboard)

    def append_line(self,file_name, line):
        with open(file_name, "a+") as file_object:
            supp=f"{line}\n"
            file_object.write(supp)

    def add_selection(self,data):
        duo=data.split('=')
        self.selection[duo[0]]=duo[1]
        return duo[1]

    def modify_selection(self,key,data):
        duo=data.split('=')
        self.selection[key]=duo[1]
        return duo[1]

    def output_data(self,call):
        line=""
        date=datetime.now().strftime("%d/%m/%Y")
        time=datetime.now().strftime("%H:%M:%S")
        quantità=self.modify_selection("QUANTITA",call.data)
        line+=f"{date},"
        line+=f"{time},"
        line+=f"{self.username},"
        line+=f"{quantità},"
        lastkey=list(self.filtered_tab.dictionary.keys())[-1]
        for key in self.filtered_tab.dictionary.keys():
            if key==lastkey:
                line+=f"{self.filtered_tab.dictionary[key][0]}"
            else:
                line+=f"{self.filtered_tab.dictionary[key][0]},"
        self.append_line(self.output_file,line)
        separator=f"{Fore.GREEN}{Style.BRIGHT}**************************************************"
        print(f"\n{separator}\n\nNUOVA VOCE AGGIUNTA AL FILE [{self.output_file}]\n VOCE INSERITA: [{line}]\n\n{separator}\n")

    def output_menu(self,bot,call):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='STESSO TAGLIO -> NUOVA QUANTITA', callback_data=f"QUANTITA=NUOVO"))
        keyboard.add(types.InlineKeyboardButton(text='NUOVO TAGLIO', callback_data='PRODOTTO=NUOVOTAGLIO'))
        art=""
        for key in self.filtered_tab.dictionary.keys():
            art+=f" 🔴 {key}: {self.filtered_tab.dictionary[key][0]}\n"
        self.msg_text=f"✅ Ho memorizzato il seguente Articolo:\n\n{art}\nQUANTITA': {self.selection['QUANTITA']}\n"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=self.msg_text,reply_markup=keyboard)
        channel_text=f"✅ {self.username} ha memorizzato il seguente Articolo:\n\n"
        channel_text+=f" 🔴 CODICE : {self.filtered_tab.dictionary['CODICE'][0]}\n"
        channel_text+=f" 🔴 QUANTITA : {self.selection['QUANTITA']}\n"
        bot.send_message(chat_id=self.logging_channel_id,text=channel_text)
        print(call.message.chat.id)

    def handle_call(self,call,bot):
        if "TAGLIO_CONFERMATO" in call.data:
            self.output_data(call)
            self.output_menu(bot,call)
            return
        if "PRODOTTO=NUOVOTAGLIO"==call.data:
            old_msg_text=f"✅ Ho memorizzato il seguente Articolo:\n\n"
            old_msg_text+=f"🔴 CODICE : {self.filtered_tab.dictionary['CODICE'][0]}\n"
            old_msg_text+=f"🔴 QUANTITA: {self.selection['QUANTITA']}"
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=old_msg_text)
            self.reset()
            call.data="PRODOTTO=TAGLIO"
            time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"{Fore.YELLOW}{Style.BRIGHT}{time} | {self.username} -> SESSION RESET {self.selection}")
            self.newcut=True
        """Se la callback contiene QUANTITA allora passiamo al menu di selezione della stessa"""
        if "QUANTITA" in call.data:
            self.quantity_menu(bot,call)
            return
        """Se la callback contiene [BACK] allora si torna indietro di uno step"""
        if call.data=="[BACK]":
            lastkey=list(self.selection.keys())[-1]
            time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"{Fore.YELLOW}{Style.BRIGHT}{time} | {self.username} -> REMOVE [{lastkey} : {self.selection[lastkey]}]")
            del self.selection[lastkey]
            """Se la callback contiene [BACK] e perdiamo tutti i dati filtrati allora torniamo al menu principale"""
            if not self.selection:
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text='MESCOLA', callback_data='PRODOTTO=MESCOLA'))
                keyboard.add(types.InlineKeyboardButton(text='TAGLIO', callback_data='PRODOTTO=TAGLIO'))
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Ciao {self.username} Cosa hai prodotto?",reply_markup=keyboard)
                return
        else:
            self.add_selection(call.data)
        """Se siamo nella selezione di un prodotto di taglio"""
        if self.selection["PRODOTTO"]=="TAGLIO":
            lastkey=list(self.selection.keys())[-1]
            self.evaluate_data(call)
            """In base all'ultima selezione decidiamo se fornire un menu di nuovi filtri o di selezione valori"""
            if self.selection[lastkey]=="[0]":
                self.value_menu(bot,call)
            else:
                self.filter_menu(bot,call)
        if self.verbose:
            time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"{Fore.YELLOW}{Style.BRIGHT}{time} | {self.username} -> {self.selection}")

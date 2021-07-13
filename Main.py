from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineKeyboardButton
import MyCsv

# IMPORTANTE: inserire il token fornito dal BotFather nella seguente stringa
TOKEN="1892091599:AAH2J2nudTs0xffaZbR_4beAuu_3jNZWRK4"

def extract_number(text):
     return text.split()[1].strip()

def add_cut(update, context):
     usd=context.args
     eur=update.message.text
     print(f'Messaggio: {eur}')
     update.message.reply_text(f'{usd} - Hai scritto: {eur}')

def kill(update, context):
    pass

def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
  menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
  if header_buttons:
    menu.insert(0, header_buttons)
  if footer_buttons:
    menu.append(footer_buttons)
  return menu

def city(update,context):
  list_of_cities = ['Erode','Coimbatore','London', 'Thunder Bay', 'California']
  button_list = []
  for each in list_of_cities:
     button_list.append(InlineKeyboardButton(each, callback_data = each))
  reply_markup=InlineKeyboardMarkup(build_menu(button_list,n_cols=1)) #n_cols = 1 is for single column and mutliple rows
  bot.send_message(chat_id=update.message.chat_id, text='Choose from the following',reply_markup=reply_markup)

def main():
   upd= Updater(TOKEN, use_context=True)
   disp=upd.dispatcher

   disp.add_handler(CommandHandler("L161AM", add_cut))
   disp.add_handler(CommandHandler("L161B0", city))
   disp.add_handler(CommandHandler("kill", kill))

   upd.start_polling()

   upd.idle()

if __name__=='__main__':
   main()

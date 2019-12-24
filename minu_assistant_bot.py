# Python-telegram-bot libraries
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from time import time
import psutil
from datetime import timedelta

# Logging and requests libraries
import logging

# Importing token from config file
import config


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


# Displaying the starting message when bot starts
def start(update, context):
        inline_keyboard = [[InlineKeyboardButton('Место на диске',
                    callback_data='diskspace'),
                 InlineKeyboardButton('Аптайм',
                    callback_data='uptime'),
                 InlineKeyboardButton('Процессы с ботами',
                    callback_data='liveprocesses')]]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        update.message.reply_text(text="Помощник на сервере",
                             reply_markup=reply_markup)


def get_uptime():
    # value = datetime.datetime.fromtimestamp(psutil.boot_time())
    value = time() - psutil.boot_time()
    uptime_string = str(timedelta(seconds=value))
    return uptime_string


def bytes2human(n):
    # http://code.activestate.com/recipes/578019
    # >>> bytes2human(10000)
    # '9.8K'
    # >>> bytes2human(100001221)
    # '95.4M'
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


def get_diskspace():
    disk_usage = psutil.disk_usage('/')
    total_used_free_text = 'Total {total}, Used {used}, Free {free}\
                    '.format(total=bytes2human(disk_usage.total),
                    used=bytes2human(disk_usage.used),
                    free=bytes2human(disk_usage.free))
    return total_used_free_text


def get_liveprocesses():
    alive_bots_text = ''
    for p in psutil.process_iter(attrs=['name', 'status']):
        if 'bot' in p.info['name']:
            alive_bots_text = alive_bots_text + 'id: {}, name: {}, status: {} '.format(p.pid,p.info['name'],p.info['status'])
    return alive_bots_text


# Error handling
def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Sorry, I didn't understand the command!\
                             Please try again!")


def button(update, context):
    query = update.callback_query

    if query.data == 'diskspace':
        result_text = get_diskspace()
    elif query.data == 'uptime':
        result_text = get_uptime()
    elif query.data == 'liveprocesses':
        result_text = get_liveprocesses()
    else:
        result_text = 'Unknown command'

    query.edit_message_text(text="Status is: {}".format(result_text))


def main():
    # Importing the Updater object with token for updates from Telegram API
    # Declaring the Dispatcher object to send information to user
    # Creating the bot variable and adding our token
    updater = Updater(token=config.token, use_context=True)
    dispatcher = updater.dispatcher
    bot = telegram.Bot(token=config.token)

    # Logging module for debugging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    start_handler = CommandHandler('start', start)
    unknown_handler = MessageHandler(Filters.command, unknown)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(unknown_handler)

    # Updater function to start polling
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

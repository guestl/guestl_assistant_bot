# Python-telegram-bot libraries
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ChatAction
from functools import wraps

# Logging and requests libraries
import logging

# Importing token from config file
import config

# Importing the Updater object with token for updates from Telegram API
# Declaring the Dispatcher object to send information to user
# Creating the bot variable and adding our token
updater = Updater(token=config.token, use_context=True)
dispatcher = updater.dispatcher
bot = telegram.Bot(token=config.token)

# Logging module for debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Creating a reply keyboard
reply_keyboard = [['/free_space']]
markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)


# Typing animation to show to user to imitate human interaction
def send_typing_action(func):
    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id,
                                     action=ChatAction.TYPING)
        return func(update, context, *args, **kwargs)
    return command_func


# Displaying the starting message when bot starts
@send_typing_action
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Type /free_space to get a free space size",
                             reply_markup=markup)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


# Quote Message function to display the quotes
@send_typing_action
def freespace_message(update, context):
    freeSpace = "Nothing"
    context.bot.send_message(chat_id=update.message.chat_id, text=freeSpace)


freespace_message_handler = CommandHandler('free_space', freespace_message)
dispatcher.add_handler(freespace_message_handler)


# Error handling
@send_typing_action
def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Sorry, I didn't understand the command! Please try again!")


unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

# Updater function to start polling
updater.start_polling()
updater.idle()

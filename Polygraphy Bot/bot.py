#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#Empty Project Bot from Dight with Love

from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler)

import telegram

import logging
import config
from functools import wraps

import datetime
import os


users_path = os.getcwd() + "/Users/"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def send_typing_action(func):

    @wraps(func)
    def command_func(*args, **kwargs):
        bot, update = args
        bot.send_chat_action(chat_id=update.effective_message.chat_id, action=telegram.ChatAction.TYPING)
        return func(bot, update, **kwargs)

    return command_func


@send_typing_action
def start(bot, update):

    user = update.message.from_user.id

    if not os.path.exists(users_path+str(user)):
        os.mkdir(users_path+str(user), 0o777)

    text = "Добро пожаловать в Калькулятор распила досок"
    bot.sendMessage(user, text)

    text = "Выберите размеры доски"

    keyboard = [[InlineKeyboardButton("1500 x 750 мм", callback_data='first_size'),
                 InlineKeyboardButton("2500 x 1250 мм", callback_data='second_size')],

                [InlineKeyboardButton("2240 х 1220 мм", callback_data='third_size')]]

    markup = InlineKeyboardMarkup(keyboard)
    bot.send_photo(chat_id=user, photo=open('rasp_2.jpg', 'rb'),reply_markup=markup)

    return

@send_typing_action
def contact_handler(bot, update):
    """
    user = update.message.from_user.id
    contact = update.message.contact

    if user!= contact.user_id:
        bot.sendMessage(user, "К большому сожалению, нужно отправить именно свой номер :)")
    else:

        file = open(users_path + str(user)+"/phone_number.cfg","w")
        file.write(contact.phone_number)
        file.close()

        text = "Регистрация завершена. Теперь вы можете отправить контрольные данные для получения Ключа Активации"

        keyboard = [[ "СТРЕЛЬНУТЬ" ]]
        markup = telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

        bot.sendMessage(user, text, markup)
        
    return
    """
    pass

    
@send_typing_action
def InlineKeyboardHandler(bot, update):
    user = update.callback_query.from_user.id
    recieved_text = update.callback_query.data

    return

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    print(datetime.datetime.now() + " " + config.name + " Bot started...")

    if not os.path.exists(users_path):
        os.mkdir(users_path, 0o777)
    # Create the Updater and pass it your bot's token.
    updater = Updater(config.token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    
    # log all errors
    dispatcher.add_error_handler(error)

    #Command Handler
    dispatcher.add_handler(CommandHandler("start", start))

    #Contact Handler
    dispatcher.add_handler(MessageHandler(Filters.contact,contact_handler))

    dispatcher.add_handler(CallbackQueryHandler(InlineKeyboardHandler))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
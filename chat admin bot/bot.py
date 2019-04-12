#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#Empty Project Bot from Dight with Love

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import telegram

import logging
import config
from functools import wraps

import datetime
import os
import time


users_path = os.getcwd() + "\\Users\\"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

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
    
    #user = update.message.from_user.id
    #text = "Здравствуйте! Вас приветствует бот " + config.name + "\n\n" + config.description

    #bot.sendMessage(user, text)
    return

@send_typing_action
def contact_handler(bot, update):
    """
    Сохранение контактов
    """
    return

def text_handler(bot, update):
    chat = update.message.chat_id
    recieved_text = update.message.text

    if "!" in recieved_text:
        if recieved_text=="!ro":
            text = "Вы получаете Read Only. Мои поздравления :)"
            print(update.message.reply_to_message.message_id)
            bot.restrictChatMember(chat, update.message.reply_to_message.from_user.id, until_date=int(time.time())+30, can_send_messages=False, can_send_media_messages=False, can_send_other_messages=False, can_add_web_page_previews=False)
            bot.sendMessage(chat, text, reply_to_message_id = update.message.reply_to_message.message_id)
    return




def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    print(str(datetime.datetime.now()) + " " + config.name + " Bot started...")

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

    #Text Handler
    dispatcher.add_handler(MessageHandler(Filters.text, text_handler))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
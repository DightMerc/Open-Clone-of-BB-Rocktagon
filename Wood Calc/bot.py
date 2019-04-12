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
import shutil


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


def send_sending_photo_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(*args, **kwargs):
        bot, update = args
        bot.send_chat_action(chat_id=update.effective_message.chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
        return func(bot, update, **kwargs)

    return command_func



@send_typing_action
def start(bot, update):
    user = update.message.from_user.id

    if not os.path.exists(users_path+str(user)):
        os.mkdir(users_path+str(user), 0o777)
    if not os.path.exists(users_path+str(user)+"/Details"):
        os.mkdir(users_path+str(user)+"/Details", 0o777)
    else:
        shutil.rmtree(users_path+str(user)+"/Details",True)
        os.mkdir(users_path+str(user)+"/Details", 0o777)


    file = open(users_path+str(user)+"/counter","w",encoding="utf8")
    file.write("0")
    file.close()
    

    text = "Добро пожаловать в Калькулятор распила досок"

    bot.sendMessage(user, text)
    send_photo(bot, update)

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

@send_sending_photo_action
def send_photo(bot, update):
    user = update.message.from_user.id

    text = "Выберите толщину доски"

    keyboard = [[InlineKeyboardButton("15 мм", callback_data='15'),
                InlineKeyboardButton("18 мм", callback_data='18')],

                [InlineKeyboardButton("21 мм", callback_data='21')]]

    markup = InlineKeyboardMarkup(keyboard)

    bot.send_photo(chat_id=user, caption=text, photo=open('wood.jpeg', 'rb'), reply_markup=markup)
    

    
    return
    
@send_typing_action
def InlineKeyboardHandler(bot, update):
    recieved_text = update.callback_query.data
    user = update.callback_query.from_user.id
    
    if recieved_text in "15" or recieved_text in "18" or recieved_text in "21":
        text = "Выбранная ширина: <b>"+recieved_text+"мм </b>"

        keyboard = [[InlineKeyboardButton("Изменить размер", callback_data='change_size_1')]]
        markup = InlineKeyboardMarkup(keyboard)

        bot.editMessageCaption(user, update.callback_query.message.message_id, caption=text, reply_markup=markup, parse_mode=telegram.ParseMode.HTML)
        
        text = "Выберите размеры доски"

        keyboard = [[InlineKeyboardButton("1500 x 750 мм", callback_data='first_size'),
                    InlineKeyboardButton("2240 х 1220 мм", callback_data='second_size')],

                    [InlineKeyboardButton("2500 x 1250 мм", callback_data='third_size')]]

        markup = InlineKeyboardMarkup(keyboard)

        message = bot.send_photo(chat_id=user, caption=text, photo=open('rasp_2.jpg', 'rb'), reply_markup=markup)

        file = open(users_path+str(user)+"/main_size_sh","w", encoding="utf8")
        file.write(str(recieved_text))
        file.close()

        file = open(users_path+str(user)+"/temp_id","w", encoding="utf8")
        file.write(str(message.message_id))
        file.close()
        return

    if recieved_text in "first_size":
        text = "Выбранный размер: <b>1500 x 750 мм</b>"

        keyboard = [[InlineKeyboardButton("Изменить размер", callback_data='change_size')]]
        markup = InlineKeyboardMarkup(keyboard)

        bot.editMessageCaption(user, update.callback_query.message.message_id, caption=text, reply_markup=markup, parse_mode=telegram.ParseMode.HTML)

        text = "Отправьте размер изделия(не должен превышать <b>1500 x 750 мм</b>)"
        message = bot.sendMessage(user, text, parse_mode=telegram.ParseMode.HTML)

        file = open(users_path+str(user)+"/adding_size","w", encoding="utf8")
        file.close()
        

        file = open(users_path+str(user)+"/main_size","w", encoding="utf8")
        file.write("1500\n750")
        file.close()

        file = open(users_path+str(user)+"/temp_id","w", encoding="utf8")
        file.write(str(message.message_id))
        file.close()
        return
    if recieved_text in "second_size":
        text = "Выбранный размер: <b>2240 х 1220 мм</b>"

        keyboard = [[InlineKeyboardButton("Изменить размер", callback_data='change_size')]]
        markup = InlineKeyboardMarkup(keyboard)

        bot.editMessageCaption(user, update.callback_query.message.message_id, caption=text, reply_markup=markup, parse_mode=telegram.ParseMode.HTML)

    

        text = "Отправьте размер изделия(не должен превышать <b>2500 x 1250 мм</b>)"
        message = bot.sendMessage(user, text, parse_mode=telegram.ParseMode.HTML)

        file = open(users_path+str(user)+"/adding_size","w", encoding="utf8")
        file.close()

        file = open(users_path+str(user)+"/main_size","w", encoding="utf8")
        file.write("2240\n1220")
        file.close()
        
        file = open(users_path+str(user)+"/temp_id","w", encoding="utf8")
        file.write(str(message.message_id))
        file.close()
        return
    if recieved_text in "third_size":
        text = "Выбранный размер: <b>2500 x 1250 мм</b>"

        keyboard = [[InlineKeyboardButton("Изменить размер", callback_data='change_size')]]
        markup = InlineKeyboardMarkup(keyboard)

        bot.editMessageCaption(user, update.callback_query.message.message_id, caption=text, reply_markup=markup, parse_mode=telegram.ParseMode.HTML)

        text = "Отправьте размер изделия(не должен превышать <b>2240 х 1220 мм</b>)"
        message = bot.sendMessage(user, text, parse_mode=telegram.ParseMode.HTML)

        file = open(users_path+str(user)+"/adding_size","w", encoding="utf8")
        file.close()

        file = open(users_path+str(user)+"/main_size","w", encoding="utf8")
        file.write("2500\n1250")
        file.close()
        
        file = open(users_path+str(user)+"/temp_id","w", encoding="utf8")
        file.write(str(message.message_id))
        file.close()
        return
    if recieved_text in "change_size":
        try:
            file = open(users_path+str(user)+"/temp_id","r", encoding="utf8")
            temp_id = file.read()
            file.close()
        except Exception as e:
            temp_id = ""
        try:
            bot.deleteMessage(user, temp_id)
        except Exception as e:
            pass
        text = "Выберите размеры доски"

        keyboard = [[InlineKeyboardButton("1500 x 750 мм", callback_data='first_size'),
                    InlineKeyboardButton("2240 х 1220 мм", callback_data='second_size')],

                    [InlineKeyboardButton("2500 x 1250 мм", callback_data='third_size')]]

        markup = InlineKeyboardMarkup(keyboard)

        bot.editMessageCaption(user, update.callback_query.message.message_id, caption=text, reply_markup=markup, parse_mode=telegram.ParseMode.HTML)

        
        return
    
    if recieved_text in "change_size_1":
        try:
            file = open(users_path+str(user)+"/temp_id","r", encoding="utf8")
            temp_id = file.read()
            file.close()
        except Exception as e:
            temp_id = ""
        try:
            bot.deleteMessage(user, temp_id)
        except Exception as e:
            pass
        text = "Выберите толщину доски"

        keyboard = [[InlineKeyboardButton("15 мм", callback_data='15'),
                    InlineKeyboardButton("18 мм", callback_data='18')],

                    [InlineKeyboardButton("21 мм", callback_data='21')]]

        markup = InlineKeyboardMarkup(keyboard)

        bot.editMessageCaption(user, update.callback_query.message.message_id, caption=text, reply_markup=markup, parse_mode=telegram.ParseMode.HTML)

        
        return

    




def TextHandler(bot, update):
    user = update.message.from_user.id
    recieved_text = update.message.text

    
    
    if "Расчёт" in recieved_text:
        if os.path.exists(users_path+str(user)+"/adding_size"):
            os.remove(users_path+str(user)+"/adding_size")
        file = open(users_path+str(user)+"/counter","w",encoding="utf8")
        file.write("0")
        file.close()

        sq_details = 0

        detail_text = "Список:\n"

        data = os.listdir(users_path+str(user)+"/Details")
        for a in data:
            file = open(users_path+str(user)+"/Details/"+str(a),"r",encoding="utf8")
            size = file.readlines()
            file.close()

            detail_text = detail_text + "      Изделие размером <b>" + str(size[0]).replace("\n","") + " x " + str(size[1]).replace("\n","") + " мм</b>\n"

            sq_details = sq_details + int(size[0])*int(size[1])
        
        file = open(users_path+str(user)+"/main_size","r",encoding="utf8")
        wood_size = file.readlines()
        file.close()

        file = open(users_path+str(user)+"/main_size_sh","r",encoding="utf8")
        wood_size_sh = file.read()
        file.close()

        sq_main = int(wood_size[0])*int(wood_size[1])

        number = sq_details/sq_main
        int_part = int(number)
        
        

        if number-int_part!=0:
            number = int_part + 1
        else:
            number = int_part

        end = "%.2f" % ((int(sq_main*number) - int(sq_details))/ 10)

        price = 75000
        
        text = detail_text + "\nРазмер доски: <b>"+str(wood_size[0]).replace("\n","")+" x "+str(wood_size[1]).replace("\n","")+" мм</b> Толщина: <b>"+str(wood_size_sh)+" мм</b>\nКоличество: <b>" + str(number) + "</b>\n\nОбщая площадь остатков: <b>"+str(end)+" кв см</b>\n\nЦена: <b>" + str("%.2f" % (number*price)) + " сум</b>"

        bot.sendMessage(user, text, parse_mode=telegram.ParseMode.HTML)

        text = "Для того, чтобы выполнить ещё один запрос - нажмите /start"

        markup = telegram.ReplyKeyboardRemove()

        bot.sendMessage(user, text, reply_markup=markup)

        return

    recieved_text = recieved_text.replace("*"," ")
    recieved_text = recieved_text.replace("x"," ")
    recieved_text = recieved_text.replace("X"," ")
    
    current_size = recieved_text.split()

    if len(current_size)!=2:
        text = "Введены неверные данные(ширина*длина)"
        bot.sendMessage(user, text)
        return
    if not current_size[0].isdigit() or not current_size[0].isdigit():
        text = "Введены неверные данные(ширина*длина)"
        bot.sendMessage(user, text)
        return

    if os.path.exists(users_path+str(user)+"/adding_size"):
        file = open(users_path+str(user)+"/main_size", "r", encoding="utf8")
        size = file.readlines()
        file.close()

        if int(size[0])<int(current_size[0]) and int(size[1])<int(current_size[1]):
            text = "Размер изделия слишком велик. Укажите меньший размер изделия, либо выберите другой размер доски"
            bot.sendMessage(user, text)
            return
        else:
            file = open(users_path+str(user)+"/counter","r",encoding="utf8")
            n = file.read()
            file.close()

            file = open(users_path+str(user)+"/Details/detail"+str(n),"w",encoding="utf8")
            file.write(str(current_size[0])+"\n"+str(current_size[1]))
            file.close()

            file = open(users_path+str(user)+"/counter","w",encoding="utf8")
            file.write(str(int(n)+1))
            file.close()

            text = "Деталь с размерами <b>"+str(current_size[0])+" x "+str(current_size[1])+" мм </b> добавлена"

            bot.sendMessage(user, text, parse_mode=telegram.ParseMode.HTML)


            reply_keyboard = [['Расчёт']]
            markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)

            text = "Продолжите присылать размеры деталей, для добавления новых, либо нажмите кнопку -> <b>Расчёт</b>"

            bot.sendMessage(user, text, reply_markup=markup, parse_mode=telegram.ParseMode.HTML)

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

    dispatcher.add_handler(CallbackQueryHandler(InlineKeyboardHandler))

    dispatcher.add_handler(MessageHandler(Filters.text, TextHandler))


    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
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
import threading

from client import Client

import emoji


users_path = os.getcwd() + "\\Users\\"

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


def CreateTelegramUser(user, full_name, username, phone):

    if str(username)=="None":
        username = "none"
    phone = str(phone).replace("+","")
    phone = str(phone).replace("-","")
    phone = str(phone).replace(" ","")

    cli = Client()
    cli.CreateUser(user, full_name, username, phone)

    return

def CreateBook(title, author, published_date):
    description = "Нет описания"
    rating = 0

    cli = Client()
    cli.CreateBook(title, author, description, published_date, rating)

    return



@send_typing_action
def start(bot, update):
    user = update.message.from_user.id

    if not os.path.exists(users_path+str(user)):
        os.mkdir(users_path+str(user), 0o777)
    if not os.path.exists(users_path+str(user)+"\\Books"):
        os.mkdir(users_path+str(user)+"\\Books", 0o777)

    with open(users_path+str(user)+"\\Books\\counter","w") as file:
        file.write("1")
    

    text = config.greetings
    bot.sendMessage(user, text)
    if not os.path.exists(users_path+str(user)+"\\phone"):
        text = "Для начала, давай познакомимся. Отправь свой номер телефона"

        #location_keyboard = telegram.KeyboardButton(text="send_location", request_location=True)
        contact_keyboard = telegram.KeyboardButton(text="Поделиться номером", request_contact=True)
        custom_keyboard = [[ contact_keyboard ]]

        markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
        bot.send_message(chat_id=user, text=text, reply_markup=markup)
    else:
        text = "Выбери действие"

        keyboard = [[ emoji.emojize(":blue_book: Мои книги", use_aliases=True), emoji.emojize(":books: Все книги", use_aliases=True) ],[ emoji.emojize("🏡 Мои друзья", use_aliases=True) ],[ emoji.emojize(":loudspeaker: Стрельнуть книгу", use_aliases=True) ]]
        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)

        bot.sendMessage(user, text, reply_markup=markup)

    return

@send_typing_action
def contact_handler(bot, update):
    
    user = update.message.from_user.id
    contact = update.message.contact

    
    if user!= contact.user_id:
        bot.sendMessage(user, "К большому сожалению, нужно отправить именно свой номер :)")
    else:

        my_thread = threading.Thread(target=CreateTelegramUser, args=(user, update.message.from_user.full_name, update.message.from_user.username, contact.phone_number,))
        my_thread.start()

        text = "Отлично!\nТеперь давай соберём свою библиотеку"

        keyboard = [[InlineKeyboardButton("Добавить книгу", callback_data='add_book')]]
        markup = InlineKeyboardMarkup(keyboard)

        bot.sendMessage(user, text, reply_markup=markup)

        with open(users_path+str(user)+"\\phone","w") as file:
            file.write(contact.phone_number)
        
    return


def InlineKeyboardHandler(bot, update):
    user = update.callback_query.from_user.id
    recieved_text = update.callback_query.data

    if "clear" in recieved_text:
        bot.answerCallbackQuery(update.callback_query.id)

        with open(users_path + str(user)+"\\temp_id2") as file:
            temp_id = file.read()


        os.remove(users_path + str(user)+"\\adding_book")
        os.remove(users_path + str(user)+"\\temp_id2")

        text = "Заполни имеющуюся информацию"

        keyboard = [[InlineKeyboardButton("Название", callback_data='null'), InlineKeyboardButton("__________", callback_data='add_title')],
                    [InlineKeyboardButton("Автор", callback_data='null'), InlineKeyboardButton("__________", callback_data='add_author')],
                    [InlineKeyboardButton("Год издания", callback_data='null'), InlineKeyboardButton("__________", callback_data='add_date')]]
        markup = InlineKeyboardMarkup(keyboard)

        temp = bot.edit_message_text(text=text, chat_id=user, message_id=temp_id,  reply_markup=markup)
        with open(users_path + str(user)+"\\temp_id2","w") as file:
            file.write(str(temp.message_id))
        
        return

    if "publish" in recieved_text:
        bot.answerCallbackQuery(update.callback_query.id)

        with open(users_path+str(user)+"\\Books\\counter") as file:
            counter = int(file.read())

        if not os.path.exists(users_path+str(user)+"\\Books\\"+str(counter)):
            os.mkdir(users_path+str(user)+"\\Books\\"+str(counter), 0o777)
            book_dir = users_path+str(user)+"\\Books\\"+str(counter)
        else:
            os.mkdir(users_path+str(user)+"\\Books\\"+str(counter+1), 0o777)
            with open(users_path+str(user)+"\\Books\\counter","w") as file:
                file.write(str(counter+1))
            book_dir = users_path+str(user)+"\\Books\\"+str(counter+1)

        to_cli = []
            
        with open(users_path+str(user)+"\\adding_book","r",encoding="utf8") as file:
            book = file.readlines()
        os.remove(users_path+str(user)+"\\adding_book")

        with open(book_dir+"\\title","w",encoding="utf8") as file:
            file.write(str(book[0]).replace("\n",""))
            to_cli.append(str(book[0]).replace("\n",""))
        
        with open(book_dir+"\\author","w",encoding="utf8") as file:
            file.write(str(book[1]).replace("\n",""))
            to_cli.append(str(book[1]).replace("\n",""))

        
        if book[2]!="\n":
            with open(book_dir+"\\date","w",encoding="utf8") as file:
                file.write(str(book[2]).replace("\n",""))
                to_cli.append(str(book[2]).replace("\n",""))
        else:
            to_cli.append("0")

        my_thread = threading.Thread(target=CreateBook, args=(to_cli[0], to_cli[1], to_cli[2],))
        my_thread.start()

        text = "{} - {}\nКнига добавлена".format(to_cli[0], to_cli[1])
        bot.edit_message_text(text=text, chat_id=user, message_id=update.callback_query.message.message_id,  reply_markup="")

        bot.answerCallbackQuery(update.callback_query.id, "Книга добавлена", show_alert=True)

        path = users_path + str(user) + "\\Books\\"
        if not len(os.listdir(path))>2:
            text = "Отлично! Твоя первая книга добавлена :)\nВыбери действие"
        else:
            text = "Выбери действие"

        

        keyboard = [[ emoji.emojize(":blue_book: Мои книги", use_aliases=True), emoji.emojize(":books: Все книги", use_aliases=True) ],[ emoji.emojize("🏡 Мои друзья", use_aliases=True) ],[ emoji.emojize(":loudspeaker: Стрельнуть книгу", use_aliases=True) ]]
        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)

        bot.sendMessage(user, text, reply_markup=markup)
        return
        

    if "add_book" in recieved_text:
        bot.answerCallbackQuery(update.callback_query.id)

        text = "Заполни имеющуюся информацию"

        keyboard = [[InlineKeyboardButton("Название", callback_data='null'), InlineKeyboardButton("__________", callback_data='add_title')],
                    [InlineKeyboardButton("Автор", callback_data='null'), InlineKeyboardButton("__________", callback_data='add_author')],
                    [InlineKeyboardButton("Год издания", callback_data='null'), InlineKeyboardButton("__________", callback_data='add_date')]]
        markup = InlineKeyboardMarkup(keyboard)

        temp = bot.edit_message_text(text=text, chat_id=user, message_id=update.callback_query.message.message_id,  reply_markup=markup)
        with open(users_path + str(user)+"\\temp_id2","w") as file:
            file.write(str(temp.message_id))
        
        return
    

    if "null" in recieved_text:
        bot.answerCallbackQuery(update.callback_query.id)
        return

    if "add_title" in recieved_text:
        bot.answerCallbackQuery(update.callback_query.id)

        with open(users_path + str(user)+"\\adding_title","w") as file:
            file.write("")

        text = "Отправь название книги"
        
        
        temp = bot.sendMessage(user, text)

        with open(users_path + str(user)+"\\temp_id","w") as file:
            file.write(str(temp.message_id))
        

        return

    if "add_author" in recieved_text:
        bot.answerCallbackQuery(update.callback_query.id)

        with open(users_path + str(user)+"\\adding_author","w") as file:
            file.write("")

        text = "Отправь автора книги"
        
        temp = bot.sendMessage(user, text)

        with open(users_path + str(user)+"\\temp_id","w") as file:
            file.write(str(temp.message_id))

        return

    if "add_date" in recieved_text:
        bot.answerCallbackQuery(update.callback_query.id)

        with open(users_path + str(user)+"\\adding_date","w") as file:
            file.write("")

        text = "Отправь дату издания книги"
        
        temp = bot.sendMessage(user, text)

        with open(users_path + str(user)+"\\temp_id","w") as file:
            file.write(str(temp.message_id))

        return

    return    

@send_typing_action
def text_handler(bot, update):
    
    recieved_text = update.message.text

    print(recieved_text)
    user = update.message.from_user.id
    

    if "Мои друзья" in recieved_text:

        bot.send_photo(chat_id=user, photo=open('image.jpg', 'rb'), caption="В разработке :)")
        text = "Выбери действие"

        keyboard = [[ emoji.emojize(":blue_book: Мои книги", use_aliases=True), emoji.emojize(":books: Все книги", use_aliases=True) ],[ emoji.emojize("🏡 Мои друзья", use_aliases=True) ],[ emoji.emojize(":loudspeaker: Стрельнуть книгу", use_aliases=True) ]]
        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)

        bot.sendMessage(user, text, reply_markup=markup)

        return

    if "Стрельнуть книгу" in recieved_text:
        with open(users_path + str(user)+"\\request_book","w", encoding="utf8") as file:
            file.write("")

        text = "Отправь название книги"
        bot.sendMessage(user, text)

        return

    if "Мои книги" in recieved_text:
        path = users_path + str(user) + "\\Books\\"
        books = ""
        for a in os.listdir(path):
            try:
                with open(path + str(a) + "\\title", "r", encoding="utf8") as file:
                    title = file.read()
                with open(path + str(a) + "\\author", "r", encoding="utf8") as file:
                    author = file.read()

                string = "{} - {}".format(author, title)
                books = books + string + "\n"
                
            except Exception as e:
                pass
        
        keyboard = [[InlineKeyboardButton("Добавить книгу", callback_data='add_book')]]
        markup = InlineKeyboardMarkup(keyboard)

        bot.sendMessage(user, books, reply_markup=markup)
        return
    
    if "Все книги" in recieved_text:
        bot.sendMessage(user, "http://127.0.0.1:8000/")

        return

    if os.path.exists(users_path + str(user)+"\\request_book2"):
        with open(users_path + str(user)+"\\request_books","a", encoding="utf8") as file:
                    file.write(recieved_text+"\n")
        
        os.remove(users_path + str(user)+"\\request_book2")
        
        text = "Отправь гео, чтобы людям было легче тебя найти"

        location_keyboard = telegram.KeyboardButton(text="Отправить гео", request_location=True)
        custom_keyboard = [[ location_keyboard ]]

        markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=True)

        bot.sendMessage(user, text, reply_markup=markup)

        return

    if os.path.exists(users_path + str(user)+"\\request_book"):
        with open(users_path + str(user)+"\\request_books","w", encoding="utf8") as file:
                    file.write(recieved_text+"\n")

        os.remove(users_path + str(user)+"\\request_book")
        

        text = "Отправь автора книги"

        bot.sendMessage(user, text)

        with open(users_path + str(user)+"\\request_book2","w", encoding="utf8") as file:
            file.write("")

        return

    

    if os.path.exists(users_path + str(user)+"\\adding_title"):
        with open(users_path + str(user)+"\\temp_id") as file:
            temp_id = file.read()
        os.remove(users_path + str(user)+"\\temp_id")


        bot.deleteMessage(user, temp_id)

        with open(users_path + str(user)+"\\temp_id2") as file:
            temp_id = file.read()

        bot.deleteMessage(user, temp_id)

        if not os.path.exists(users_path + str(user)+"\\adding_book"):
            template = "__________"
            book = []

            title = str(recieved_text).replace("\n","")
            author = template
            date = template

            book.append(title)
            book.append(author)
            book.append(date)
            with open(users_path + str(user)+"\\adding_book", "w", encoding="utf8") as file:
                for a in book:
                    if str(a)!=template:
                        file.write(str(a) + "\n")
                    else:
                        file.write("\n")
            
            text = "Заполни имеющуюся информацию"

            keyboard = [[InlineKeyboardButton("Название", callback_data='null'), InlineKeyboardButton(str(book[0]), callback_data='add_title')],
                        [InlineKeyboardButton("Автор", callback_data='null'), InlineKeyboardButton(str(book[1]), callback_data='add_author')],
                        [InlineKeyboardButton("Год издания", callback_data='null'), InlineKeyboardButton(str(book[2]), callback_data='add_date')]]
            if title!=template and author!=template:
                key = []
                key.append(InlineKeyboardButton("Очистить", callback_data='clear'))

                keyboard.append(key)

                key = []
                key.append(InlineKeyboardButton(emoji.emojize("✅ Добавить",use_aliases=True), callback_data='publish'))
                
                keyboard.append(key)
            markup = InlineKeyboardMarkup(keyboard)

            temp = bot.sendMessage(user, text, reply_markup=markup)
            with open(users_path + str(user)+"\\temp_id2","w") as file:
                file.write(str(temp.message_id))


            os.remove(users_path + str(user)+"\\adding_title")
            
            return

        else:

            with open(users_path + str(user)+"\\adding_book", encoding="utf8") as file:
                book_info = file.readlines()

                template = "__________"
                book = []

                title = str(recieved_text).replace("\n","")

                if str(book_info[1])!="\n":
                    author = str(book_info[1]).replace("\n","")
                else:
                    author = template

                if str(book_info[2])!="\n":
                    date = str(book_info[2]).replace("\n","")
                else:
                    date = template

                book.append(title)
                book.append(author)
                book.append(date)
                with open(users_path + str(user)+"\\adding_book", "w", encoding="utf8") as file:
                    for a in book:
                        if str(a)!=template:
                            file.write(str(a) + "\n")
                        else:
                            file.write("\n")
            
            text = "Заполни имеющуюся информацию"

            keyboard = [[InlineKeyboardButton("Название", callback_data='null'), InlineKeyboardButton(str(book[0]), callback_data='add_title')],
                        [InlineKeyboardButton("Автор", callback_data='null'), InlineKeyboardButton(str(book[1]), callback_data='add_author')],
                        [InlineKeyboardButton("Год издания", callback_data='null'), InlineKeyboardButton(str(book[2]), callback_data='add_date')]]
            if title!=template and author!=template:
                key = []
                key.append(InlineKeyboardButton("Очистить", callback_data='clear'))


                keyboard.append(key)

                key = []
                key.append(InlineKeyboardButton(emoji.emojize("✅ Добавить",use_aliases=True), callback_data='publish'))


                keyboard.append(key)
            markup = InlineKeyboardMarkup(keyboard)

            temp = bot.sendMessage(user, text, reply_markup=markup)
            with open(users_path + str(user)+"\\temp_id2","w") as file:
                file.write(str(temp.message_id))

            os.remove(users_path + str(user)+"\\adding_title")
            
            return

    if os.path.exists(users_path + str(user)+"\\adding_date"):
        with open(users_path + str(user)+"\\temp_id") as file:
            temp_id = file.read()
        os.remove(users_path + str(user)+"\\temp_id")

        bot.deleteMessage(user, temp_id)

        with open(users_path + str(user)+"\\temp_id2") as file:
            temp_id = file.read()

        bot.deleteMessage(user, temp_id)

        if not os.path.exists(users_path + str(user)+"\\adding_book"):
            template = "__________"
            book = []

            date = str(recieved_text).replace("\n","")
            title = template
            author = template

            book.append(title)
            book.append(author)
            book.append(date)
            with open(users_path + str(user)+"\\adding_book", "w", encoding="utf8") as file:
                for a in book:
                    if str(a)!=template:
                        file.write(str(a) + "\n")
                    else:
                        file.write("\n")
            
            text = "Заполни имеющуюся информацию"

            keyboard = [[InlineKeyboardButton("Название", callback_data='null'), InlineKeyboardButton(str(book[0]), callback_data='add_title')],
                        [InlineKeyboardButton("Автор", callback_data='null'), InlineKeyboardButton(str(book[1]), callback_data='add_author')],
                        [InlineKeyboardButton("Год издания", callback_data='null'), InlineKeyboardButton(str(book[2]), callback_data='add_date')]]
            if title!=template and author!=template:
                key = []
                key.append(InlineKeyboardButton("Очистить", callback_data='clear'))

                keyboard.append(key)

                key = []
                key.append(InlineKeyboardButton(emoji.emojize("✅ Добавить",use_aliases=True), callback_data='publish'))

                keyboard.append(key)
            markup = InlineKeyboardMarkup(keyboard)

            temp = bot.sendMessage(user, text, reply_markup=markup)
            with open(users_path + str(user)+"\\temp_id2","w") as file:
                file.write(str(temp.message_id))
            

            os.remove(users_path + str(user)+"\\adding_date")
            
            return
        else:

            with open(users_path + str(user)+"\\adding_book", encoding="utf8") as file:
                book_info = file.readlines()

                template = "__________"
                book = []

                date = str(recieved_text).replace("\n","")

                if str(book_info[0])!="\n":
                    title = str(book_info[0]).replace("\n","")
                else:
                    title = template

                if str(book_info[1])!="\n":
                    author = str(book_info[1]).replace("\n","")
                else:
                    author = template

                book.append(title)
                book.append(author)
                book.append(date)
                with open(users_path + str(user)+"\\adding_book", "w", encoding="utf8") as file:
                    for a in book:
                        if str(a)!=template:
                            file.write(str(a) + "\n")
                        else:
                            file.write("\n")
            
            text = "Заполни имеющуюся информацию"

            keyboard = [[InlineKeyboardButton("Название", callback_data='null'), InlineKeyboardButton(str(book[0]), callback_data='add_title')],
                        [InlineKeyboardButton("Автор", callback_data='null'), InlineKeyboardButton(str(book[1]), callback_data='add_author')],
                        [InlineKeyboardButton("Год издания", callback_data='null'), InlineKeyboardButton(str(book[2]), callback_data='add_date')]]
            if title!=template and author!=template:
                key = []
                key.append(InlineKeyboardButton("Очистить", callback_data='clear'))

                keyboard.append(key)

                key = []
                key.append(InlineKeyboardButton(emoji.emojize("✅ Добавить",use_aliases=True), callback_data='publish'))
                
                keyboard.append(key)
            markup = InlineKeyboardMarkup(keyboard)

            temp = bot.sendMessage(user, text, reply_markup=markup)
            with open(users_path + str(user)+"\\temp_id2","w") as file:
                file.write(str(temp.message_id))
            
            os.remove(users_path + str(user)+"\\adding_date")

            return

        
    if os.path.exists(users_path + str(user)+"\\adding_author"):
        with open(users_path + str(user)+"\\temp_id") as file:
            temp_id = file.read()
        os.remove(users_path + str(user)+"\\temp_id")

        bot.deleteMessage(user, temp_id)

        with open(users_path + str(user)+"\\temp_id2") as file:
            temp_id = file.read()

        bot.deleteMessage(user, temp_id)

        if not os.path.exists(users_path + str(user)+"\\adding_book"):
            template = "__________"
            book = []

            author = str(recieved_text).replace("\n","")
            title = template
            date = template

            book.append(title)
            book.append(author)
            book.append(date)
            with open(users_path + str(user)+"\\adding_book", "w", encoding="utf8") as file:
                for a in book:
                    if str(a)!=template:
                        file.write(str(a) + "\n")
                    else:
                        file.write("\n")
            
            text = "Заполни имеющуюся информацию"

            keyboard = [[InlineKeyboardButton("Название", callback_data='null'), InlineKeyboardButton(str(book[0]), callback_data='add_title')],
                        [InlineKeyboardButton("Автор", callback_data='null'), InlineKeyboardButton(str(book[1]), callback_data='add_author')],
                        [InlineKeyboardButton("Год издания", callback_data='null'), InlineKeyboardButton(str(book[2]), callback_data='add_date')]]
            if title!=template and author!=template:
                key = []
                key.append(InlineKeyboardButton("Очистить", callback_data='clear'))
                
                keyboard.append(key)

                key = []
                key.append(InlineKeyboardButton(emoji.emojize("✅ Добавить",use_aliases=True), callback_data='publish'))

                keyboard.append(key)


            markup = InlineKeyboardMarkup(keyboard)

            temp = bot.sendMessage(user, text, reply_markup=markup)
            with open(users_path + str(user)+"\\temp_id2","w") as file:
                file.write(str(temp.message_id))
            

            os.remove(users_path + str(user)+"\\adding_author")

            return
        else:

            with open(users_path + str(user)+"\\adding_book", encoding="utf8") as file:
                book_info = file.readlines()

                template = "__________"
                book = []

                author = str(recieved_text).replace("\n","")

                if str(book_info[0])!="\n":
                    title = str(book_info[0]).replace("\n","")
                else:
                    title = template

                

                if str(book_info[2])!="\n":
                    date = str(book_info[2]).replace("\n","")
                else:
                    date = template

                book.append(title)
                book.append(author)
                book.append(date)
                with open(users_path + str(user)+"\\adding_book", "w", encoding="utf8") as file:
                    for a in book:
                        if str(a)!=template:
                            file.write(str(a) + "\n")
                        else:
                            file.write("\n")
            
            text = "Заполни имеющуюся информацию"

            keyboard = [[InlineKeyboardButton("Название", callback_data='null'), InlineKeyboardButton(str(book[0]), callback_data='add_title')],
                        [InlineKeyboardButton("Автор", callback_data='null'), InlineKeyboardButton(str(book[1]), callback_data='add_author')],
                        [InlineKeyboardButton("Год издания", callback_data='null'), InlineKeyboardButton(str(book[2]), callback_data='add_date')]]
            if title!=template and author!=template:
                key = []
                key.append(InlineKeyboardButton("Очистить", callback_data='clear'))

                keyboard.append(key)

                key = []
                key.append(InlineKeyboardButton(emoji.emojize("✅ Добавить",use_aliases=True), callback_data='publish'))

                keyboard.append(key)
            markup = InlineKeyboardMarkup(keyboard)

            temp = bot.sendMessage(user, text, reply_markup=markup)
            with open(users_path + str(user)+"\\temp_id2","w") as file:
                file.write(str(temp.message_id))
            

            os.remove(users_path + str(user)+"\\adding_author")

            return
            
def location_handler(bot, update):
    loc = update.message.location
    user = update.message.from_user.id
    
    with open(users_path + str(user)+"\\request_books","r",encoding="utf8") as file:
        request = file.readlines()
    
    with open(users_path+str(user)+"\\phone","r") as file:
        phone = file.read()

    if update.message.from_user.username!="None":
        contacts = update.message.from_user.full_name + " | @" + update.message.from_user.username + " | " + phone
    else:
        contacts = update.message.from_user.full_name + " | " + phone


    text = "<b>Кто?</b>\n{}\n\n<b>Что?</b>\n{} - {}\n\n<b>Где?</b>".format(contacts, str(request[1]).replace("\n",""), str(request[0]).replace("\n",""))
    bot.sendMessage(-1001180376076, text, parse_mode=telegram.ParseMode.HTML)
    bot.sendLocation(-1001180376076, loc.latitude, loc.longitude)
    
    text = "Твоя заявка принята и опубликована тут: @epam_bookshare"
    bot.sendMessage(user, text)

    text = "Выбери действие"

    keyboard = [[ emoji.emojize(":blue_book: Мои книги", use_aliases=True), emoji.emojize(":books: Все книги", use_aliases=True) ],[ emoji.emojize("🏡 Мои друзья", use_aliases=True) ],[ emoji.emojize(":loudspeaker: Стрельнуть книгу", use_aliases=True) ]]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)

    bot.sendMessage(user, text, reply_markup=markup)

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

    dispatcher.add_handler(MessageHandler(Filters.location,location_handler))

    dispatcher.add_handler(CallbackQueryHandler(InlineKeyboardHandler))

    dispatcher.add_handler(MessageHandler(Filters.text, text_handler))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
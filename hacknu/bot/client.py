import requests

from config import url

import json



class Client(object):

    def CreateUser(self, telegram_id, full_name, username, phone):

        usr = User(telegram_id=telegram_id, full_name=full_name, username=username, phone=phone)
        headers = {'Content-Type': 'application/json'}

        r = requests.post(url + "api/v2/users/create/", data=json.dumps(usr.__dict__), headers=headers)
        return str(r.status_code)

    def CreateBook(self, title, author, description, published_date, rating):
        bk = Book(title=title, author=author, description=description, published_date=published_date, rating=rating)
        headers = {'Content-Type': 'application/json'}

        r = requests.post(url + "api/v2/books/create/", data=json.dumps(bk.__dict__), headers=headers)

        return str(r.status_code)

    def GetAllBooks(self):
        r = requests.get(url + 'api/v2/books/')
        r.status_code
        
        return(r.json())

    def GetAllUsers(self):
        r = requests.get(url + 'api/v2/users/')
        r.status_code

        return(r.json())



        



class User(object):

    def __init__(self, telegram_id, full_name, username, phone):
        self.telegram_id = telegram_id
        self.full_name = full_name
        if username!="":
            self.username = username
        else:
            self.username = ""
        self.phone = phone
        

class Book(object):

    def __init__(self, title, author, description, published_date, rating):
        self.title = title
        self.author = author

        if description!="":
            self.description = description
        else:
            self.description = "Описание отсутствует"

        self.published_date = published_date
        self.rating = rating

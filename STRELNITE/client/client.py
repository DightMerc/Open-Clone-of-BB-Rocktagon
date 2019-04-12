import requests

import json
from collections import namedtuple


class Client(object):

    def CreateUser(self, telegram_id, full_name, username=""):

        usr = User(telegram_id=telegram_id, full_name=full_name, username=username)
        headers = {'Content-Type': 'application/json'}

        r = requests.post("http://localhost:8000/api/v2/users/create/", data=json.dumps(usr.__dict__), headers=headers)
        
        return r.status_code
    
    def CheckConnection(self):
        pass



class User(object):

    def __init__(self, telegram_id, full_name, username):
        self.telegram_id = telegram_id
        self.full_name = full_name
        if username!="":
            self.username = username
        else:
            self.username = ""

import json
import requests
import time
import urllib
import os

TOKEN = "***REMOVED***"

class WuersoTestBot:

    def __init__(self):
        self.url = "https://api.telegram.org/bot{}/".format(TOKEN)
        self.last_updates = {}
    
    def send_pic(self, image_path, chat_id, image_loaded=True):
         
        url = self.url + 'sendPhoto?chat_id={}'.format(chat_id)
        multipart_form_data = {
            'photo': open(image_path, 'rb') if not image_loaded else image_path
        }
        print(multipart_form_data)
        response = requests.get(url, files=multipart_form_data)
    
        print(response.status_code)
        print(response.text)

    def get_url(self, url):
        response = requests.get(url)
        print(response.text)
        content = response.content.decode("utf8")
        return content

    def get_json_from_url(self, url):
        content = self.get_url(url)
        js = json.loads(content)
        return js

    def get_updates(self, offset=None):
        url = self.url + "getUpdates?timeout=100"
        if offset:
            url += "&offset={}".format(offset)
        js = self.get_json_from_url(url)
        return js

    def get_last_update_id(self, updates):
        update_ids = []
        for update in updates["result"]:
            update_ids.append(int(update["update_id"]))
        return max(update_ids)

    def echo_all(self, updates):
        for update in updates["result"]:
            try:
                text = update["message"]["text"]
                chat = update["message"]["chat"]["id"]
                self.send_message(text, chat)
            except Exception as e:
                print(e)


    def get_last_chat_id_and_text(self, updates):
        num_updates = len(updates["result"])
        last_update = num_updates - 1
        _text = updates["result"][last_update]["message"]["text"]
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
        return _text, chat_id


    def send_message(self, text, chat_id):
        text = urllib.parse.quote_plus(text)
        url = self.url + "sendMessage?text={}&chat_id={}".format(text, chat_id)
        self.get_url(url)

    def get_triggered_chat_id(self, updates):
        for update in updates["result"]:
            try:
                if update["message"]["text"] == '/start':
                    return update["message"]["chat"]["id"]
            except Exception as e:
                print(e)
                return False        

    def check_triggered(self, updates):
        for update in updates["result"]:
            try:
                return update["message"]["text"] == '/start'
            except Exception as e:
                print(e)
                return False

    def get_player_confirmation(self, chat_id):
        while True:
            updates = self.get_updates(self.last_updates[chat_id])
            if len(updates["result"]) > 0:
                self.last_updates[chat_id] = self.get_last_update_id(updates) + 1
            for update in updates["result"]:
                try:
                    if update["message"]["text"].lower() == 'yes':
                        return True
                    if update["message"]["text"].lower() == 'no':
                        return False
                except Exception as e:
                    print(e)
            
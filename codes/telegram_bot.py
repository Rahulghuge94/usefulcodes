"""
@Author:Rahul Ghuge
Simple telegram bot class to send message and receive.
use
  token="1836363615:AAEb9ttMuvPhddU4rhclUV9cT27kM2GAE88"
  chat_id="643446480"
  bot=Bot(token)
  #send message
  bot.send_message(chat_id,"hi")
  #get updates from user
  bot.get_updates()
"""
import requests
from pytz import timezone
import datetime,time
tz=timezone("Asia/Kolkata")
token="1836363615:AAEb9DRMbvPFddU4xhclUV9cT27kM2GAE88"
chatid=643347080
class Bot:
    def __init__(self,token:str):
        self.token=token
        self.base_url="https://api.telegram.org/bot"
        self.session=requests.session()

    def send_message(self,chat_id,text):
        '''send message to user'''
        payload = {'chat_id': str(chat_id), 'text': text}
        url=self.base_url+self.token+"/sendMessage"
        self.session.post(url,payload)
    def get_updates(self):
        '''return updates from users.'''
        url=self.base_url+self.token+"/getUpdates"
        return self.session.get(url).json()["result"]
    def isCommand(self,response):
        if response["message"]["entities"][0]["type"]=="bot_command":
           return True
        else:
           return False
    def isLatestMessage(self,requests):
        dt=datetime.datetime.now(tz)
        pastTime=dt-datetime.timedelta(seconds=1.4)
        messageTime=datetime.datetime.fromtimestamp(requests["message"]["date"],tz)
        if pastTime<messageTime:
           return True
        else:
           return False


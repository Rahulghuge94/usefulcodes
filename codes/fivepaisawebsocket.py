"""
@author:Rahul Ghuge
5paisa websocket connection which runs on background thread.
usage:
  wspayload=[{ "Exch":"M","ExchType":"D","ScripCode":228699},{ "Exch":"M","ExchType":"D","ScripCode":229411}]
  #App credential. use yours.
  cred={"APP_NAME":"5P51432824",
      "APP_SOURCE":"3280",
      "USER_ID":"AtecCMFIn7y",
      "PASSWORD":"HyOLfBcyo0y",
      "USER_KEY":"JQdmvDR7U5vj47VvtNlVwo2wn2siAOaW",
      "ENCRYPTION_KEY":"Z6Rjhhne5SMQPKtVpLa7ORQlFryWIoECGyVJndAtBn1xJe2gXBwVTfdtIXKxgQMZW"}
  #5paisaCLient object
  client = FivePaisaClient(email="abc@gmail.com", passwd="a@cil9422", dob="19801122",cred=cred)
  client.login()
  client.Login_check()
  #LTP variable stores quotes of scrip subscribed
  LTP={}
  run_ws()
  time.sleep(1.5)
  subscribe(wspayload)
replace credential with your one.
"""
from py5paisa import FivePaisaClient
from py5paisa.order import Order, OrderType, Exchange
import websocket,threading,json,time
#import telegram_

#function to to connect to 5paisa websocket. it allows u to create threaded connection to websocket.
def run_ws():
    global ws #global websocket object.
    global thread
    auth=client.Login_check()
    web_url=f'wss://openfeed.5paisa.com/Feeds/api/chat?Value1={client.Jwt_token}|{client.client_code}'
    ws = websocket.WebSocketApp(web_url,
                              on_open=on_open,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close,
                              cookie=auth)
    thread=threading.Thread(target=ws.run_forever)
    thread.daemon = True
    thread.start()

def on_message(ws,message):
    global LTP #global ltp object
    msg=json.loads(message)
    #print(message)
    LTP.update({str(msg[0]["Token"]) : msg[0]["LastRate"]})

def on_error(ws,error):
    print(error)
            
def on_close(ws):
    print("Streaming Stopped")
     
def on_open(ws):
    print("Streaming Started")
    return
#function to suscribe the list of scrips.e.g wspayload=[{ "Exch":"M","ExchType":"D","ScripCode":228699},{ "Exch":"M","ExchType":"D","ScripCode":230902}]
def subscribe(wsPayload):
    wsPayload=client.Request_Feed('mf','s',wsPayload)
    ws.send(json.dumps(wsPayload))
#function to suscribe the list of scrips.use unsubscribe method from 5paisa
def unsubscribe(wsPayload):
    wsPayload=client.Request_Feed('mf','u',wsPayload)
    ws.send(json.dumps(wsPayload))

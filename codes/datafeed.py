#@author:Rahul Ghuge


import requests
import pandas as pd
s=requests.session()
s.get('https://www.edelweiss.in/market/nse-option-chain')
class datafeed:
      def __init__(self,session=s):
          self.session=session
          self.headers={"accept": "application/json, text/plain, */*","accept-language": "en-US,en;q=0.9,mr;q=0.8,hi;q=0.7","content-type": "application/json;charset=UTF-8",
                        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
                        "sec-ch-ua-mobile": "?0","sec-fetch-dest": "empty","sec-fetch-mode": "cors","sec-fetch-site": "same-site","referrer": "https://www.edelweiss.in/",
                        'use-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'}
      
      def get_option_chain(self,symbol:str,expiry:str):
          '''functon to get live option chain.
             param:
             symbol: string type symbol name. case-insensative.
             expiry: string type expiry dtae in "dd mm yy". i.e. '29 Apr 2021'
                     first three letters of month with first letter capital.
                     e.g. usage
                     #create datafeed object
                     data=datafeed()
                     data.get_option_chain('nifty','29 Apr 2021')
          '''
          seg="OPTIDX"
          if expiry.find(' ')<0:
             return 'Enter correct date with spaces between day, month and year.'
          elif expiry[-3]==" ":
               return 'Enter year in yyyy format.'
          if ["NIFTY","BANKNIFTY","FINNIFTY"].count(symbol.upper())==0:
             seg="OPTSTK"
          data=str({"aTyp": seg,"exp": expiry,"uSym": symbol.upper()})
          response=self.session.post("https://ewmw.edelweiss.in/api/Market/optionchaindetails",headers=self.headers,data=data)
          if response.status_code==200:
             temp=response.json()['opChn']
             print(temp)
             ce=[]
             pe=[]
             data=[]
             col=['trdSym', 'stkPrc','sym', 'o', 'h', 'l', 'c', 'ltp','bidPr', 'askPr', 'vol', 'chg', 'chgP', 'bdSz', 'akSz', 'opInt', 'opIntChg', 'opIntChgP', 'spot', 'ntByQty', 'ntSlQty', 'ltpivspt', 'ntTrdVal']
             for i in temp:
                 ce.append([i['ceQt']['trdSym'],i['stkPrc'],i['ceQt']['sym'],i['ceQt']['o'],i['ceQt']['h'],i['ceQt']['l'],i['ceQt']['c'],i['ceQt']['ltp'],i['ceQt']['bidPr'],i['ceQt']['askPr'],i['ceQt']['vol'],
                              i['ceQt']['chg'],i['ceQt']['chgP'],i['ceQt']['bdSz'],i['ceQt']['akSz'],i['ceQt']['opInt'],i['ceQt']['opIntChg'],i['ceQt']['opIntChgP'],i['ceQt']['spot'],
                              i['ceQt']['ntByQty'],i['ceQt']['ntSlQty'],i['ceQt']['ltpivspt'],i['ceQt']['ntTrdVal']])
                 pe.append([i['peQt']['trdSym'],i['stkPrc'],i['peQt']['sym'],i['peQt']['o'],i['peQt']['h'],i['peQt']['l'],i['peQt']['c'],i['peQt']['ltp'],i['peQt']['bidPr'],i['peQt']['askPr'],i['peQt']['vol'],
                              i['peQt']['chg'],i['peQt']['chgP'],i['peQt']['bdSz'],i['peQt']['akSz'],i['peQt']['opInt'],i['peQt']['opIntChg'],i['peQt']['opIntChgP'],i['peQt']['spot'],
                              i['peQt']['ntByQty'],i['peQt']['ntSlQty'],i['peQt']['ltpivspt'],i['peQt']['ntTrdVal']])
             dfce=pd.DataFrame(ce,columns=col)
             dfpe=pd.DataFrame(pe,columns=col)
             data=dfce.merge(dfpe,how='inner',on='stkPrc')
             return data
          else:
             return response.text
      def quote(self,symbol:str,ltponly=None):
          ''' function to get live quotes of derivative contract.
             param:
             symbol:sting symbol name nifty.e.g 'nifty~2021042914500ce'. must inlcude '~' index name.
             e.g. usage
                     #create datafeed object
                     data=datfeed()
                     data.quote('nify~202104291400pe')
          '''
          symbol=symbol.lower()
          null=0
          temp=self.session.get('https://ewmw.edelweiss.in/api/Market/Process/QuoteOption/'+symbol,headers=self.headers).json()
          col=['Symbol','FuturePrice', 'LTP', 'ChangeInLTP','ChangeinLTPPerc', 'HighDay', 'LowDay', 'PreviousClose', 'Volume', 'OI', 'OIChange', 'StrikePrice', 'ExpiryDate']
          qt=eval(temp)['JsonData']['QuoteOptionLists']
          '''if not ltponly:
             der=[qt['Symbol'],qt['FuturePrice'],qt['LTP'],qt['ChangeInLTP'],qt['ChangeinLTPPerc'],
                 qt['HighDay'],qt['LowDay'],qt['PreviousClose'],qt['Volume'],qt['OI'],qt['OIChange'],qt['StrikePrice'],qt['ExpiryDate']]
             return pd.DataFrame(der,col)
          else:
             return qt['LTP']'''
          return qt

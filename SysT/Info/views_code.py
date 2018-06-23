import json
import requests
from . import AI_code, streaming
import time
import threading

'''
streamingを使うときはoanda.comのapiでなくstreamをつかう
'''
'''
AI INFO
'''
AI = AI_code.AI_manager(["USD_JPY","AUD_JPY"])#AIクラスの初期化

'''
POSTリクエストが行われるとAIが起動，ストップ
'''
def manage_trade(request):
    if(request.POST):
        if(AI.operation_info):
            AI.stop()
        else:
            AI.start()           
            
    return AI.operation_info


class Polling_Manager():
    def __init__(self, access_token, account_id):
        self.change_flg=False#通信内容変更の有無の確認用
        self.access_token=access_token#oanda apiに必要なaccess token
        self.account_id=account_id
        self.now_rate={}#現在のレートを保持する変数
        self.AccountInfo=[]#現在の口座情報を保持する変数
        self.TradeInfo=[]#現在のポジション情報を保持する変数
        self.get_account_info()#現在の口座情報の初期化(取得)
        self.get_trade_info()#現在のポジションの初期化(取得)
        self.instruments=["USD_JPY"]#取引に使う通貨ペア
        self.ret_dict={}#クライアントに送るjsonまとめ
        self.check_ret_dict()
        self.stop_event=threading.Event()#レートストリームを止めるためのイベント
        self.thread = threading.Thread(target=self.rate_streaming)#レートストリームのためのマルチスレッド化
        self.thread.start()#レートストリームを開始
        
    '''
    自分の口座情報の取得関数
    '''

    def get_account_info(self):
        url='https://api-fxpractice.oanda.com'+'/v1/accounts/'+self.account_id
        headers={'Authorization' : 'Bearer ' + self.access_token,}
        try:
            req=requests.get(url, headers = headers)
            if(req.status_code==200):
                account_info=json.loads(req.text)
                self.AccountInfo=[account_info["balance"],
                             account_info["unrealizedPl"],
                             account_info["realizedPl"],
                             account_info["marginUsed"],
                             account_info["marginAvail"],
                             ]
        except Exception as e:
            print(e)
            return e

    '''
    レートストリーム
    '''
    def rate_streaming(self):
        url='https://stream-fxpractice.oanda.com'+'/v1/prices'
        headers={'Authorization' : 'Bearer ' + self.access_token,}
        params={'instruments' : self.instruments[0], 'accountId':self.account_id}
        try:
            s=requests.Session()
            req=requests.Request('GET',url, headers=headers, params=params)
            pre=req.prepare()
            resp=s.send(pre, stream=True, verify=True)
        except Exception as e:
            print("Caught exception when connect api")
            s.close()
            return e
        
        for line in resp.iter_lines(1):
            if line and self.stop_event.is_set()==False:
                try:
                    line=line.decode("utf-8")
                    rate=json.loads(line)
                except Exception as e:
                    print("Caught exception when coverting message")
                    return e

                if 'tick' in rate:
                    self.now_rate=rate["tick"]
                    self.get_account_info()
                    self.get_trade_info()
                    self.check_ret_dict()
                    self.change_flg=True
            else:
                return
                    
    '''
    取引情報の計算
    '''
    def culc_trade_info(self):
        if len(self.now_rate)==0:
            print("Can not get now_rate")
            return
        for t in self.TradeInfo:
            if(t[3]=="buy"):
                t.append(self.now_rate['bid'])
                t.append(round(t[2]*(float(t[5])-float(t[4])), 3))
                t.append(round(100*(float(t[5])-float(t[4])),3))
                t.append(round(100*t[6]/(float(t[4])*t[2]), 2))
            elif(t[3]=="sell"):
                t.append(self.now_rate['ask'])
                t.append(round(t[2]*(float(t[4])-float(t[5])), 3))
                t.append(round(100*(float(t[4])-float(t[5])),3))
                t.append(round(100*t[6]/(float(t[4])*t[2]), 2))

    '''
    取引状況の取得
    '''
    def get_trade_info(self):
        url='https://api-fxpractice.oanda.com'+'/v1/accounts/'+self.account_id+'/trades'
        headers={'Authorization' : 'Bearer ' + self.access_token,}
        try:
            req=requests.get(url, headers = headers)
            if(req.status_code==200):
                trade_info=json.loads(req.text)
                i=1
                self.TradeInfo=[]
                for r in trade_info['trades']:
                    self.TradeInfo.append([i,r["instrument"],r["units"],r["side"],
                                      round(float(r["price"]),3)])
                    i += 1
            self.culc_trade_info()
        except Exception as e:
            print(e)
            return e

    def stop(self):
        self.stop_event.set()
        self.thread.join()

    '''
    Trade_Infoを初期化して調整するときに返却用のjsonの参照から外れるためもう一度参照させるための関数
    '''
    def check_ret_dict(self):
        self.ret_dict["ACCOUNT_INFO"]=self.AccountInfo
        self.ret_dict["TRADE_INFO"]=self.TradeInfo        
        self.ret_dict["OPERATION_STATE"]=AI.operation_info#今AIがマルチスレッドで動いているかの確認のための変数

'''
access_token, idの定義(改善の余地あり)
クライアントに渡すためのクラス初期化
'''
access_token = 'e777fc0c0a7aedb89e00f91e15a7b415-ac361a890d2fa25b195ba4dbe825f38b'
account_id = '2828919'
x=Polling_Manager(access_token, account_id)

'''
viewで呼び出されて変更があった時のみデータを渡す関数
'''
def get_info(request):
    while True:
        if(x.change_flg and len(x.AccountInfo) is not 0):
            if(len(x.TradeInfo) is not 0):
                if(len(x.TradeInfo[0]) is 9):
                    x.change_flg=False
                    return x.ret_dict
            else:
                x.change_flg=False
                return x.ret_dict







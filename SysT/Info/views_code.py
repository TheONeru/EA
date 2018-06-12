import json
import requests
import asyncio
from . import AI_code
import time
'''
Get infomation from oanda api asynchronous
'''
def async_get(uri, ret):
    if(len(uri)==2):        
        req=requests.get(uri[0], headers = uri[1], timeout=1)
        if(req.status_code ==200):
            ret.append(req.text)            
    elif(len(uri)==3):
        req=requests.get(uri[0], headers = uri[1], params=uri[2], timeout=1)
        if(req.status_code ==200):
            ret.append(req.text)

def async(uri_list):
    ret=[]
    #loop = asyncio.new_event_loop()
    #asyncio.set_event_loop(loop)
    cors=[async_get(uri, ret) for uri in uri_list]
    #result=asyncio.gather(*cors)
    #loop.run_until_complete(result)
    #loop.close()
    return ret

'''
It is main view
'''
def get_info(request):
    domainDict = { 'live' : 'stream-fxtrade.oanda.com',
               'demo' : 'api-fxpractice.oanda.com' }
    environment = "demo" 
    domain = domainDict[environment] 
    access_token = 'e777fc0c0a7aedb89e00f91e15a7b415-ac361a890d2fa25b195ba4dbe825f38b'
    account_id = '2828919'
    instruments = 'USD_JPY'
    account_url = "https://" + domain + "/v1/accounts/"+account_id
    trades_url=account_url+'/trades'
    rate_url="https://" + domain + "/v1/prices"
    headers = {'Authorization' : 'Bearer ' + access_token,
                  }
    rate_params = {'instruments' : 'USD_JPY'}
    uri=[[account_url, headers],[trades_url,headers],[rate_url,headers,rate_params]]
    info = async(uri)
    AccountInfo=[]
    TradeInfo=[]
    now_rate={}
    if(len(info)==3):        
        for info_ in info:
            if(info_.find("trades")!=-1):
                trade_info=json.loads(info_)
                i=1
                for r in trade_info['trades']:
                    TradeInfo.append([i,r["instrument"],r["units"],r["side"],
                                         round(float(r["price"]),3),'','','',''])
                    i += 1
            elif(info_.find("accountId")!=-1):
                account_info=json.loads(info_)
                AccountInfo=[account_info["balance"],account_info["unrealizedPl"],
                             account_info["realizedPl"],account_info["marginUsed"],
                             account_info["marginAvail"]]
            elif(info_.find("prices") != -1):
                now_rate=json.loads(info_)                

        for t in TradeInfo:
            if(t[3]=="buy"):
                t[5]=now_rate['prices'][0]['bid']
                t[6]=round(t[2]*(float(t[5])-float(t[4])), 3)
                t[7]=round(100*(float(t[5])-float(t[4])),3)
                t[8]=round(100*t[6]/(float(t[4])*t[2]), 2)
            elif(t[3]=="sell"):
                t[5]=now_rate['prices'][0]['ask']
                t[6]=round(t[2]*(float(t[4])-float(t[5])), 3)
                t[7]=round(100*(float(t[4])-float(t[5])),3)
                t[8]=round(100*t[6]/(float(t[4])*t[2]), 2)
        dict_={}
        dict_["ACCOUNT_INFO"]=AccountInfo
        dict_["TRADE_INFO"]=TradeInfo
        operation_info=manage_trade(request)
        dict_["OPERATION_STATE"]=operation_info
        
        return dict_
    else:
        return "Now we can't get information, Please contact"



'''
AI INFO
'''

AI = AI_code.AI_manager(["USD_JPY","AUD_JPY"])

def manage_trade(request):
    if(request.POST):
        if(AI.operation_info):
            AI.stop()
        else:
            AI.start()           
            
    return AI.operation_info
    
        







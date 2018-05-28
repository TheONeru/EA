from django.shortcuts import render
from django.http.response import HttpResponse
import datetime
import json
import requests
import asyncio
# Create your views here.
async def async_get(url, headers, ret):
    req=requests.get(url, headers = headers)
    if(req.status_code ==200):
        ret.append(req.text)

def async(urls, headers):
    ret=[]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    cors=[async_get(u, headers, ret) for u in urls]
    result=asyncio.gather(*cors)
    loop.run_until_complete(result)
    loop.close()
    print(ret)
    return ret

def account_info(request):
    domainDict = { 'live' : 'stream-fxtrade.oanda.com',
               'demo' : 'api-fxpractice.oanda.com' }
    environment = "demo" 
    domain = domainDict[environment] 
    access_token = 'e777fc0c0a7aedb89e00f91e15a7b415-ac361a890d2fa25b195ba4dbe825f38b'
    account_id = '2828919'
    instruments = 'USD_JPY'
    account_url = "https://" + domain + "/v1/accounts/"+account_id
    position_url=account_url+'/trades'
    urls=[account_url, position_url]
    headers = {'Authorization' : 'Bearer ' + access_token,
                  }
    async(urls, headers)  
    
    
    AccountInfo=[]
    PositionInfo=[]
    '''
    try:
        
Get account informations from oanda api

        
        s = requests.Session()      
        
        #params = {'instruments' : instruments, 'accountId' : account_id}
        params={'account_id':account_id}
        req = requests.Request('GET', account_url, headers = headers)
        pre = req.prepare()
        res = s.send(pre, stream = True, verify = True)
        #resp is code of responce, if you check responsetext resp.text
        print(res.text)
        if(res.status_code == 200):
            resp=json.loads(res.text)
            AccountInfo=[resp["balance"],resp["unrealizedPl"],resp["realizedPl"],resp["marginUsed"],resp["marginAvail"]]
        else:
            print("Error:Cant't Get Account Information")

Get positions I'm holding now from oanda api
        req = requests.Request('GET', position_url, headers = headers)
        pre = req.prepare()
        res = s.send(pre, stream = True, verify = True)
        print(res.text)
        if(res.status_code == 200):
            resp=json.loads(res.text)
            i=1
            for r in resp["trades"]:
                print(r)
                PositionInfo.append([i,r["instrument"],r["units"],r["side"],r["price"],'','','',''])
                i += 1
        else:
            print("Error:Can't Get Positions Information")
        
        #req = requests.Request('GET', url, headers = headers, params = params)
        
    except Exception as e:
        s.close()
        print(str(e))
'''    
    dict_={}
    dict_["ACCOUNT_INFO"]=AccountInfo
    dict_["POSITION_INFO"]=PositionInfo
    print(AccountInfo)
    print(PositionInfo)
    return render(request, 'Info/index.html', dict_)

def position_info(request):
    return HttpResponse("This page is position_info")


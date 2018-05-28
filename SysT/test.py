from django.shortcuts import render
from django.http.response import HttpResponse
import datetime
import requests
import json

domainDict = { 'live' : 'stream-fxtrade.oanda.com',
               'demo' : 'api-fxpractice.oanda.com' }
environment = "demo" # Replace this 'live' if you wish to connect to the live environment 
domain = domainDict[environment] 
access_token = 'e777fc0c0a7aedb89e00f91e15a7b415-ac361a890d2fa25b195ba4dbe825f38b'
account_id = '2828919'
instruments = 'USD_JPY'
username='pm741154'
try:
    s = requests.Session()
    url = "https://" + domain + "/v1/accounts/"+account_id+"/trades"
    print(url)
    headers = {'Authorization' : 'Bearer ' + access_token,
                # 'X-Accept-Datetime-Format' : 'unix'
              }
    #params = {'instruments' : instruments, 'accountId' : account_id}
    params={'username':account_id}
    #req = requests.Request('GET', url, headers = headers, params = params)
    req = requests.Request('GET', url, headers = headers)
    pre = req.prepare()
    resp = s.send(pre, stream = True, verify = True)
    print(resp.text)
    res=json.loads(resp.text)#change type str to dict
    print(res)
except Exception as e:
    s.close()
    print(str(e))

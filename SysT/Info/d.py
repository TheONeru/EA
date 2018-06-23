import json
import requests
access_token = 'e777fc0c0a7aedb89e00f91e15a7b415-ac361a890d2fa25b195ba4dbe825f38b'
account_id = '2828919'
url='https://api-fxpractice.oanda.com'+'/v1/accounts/'+account_id+'/trades'
headers={'Authorization' : 'Bearer ' + access_token,}
params={'instruments' : "USD_JPY", 'accountId':account_id}
r = requests.get(url,headers=headers)
print(r.text)
for line in r.iter_lines():

    # filter out keep-alive new lines
    if line:
        print(line)
        decoded_line = line.decode('utf-8')
        print(json.loads(decoded_line))

#stream can get only now_rate

"""
Demonstrates streaming feature in OANDA open api
To execute, run the following command:
python streaming.py [options]
To show heartbeat, replace [options] by -b or --displayHeartBeat
"""
import requests
import json

from optparse import OptionParser

def connect_to_stream(url, headers, params):
    try:
        #s = requests.Session()
        req = requests.get(url, headers = headers, params = params, stream=True)
        #pre = req.prepare()
        #resp = s.send(pre, stream = True, verify = True)
        print(req.text)
        return req
    except Exception as e:
        #s.close()
        print("Caught exception when connecting to stream\n" + str(e)) 

def connect_manager(url, headers, params, now_rate, event):
    print("Rate Start")
    response = connect_to_stream(url, headers, params)    
    if response.status_code != 200:
        print(response.text)
        return
    for line in response.iter_lines(chunk_size=10):
        if event.is_set():
            return
        if line:
            try:
                print(line)
                line = line.decode('utf-8')
                print(line)
                msg = json.loads(line)
                print(line)#dict 型になっていない
                #now_rate=msg[]
            except Exception as e:
                print("Caught exception when converting message into json\n" + str(e))
                return
            if "instrument" in msg or "tick" in msg or displayHeartbeat:
                print(line)

def get_info(url, headers, params, now_rate, event):
    connect_manager(url, headers, params, now_rate, event)


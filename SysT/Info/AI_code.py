import time
import threading
'''
TradeAI
'''
class trade_AI():

    def __init__(self, instruments):
        self.stop_event = threading.Event()
        self.inc_event = threading.Event()
        self.info_event = threading.Event()
        self.instruments = instruments

        #スレッドの作成と開始
        self.thread = threading.Thread(target = self.target)
    def target(self):
        
        while not self.stop_event.is_set():
            time.sleep(1)
            print(self.instruments)
            

    def start(self):
        self.thread.start()

    def stop(self):
        """スレッドを停止させる"""
        self.stop_event.set()
        self.thread.join()    #スレッドが停止するのを待つ
'''
class Logger_AI():

    def __init__(self)

'''
class AI_manager():

    def __init__(self, instruments_list):
        self.trade_AI_list=[]
        self.operation_info=False
        for i in instruments_list:
            self.trade_AI_list.append(trade_AI(i))           

    def start(self):
        for i in self.trade_AI_list:
            i.start()
        self.operation_info=True

    def stop(self):
        for i in self.trade_AI_list:
            i.stop()        
        self.operation_info=False


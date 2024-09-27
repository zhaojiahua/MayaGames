import time
import threading
from maya import cmds
from maya import utils
#定义一个Tick函数,每帧都执行
def Tick():
    print('tick')
#每0.02毫秒调用一次的Update函数
def Update():
    print('update')
#线程调用的函数(游戏运行时一直运行中的线程)
def MainRunThread():
    start_time=time.time()
    current_time=time.time()
    count=0
    while True:
        utils.executeInMainThreadWithResult(Tick)
        current_time = time.time()
        if current_time-start_time > 0.02:
            utils.executeInMainThreadWithResult(Update)
            start_time=current_time
mainrunthread=threading.Thread(target=MainRunThread)
mainrunthread.start()

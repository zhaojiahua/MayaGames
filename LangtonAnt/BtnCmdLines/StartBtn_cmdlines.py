import threading
import MainTick as MT
if Gl.gamerun:
    Gl.gamerun=False
    cmds.button('StartStopBtn',e=1,label='||Start>>',bgc=[0.2,0.2,0.4])
else:
    Gl.gamerun=True
    cmds.button('StartStopBtn',e=1,label='| |Stop...| |',bgc=[0.4,0.2,0.2])
    mainrunthread=threading.Thread(target=MT.MainRunThread)
    mainrunthread.start()
import time
from Globals import ZjhGlobals
time.sleep(1)
for i in range(len(ZjhGlobals.sortedScores)):
    cmds.text('paimingtext'+str(i+1),e=1,visible=1)
    cmds.text('zhanghaotext'+str(i+1),e=1,l=ZjhGlobals.sortedScores[i][0],visible=1)
    cmds.text('defentext'+str(i+1),e=1,l=str(ZjhGlobals.sortedScores[i][1]),visible=1)
    cmds.text('defenlvtext'+str(i+1),e=1,l=str(ZjhGlobals.accountScoresrate[ZjhGlobals.sortedScores[i][0]]),visible=1)
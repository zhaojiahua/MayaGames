import time
from Globals import ZjhGlobals
cmds.columnLayout('zjhJiFenLayout1',e=1,visible=1)
time.sleep(1)
for i in range(len(ZjhGlobals.sortedScores)):
    cmds.text(l='第'+str(i+1)+'名:',height=20,bgc=[0.31,0.3,0.3],parent='zjhpaimingcol')
    cmds.text(l=ZjhGlobals.sortedScores[i][0],height=20,bgc=[0.31,0.3,0.3],parent='zjhzhanghaocol')
    cmds.text(l=str(ZjhGlobals.sortedScores[i][1]),height=20,bgc=[0.31,0.3,0.3],parent='zjhdefencol')
    cmds.text(l=str(ZjhGlobals.accountScoresrate[ZjhGlobals.sortedScores[i][0]]),height=20,bgc=[0.31,0.3,0.3],parent='zjhdefenlvcol')
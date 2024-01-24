from maya import utils
import random
import json
import time
import threading as thrd
from Globals import projectPath
from Globals import ZjhGlobals
from CommonFuns import *

###全局变量
global gameRun
gameRun=True
global interval
interval=1.0
global FrameAllIndex	#用来记录所有方块的填充状况
FrameAllIndex=[]	#一共19列,每列有36个元素
for i in range(19):
	FrameAllIndex.append([0]*36)
global theAcTetris
theAcTetris=''
global theAcButtomBricks
theAcButtomBricks=[]
global theAcLeftBricks
theAcLeftBricks=[]
global theAcRightBricks
theAcRightBricks=[]
###全局变量

restartBtnCommand_lines=Getcmdlines(projectPath+'scripts/tetris_scripts/CommandsLines/restartBtnCommand_lines.py')
gobackBtnCommand_lines=Getcmdlines(projectPath+'scripts/tetris_scripts/CommandsLines/gobackBtnCommand_lines.py')
nextLevelBtnCommand_lines=Getcmdlines(projectPath+'scripts/tetris_scripts/CommandsLines/nextLevelBtnCommand_lines.py')
addJiFenBangUICommand_lines=Getcmdlines(projectPath+'scripts/tetris_scripts/CommandsLines/addJiFenBangUI_lines.py')

#颜色和层名字的枚举对应
colorlayers={0:'O_colorLayer',1:'L_colorLayer',2:'J_colorLayer',3:'Z_colorLayer',4:'T_colorLayer',5:'S_colorLayer',6:'I_colorLayer'}
#颜色和shadingEngine的对应
colorSets={0:'O_colormatSG',1:'L_colormatSG',2:'J_colormatSG',3:'Z_colormatSG',4:'T_colormatSG',5:'S_colormatSG',6:'I_colormatSG'}
#颜色层和16进制颜色编码的对应
colorX0codes={0:'0xFFFFFF',1:'0xFF3366',2:'0x66CC00',3:'0x3399FF',4:'0x000000'}

#游戏结束和游戏胜利的界面
def CreateGameOverWindow():
	if cmds.window('zjhGameOverWindow',q=1,ex=1):
		cmds.deleteUI('zjhGameOverWindow')
	cmds.loadUI(uiFile=projectPath+'scripts/brickGame_scripts/gameoverui.ui')
	cmds.showWindow('zjhGameOverWindow')
	cmds.window('zjhGameOverWindow',e=1,wh=[550,300],bgc=[0.31,0.28,0.3],visible=0)
	cmds.button('restartBtn',e=1,bgc=[0.38,0.3,0.31],c=restartBtnCommand_lines)
	cmds.button('gobackBtn',e=1,bgc=[0.38,0.3,0.31],c=gobackBtnCommand_lines)
	#积分榜
	cmds.columnLayout('zjhJiFenLayout1',parent='zjhGameOverWindow',adjustableColumn=1,visible=1)
	cmds.text('jifenbang',l='|----- >>>积 |||---分---||| 榜<<< -----|',height=50,bgc=[0.55,0.38,0.38],font='boldLabelFont')
	cmds.rowLayout('zjhJFBrowLayout1',numberOfColumns=4,ad4=2)
	cmds.columnLayout('zjhpaimingcol',adjustableColumn=1)
	cmds.text(l='排名:',height=30,bgc=[0.35,0.3,0.3])
	cmds.setParent('..')
	cmds.columnLayout('zjhzhanghaocol',adjustableColumn=1)
	cmds.text(l='		 帐号:',height=30,bgc=[0.35,0.3,0.3])
	cmds.setParent('..')
	cmds.columnLayout('zjhdefencol',adjustableColumn=1)
	cmds.text(l='	得分:',height=30,bgc=[0.35,0.3,0.3])
	cmds.setParent('..')
	cmds.columnLayout('zjhdefenlvcol',adjustableColumn=1)
	cmds.text(l='	得分率:',height=30,bgc=[0.35,0.3,0.3])
	#前四名
	for i in range(4):
		cmds.text('paimingtext'+str(i+1),l='第'+str(i+1)+'名:',height=20,bgc=[0.31,0.3,0.3],parent='zjhpaimingcol',visible=0)
		cmds.text('zhanghaotext'+str(i+1),height=20,bgc=[0.31,0.3,0.3],parent='zjhzhanghaocol',visible=0)
		cmds.text('defentext'+str(i+1),height=20,bgc=[0.31,0.3,0.3],parent='zjhdefencol',visible=0)
		cmds.text('defenlvtext'+str(i+1),height=20,bgc=[0.31,0.3,0.3],parent='zjhdefenlvcol',visible=0)
def CreateGameWinWindow():
	if cmds.window('zjhGameWinWindow',q=1,ex=1):
		cmds.deleteUI('zjhGameWinWindow')
	cmds.loadUI(uiFile=projectPath+'scripts/brickGame_scripts/gamewinui.ui')
	cmds.showWindow('zjhGameWinWindow')
	cmds.window('zjhGameWinWindow',e=1,wh=[550,300],bgc=[0.28,0.31,0.3],visible=0)
	cmds.button('restartBtn_win',e=1,bgc=[0.3,0.32,0.31],c=restartBtnCommand_lines)
	cmds.button('nextLevelBtn',e=1,bgc=[0.3,0.32,0.31],c=nextLevelBtnCommand_lines)

def O_TetrisRote(inTetris):
	pass
def L_TetrisRote_0(inTetris):
	l_bricks=cmds.listRelatives(inTetris)
	cmds.setAttr(l_bricks[0]+'.tx',0)
	cmds.setAttr(l_bricks[0]+'.ty',0)
	cmds.setAttr(l_bricks[1]+'.tx',50)
	cmds.setAttr(l_bricks[1]+'.ty',50)
	cmds.setAttr(l_bricks[2]+'.tx',0)
	cmds.setAttr(l_bricks[2]+'.ty',50)
	cmds.setAttr(l_bricks[3]+'.tx',100)
	cmds.setAttr(l_bricks[3]+'.ty',50)
	cmds.setAttr(inTetris+'.direction',1)
def L_TetrisRote_1(inTetris):
	l_bricks=cmds.listRelatives(inTetris)
	cmds.setAttr(l_bricks[0]+'.tx',50)
	cmds.setAttr(l_bricks[0]+'.ty',100)
	cmds.setAttr(l_bricks[1]+'.tx',50)
	cmds.setAttr(l_bricks[1]+'.ty',0)
	cmds.setAttr(l_bricks[2]+'.tx',50)
	cmds.setAttr(l_bricks[2]+'.ty',50)
	cmds.setAttr(l_bricks[3]+'.tx',0)
	cmds.setAttr(l_bricks[3]+'.ty',100)
	cmds.setAttr(inTetris+'.direction',2)
def L_TetrisRote_2(inTetris):
	l_bricks=cmds.listRelatives(inTetris)
	cmds.setAttr(l_bricks[0]+'.tx',0)
	cmds.setAttr(l_bricks[0]+'.ty',0)
	cmds.setAttr(l_bricks[1]+'.tx',50)
	cmds.setAttr(l_bricks[1]+'.ty',0)
	cmds.setAttr(l_bricks[2]+'.tx',100)
	cmds.setAttr(l_bricks[2]+'.ty',0)
	cmds.setAttr(l_bricks[3]+'.tx',100)
	cmds.setAttr(l_bricks[3]+'.ty',50)
	cmds.setAttr(inTetris+'.direction',3)
def L_TetrisRote_3(inTetris):
	l_bricks=cmds.listRelatives(inTetris)
	cmds.setAttr(l_bricks[0]+'.tx',0)
	cmds.setAttr(l_bricks[0]+'.ty',0)
	cmds.setAttr(l_bricks[1]+'.tx',50)
	cmds.setAttr(l_bricks[1]+'.ty',0)
	cmds.setAttr(l_bricks[2]+'.tx',0)
	cmds.setAttr(l_bricks[2]+'.ty',50)
	cmds.setAttr(l_bricks[3]+'.tx',0)
	cmds.setAttr(l_bricks[3]+'.ty',100)
	cmds.setAttr(inTetris+'.direction',0)
L_TetrisRotes={0:L_TetrisRote_0,1:L_TetrisRote_1,2:L_TetrisRote_2,3:L_TetrisRote_3}
#传入L_Tetris的四块组(每个Tetris都有四个方块组成),它会根据其direction的属性旋转
def L_TetrisRote(inTetris):
	L_TetrisRotes[cmds.getAttr(inTetris+'.direction')](inTetris)
def J_TetrisRote_0(inTetris):
	l_bricks=cmds.listRelatives(inTetris)
	cmds.setAttr(l_bricks[0]+'.tx',0)
	cmds.setAttr(l_bricks[0]+'.ty',0)
	cmds.setAttr(l_bricks[1]+'.tx',-50)
	cmds.setAttr(l_bricks[1]+'.ty',0)
	cmds.setAttr(l_bricks[2]+'.tx',-50)
	cmds.setAttr(l_bricks[2]+'.ty',50)
	cmds.setAttr(l_bricks[3]+'.tx',50)
	cmds.setAttr(l_bricks[3]+'.ty',0)
	cmds.setAttr(inTetris+'.direction',1)
def J_TetrisRote_1(inTetris):
	l_bricks=cmds.listRelatives(inTetris)
	cmds.setAttr(l_bricks[0]+'.tx',0)
	cmds.setAttr(l_bricks[0]+'.ty',100)
	cmds.setAttr(l_bricks[1]+'.tx',-50)
	cmds.setAttr(l_bricks[1]+'.ty',0)
	cmds.setAttr(l_bricks[2]+'.tx',-50)
	cmds.setAttr(l_bricks[2]+'.ty',50)
	cmds.setAttr(l_bricks[3]+'.tx',-50)
	cmds.setAttr(l_bricks[3]+'.ty',100)
	cmds.setAttr(inTetris+'.direction',2)
def J_TetrisRote_2(inTetris):
	l_bricks=cmds.listRelatives(inTetris)
	cmds.setAttr(l_bricks[0]+'.tx',50)
	cmds.setAttr(l_bricks[0]+'.ty',0)
	cmds.setAttr(l_bricks[1]+'.tx',-50)
	cmds.setAttr(l_bricks[1]+'.ty',50)
	cmds.setAttr(l_bricks[2]+'.tx',0)
	cmds.setAttr(l_bricks[2]+'.ty',50)
	cmds.setAttr(l_bricks[3]+'.tx',50)
	cmds.setAttr(l_bricks[3]+'.ty',50)
	cmds.setAttr(inTetris+'.direction',3)
def J_TetrisRote_3(inTetris):
	l_bricks=cmds.listRelatives(inTetris)
	cmds.setAttr(l_bricks[0]+'.tx',0)
	cmds.setAttr(l_bricks[0]+'.ty',0)
	cmds.setAttr(l_bricks[1]+'.tx',-50)
	cmds.setAttr(l_bricks[1]+'.ty',0)
	cmds.setAttr(l_bricks[2]+'.tx',0)
	cmds.setAttr(l_bricks[2]+'.ty',50)
	cmds.setAttr(l_bricks[3]+'.tx',0)
	cmds.setAttr(l_bricks[3]+'.ty',100)
	cmds.setAttr(inTetris+'.direction',0)
J_TetrisRotes={0:J_TetrisRote_0,1:J_TetrisRote_1,2:J_TetrisRote_2,3:J_TetrisRote_3}
def J_TetrisRote(inTetris):
	J_TetrisRotes[cmds.getAttr(inTetris+'.direction')](inTetris)
def Z_TetrisRote_0(inTetris):
	l_bricks=cmds.listRelatives(inTetris)
	cmds.setAttr(l_bricks[0]+'.tx',0)
	cmds.setAttr(l_bricks[0]+'.ty',0)
	cmds.setAttr(l_bricks[1]+'.tx',0)
	cmds.setAttr(l_bricks[1]+'.ty',50)
	cmds.setAttr(l_bricks[2]+'.tx',50)
	cmds.setAttr(l_bricks[2]+'.ty',50)
	cmds.setAttr(l_bricks[3]+'.tx',50)
	cmds.setAttr(l_bricks[3]+'.ty',100)
	cmds.setAttr(inTetris+'.direction',1)
def Z_TetrisRote_1(inTetris):
	l_bricks=cmds.listRelatives(inTetris)
	cmds.setAttr(l_bricks[0]+'.tx',0)
	cmds.setAttr(l_bricks[0]+'.ty',0)
	cmds.setAttr(l_bricks[1]+'.tx',50)
	cmds.setAttr(l_bricks[1]+'.ty',0)
	cmds.setAttr(l_bricks[2]+'.tx',0)
	cmds.setAttr(l_bricks[2]+'.ty',50)
	cmds.setAttr(l_bricks[3]+'.tx',-50)
	cmds.setAttr(l_bricks[3]+'.ty',50)
	cmds.setAttr(inTetris+'.direction',2)
def Z_TetrisRote_2(inTetris):
	l_bricks=cmds.listRelatives(inTetris)
	cmds.setAttr(l_bricks[0]+'.tx',0)
	cmds.setAttr(l_bricks[0]+'.ty',0)
	cmds.setAttr(l_bricks[1]+'.tx',0)
	cmds.setAttr(l_bricks[1]+'.ty',50)
	cmds.setAttr(l_bricks[2]+'.tx',50)
	cmds.setAttr(l_bricks[2]+'.ty',50)
	cmds.setAttr(l_bricks[3]+'.tx',50)
	cmds.setAttr(l_bricks[3]+'.ty',100)
	cmds.setAttr(inTetris+'.direction',3)
def Z_TetrisRote_3(inTetris):
	l_bricks=cmds.listRelatives(inTetris)
	cmds.setAttr(l_bricks[0]+'.tx',0)
	cmds.setAttr(l_bricks[0]+'.ty',0)
	cmds.setAttr(l_bricks[1]+'.tx',50)
	cmds.setAttr(l_bricks[1]+'.ty',0)
	cmds.setAttr(l_bricks[2]+'.tx',0)
	cmds.setAttr(l_bricks[2]+'.ty',50)
	cmds.setAttr(l_bricks[3]+'.tx',-50)
	cmds.setAttr(l_bricks[3]+'.ty',50)
	cmds.setAttr(inTetris+'.direction',0)
Z_TetrisRotes={0:Z_TetrisRote_0,1:Z_TetrisRote_1,2:Z_TetrisRote_2,3:Z_TetrisRote_3}
def Z_TetrisRote(inTetris):
	Z_TetrisRotes[cmds.getAttr(inTetris+'.direction')](inTetris)
def I_TetrisRote_0(inTetris):
	l_bricks=cmds.listRelatives(inTetris)
	cmds.setAttr(l_bricks[0]+'.tx',0)
	cmds.setAttr(l_bricks[0]+'.ty',0)
	cmds.setAttr(l_bricks[1]+'.tx',-50)
	cmds.setAttr(l_bricks[1]+'.ty',0)
	cmds.setAttr(l_bricks[2]+'.tx',50)
	cmds.setAttr(l_bricks[2]+'.ty',0)
	cmds.setAttr(l_bricks[3]+'.tx',100)
	cmds.setAttr(l_bricks[3]+'.ty',0)
	cmds.setAttr(inTetris+'.direction',1)
def I_TetrisRote_1(inTetris):
	l_bricks=cmds.listRelatives(inTetris)
	cmds.setAttr(l_bricks[0]+'.tx',0)
	cmds.setAttr(l_bricks[0]+'.ty',0)
	cmds.setAttr(l_bricks[1]+'.tx',0)
	cmds.setAttr(l_bricks[1]+'.ty',50)
	cmds.setAttr(l_bricks[2]+'.tx',0)
	cmds.setAttr(l_bricks[2]+'.ty',100)
	cmds.setAttr(l_bricks[3]+'.tx',0)
	cmds.setAttr(l_bricks[3]+'.ty',150)
	cmds.setAttr(inTetris+'.direction',2)
def I_TetrisRote_2(inTetris):
	l_bricks=cmds.listRelatives(inTetris)
	cmds.setAttr(l_bricks[0]+'.tx',0)
	cmds.setAttr(l_bricks[0]+'.ty',0)
	cmds.setAttr(l_bricks[1]+'.tx',-50)
	cmds.setAttr(l_bricks[1]+'.ty',0)
	cmds.setAttr(l_bricks[2]+'.tx',50)
	cmds.setAttr(l_bricks[2]+'.ty',0)
	cmds.setAttr(l_bricks[3]+'.tx',100)
	cmds.setAttr(l_bricks[3]+'.ty',0)
	cmds.setAttr(inTetris+'.direction',3)
def I_TetrisRote_3(inTetris):
	l_bricks=cmds.listRelatives(inTetris)
	cmds.setAttr(l_bricks[0]+'.tx',0)
	cmds.setAttr(l_bricks[0]+'.ty',0)
	cmds.setAttr(l_bricks[1]+'.tx',0)
	cmds.setAttr(l_bricks[1]+'.ty',50)
	cmds.setAttr(l_bricks[2]+'.tx',0)
	cmds.setAttr(l_bricks[2]+'.ty',100)
	cmds.setAttr(l_bricks[3]+'.tx',0)
	cmds.setAttr(l_bricks[3]+'.ty',150)
	cmds.setAttr(inTetris+'.direction',0)
I_TetrisRotes={0:I_TetrisRote_0,1:I_TetrisRote_1,2:I_TetrisRote_2,3:I_TetrisRote_3}
def I_TetrisRote(inTetris):
	I_TetrisRotes[cmds.getAttr(inTetris+'.direction')](inTetris)
def T_TetrisRote_0(inTetris):
	l_bricks=cmds.listRelatives(inTetris)
	cmds.setAttr(l_bricks[0]+'.tx',-50)
	cmds.setAttr(l_bricks[0]+'.ty',50)
	cmds.setAttr(l_bricks[1]+'.tx',-50)
	cmds.setAttr(l_bricks[1]+'.ty',100)
	cmds.setAttr(l_bricks[2]+'.tx',-50)
	cmds.setAttr(l_bricks[2]+'.ty',0)
	cmds.setAttr(l_bricks[3]+'.tx',0)
	cmds.setAttr(l_bricks[3]+'.ty',50)
	cmds.setAttr(inTetris+'.direction',1)
def T_TetrisRote_1(inTetris):
	l_bricks=cmds.listRelatives(inTetris)
	cmds.setAttr(l_bricks[0]+'.tx',0)
	cmds.setAttr(l_bricks[0]+'.ty',0)
	cmds.setAttr(l_bricks[1]+'.tx',50)
	cmds.setAttr(l_bricks[1]+'.ty',50)
	cmds.setAttr(l_bricks[2]+'.tx',-50)
	cmds.setAttr(l_bricks[2]+'.ty',50)
	cmds.setAttr(l_bricks[3]+'.tx',0)
	cmds.setAttr(l_bricks[3]+'.ty',50)
	cmds.setAttr(inTetris+'.direction',2)
def T_TetrisRote_2(inTetris):
	l_bricks=cmds.listRelatives(inTetris)
	cmds.setAttr(l_bricks[0]+'.tx',50)
	cmds.setAttr(l_bricks[0]+'.ty',50)
	cmds.setAttr(l_bricks[1]+'.tx',50)
	cmds.setAttr(l_bricks[1]+'.ty',0)
	cmds.setAttr(l_bricks[2]+'.tx',50)
	cmds.setAttr(l_bricks[2]+'.ty',100)
	cmds.setAttr(l_bricks[3]+'.tx',0)
	cmds.setAttr(l_bricks[3]+'.ty',50)
	cmds.setAttr(inTetris+'.direction',3)
def T_TetrisRote_3(inTetris):
	l_bricks=cmds.listRelatives(inTetris)
	cmds.setAttr(l_bricks[0]+'.tx',0)
	cmds.setAttr(l_bricks[0]+'.ty',0)
	cmds.setAttr(l_bricks[1]+'.tx',50)
	cmds.setAttr(l_bricks[1]+'.ty',0)
	cmds.setAttr(l_bricks[2]+'.tx',-50)
	cmds.setAttr(l_bricks[2]+'.ty',0)
	cmds.setAttr(l_bricks[3]+'.tx',0)
	cmds.setAttr(l_bricks[3]+'.ty',50)
	cmds.setAttr(inTetris+'.direction',0)
T_TetrisRotes={0:T_TetrisRote_0,1:T_TetrisRote_1,2:T_TetrisRote_2,3:T_TetrisRote_3}
def T_TetrisRote(inTetris):
	T_TetrisRotes[cmds.getAttr(inTetris+'.direction')](inTetris)
def S_TetrisRote_0(inTetris):
	l_bricks=cmds.listRelatives(inTetris)
	cmds.setAttr(l_bricks[0]+'.tx',0)
	cmds.setAttr(l_bricks[0]+'.ty',0)
	cmds.setAttr(l_bricks[1]+'.tx',-50)
	cmds.setAttr(l_bricks[1]+'.ty',50)
	cmds.setAttr(l_bricks[2]+'.tx',0)
	cmds.setAttr(l_bricks[2]+'.ty',50)
	cmds.setAttr(l_bricks[3]+'.tx',-50)
	cmds.setAttr(l_bricks[3]+'.ty',100)
	cmds.setAttr(inTetris+'.direction',1)
def S_TetrisRote_1(inTetris):
	l_bricks=cmds.listRelatives(inTetris)
	cmds.setAttr(l_bricks[0]+'.tx',0)
	cmds.setAttr(l_bricks[0]+'.ty',0)
	cmds.setAttr(l_bricks[1]+'.tx',-50)
	cmds.setAttr(l_bricks[1]+'.ty',0)
	cmds.setAttr(l_bricks[2]+'.tx',0)
	cmds.setAttr(l_bricks[2]+'.ty',50)
	cmds.setAttr(l_bricks[3]+'.tx',50)
	cmds.setAttr(l_bricks[3]+'.ty',50)
	cmds.setAttr(inTetris+'.direction',2)
def S_TetrisRote_2(inTetris):
	l_bricks=cmds.listRelatives(inTetris)
	cmds.setAttr(l_bricks[0]+'.tx',0)
	cmds.setAttr(l_bricks[0]+'.ty',0)
	cmds.setAttr(l_bricks[1]+'.tx',-50)
	cmds.setAttr(l_bricks[1]+'.ty',50)
	cmds.setAttr(l_bricks[2]+'.tx',0)
	cmds.setAttr(l_bricks[2]+'.ty',50)
	cmds.setAttr(l_bricks[3]+'.tx',-50)
	cmds.setAttr(l_bricks[3]+'.ty',100)
	cmds.setAttr(inTetris+'.direction',3)
def S_TetrisRote_3(inTetris):
	l_bricks=cmds.listRelatives(inTetris)
	cmds.setAttr(l_bricks[0]+'.tx',0)
	cmds.setAttr(l_bricks[0]+'.ty',0)
	cmds.setAttr(l_bricks[1]+'.tx',-50)
	cmds.setAttr(l_bricks[1]+'.ty',0)
	cmds.setAttr(l_bricks[2]+'.tx',0)
	cmds.setAttr(l_bricks[2]+'.ty',50)
	cmds.setAttr(l_bricks[3]+'.tx',50)
	cmds.setAttr(l_bricks[3]+'.ty',50)
	cmds.setAttr(inTetris+'.direction',0)
S_TetrisRotes={0:S_TetrisRote_0,1:S_TetrisRote_1,2:S_TetrisRote_2,3:S_TetrisRote_3}
def S_TetrisRote(inTetris):
	S_TetrisRotes[cmds.getAttr(inTetris+'.direction')](inTetris)
TetrisRotes={'O':O_TetrisRote,'L':L_TetrisRote,'J':J_TetrisRote,'Z':Z_TetrisRote,'I':I_TetrisRote,'T':T_TetrisRote,'S':S_TetrisRote}
#返回四个方块最底层,最左侧和最右侧的方块(在生产的时候和旋转的时候获取,并存储在相应的数组里)
def BottomBricks(inTetris):
	fourbricks=cmds.listRelatives(inTetris)
	templist=[fourbricks[0]]
	for i in range(1,4):
		tempi=0
		for item in templist:
			if cmds.getAttr(item+'.tx')==cmds.getAttr(fourbricks[i]+'.tx'):
				if cmds.getAttr(item+'.ty')>cmds.getAttr(fourbricks[i]+'.ty'):
					templist.remove(item)
					templist.append(fourbricks[i])
				break
			tempi+=1
		if tempi==len(templist):
			templist.append(fourbricks[i])
	return templist
def LeftBricks(inTetris):
	fourbricks=cmds.listRelatives(inTetris)
	templist=[fourbricks[0]]
	for i in range(1,4):
		tempi=0
		for item in templist:
			if cmds.getAttr(item+'.ty')==cmds.getAttr(fourbricks[i]+'.ty'):
				if cmds.getAttr(item+'.tx')>cmds.getAttr(fourbricks[i]+'.tx'):
					templist.remove(item)
					templist.append(fourbricks[i])
				break
			tempi+=1
		if tempi==len(templist):
			templist.append(fourbricks[i])
	return templist
def RightBricks(inTetris):
	fourbricks=cmds.listRelatives(inTetris)
	templist=[fourbricks[0]]
	for i in range(1,4):
		tempi=0
		for item in templist:
			if cmds.getAttr(item+'.ty')==cmds.getAttr(fourbricks[i]+'.ty'):
				if cmds.getAttr(item+'.tx')<cmds.getAttr(fourbricks[i]+'.tx'):
					templist.remove(item)
					templist.append(fourbricks[i])
				break
			tempi+=1
		if tempi==len(templist):
			templist.append(fourbricks[i])
	return templist
#数字和Tetris类型的对应
TetrisTypes={0:'O_grp',1:'L_grp',2:'J_grp',3:'Z_grp',4:'T_grp',5:'S_grp',6:'I_grp'}
#给定一个方块元素,把它的世界坐标转换成索引坐标
def GetIndexPos(inbrick):
	wspos=cmds.xform(inbrick,q=1,t=1,ws=1)
	return [int(wspos[0]/50)+9,int(wspos[1]/50)]
#第incol列的index行往上的所有元素向下移动一格(不包括第index行)
def BricksDownOne(incol,index):
	for i in range(index,35):
		if FrameAllIndex[incol][i+1]:
			cmds.move(0,-50,0,FrameAllIndex[incol][i+1],r=1)
		FrameAllIndex[incol][i]=FrameAllIndex[incol][i+1]
	FrameAllIndex[incol][35]=0
#填充FrameAllIndex并检查是否有满行,如果有返回满行的行索引
def FillFrame():
	global FrameAllIndex
	global gameRun
	fillrows=[]
	for item in cmds.listRelatives(theAcTetris):
		indexCoord=GetIndexPos(item)
		#print(item+': '+str(indexCoord[0])+' '+str(indexCoord[1])+' ')
		#如果满列就返回游戏结束
		if indexCoord[1]>35:
			gameRun=False
			utils.executeInMainThreadWithResult("cmds.inViewMessage(amg='游戏结束!!',pos='midCenter',backColor=0x7B5353,fade=True,fadeInTime=3,fadeOutTime=1)")
			cmds.window('zjhGameOverWindow',e=1,visible=1)
			#间隔一小段时间再向界面添加排名元素
			utils.executeInMainThreadWithResult(addJiFenBangUICommand_lines)#在主线程执行添加积分榜UI
			return
		FrameAllIndex[indexCoord[0]][indexCoord[1]]=item	#y轴坐标是行,x轴坐标是列
		for i in range(19):
			if FrameAllIndex[i][indexCoord[1]]==0:
				break
		if i==18 and (indexCoord[1] not in fillrows):
			fillrows.append(indexCoord[1])
		cmds.parent(item,'staticBricks_grp')
	cmds.delete(theAcTetris)
	fillrows=sorted(fillrows,reverse=1)
	print('fillrows len: '+str(len(fillrows)))
	for fi in fillrows:
		print('fill rows: '+str(fi))
		for j in range(19):
			cmds.delete(FrameAllIndex[j][fi])#删除满行的方块,并加分(加分的多少是和fillrows的长度有关的,也就是连续消灭多行会有分数加成)
		for j in range(19):
			BricksDownOne(j,fi)#删除之后其上面的所有方快下降一格
		ZjhGlobals.currentscore+=19*len(fillrows)
		ShowIntDigits('defen_',ZjhGlobals.currentscore)

#给一个Tetris,判定它的位置是否合法(如果它的四个元素有任何一个的索引位置不是0的,就不合法)(这个函数同样可以用来判断旋转是否合法)
def IsValidPos(inTetris):
	for item in cmds.listRelatives(inTetris):
		indexCoord=GetIndexPos(item)
		if FrameAllIndex[indexCoord[0]][indexCoord[1]]:
			return False
	return True
def GenerateTetri():
	global theAcTetris
	global theAcButtomBricks
	global theAcLeftBricks
	global theAcRightBricks
	randint=random.randint(0,6)
	theAcTetris=cmds.instance(TetrisTypes[randint],lf=1)[0]
	theAcTetris_list=cmds.listRelatives(theAcTetris)
	tempOrgTetris_list=cmds.listRelatives(TetrisTypes[randint])
	for i in range(4):
		cmds.setAttr(theAcTetris_list[i]+'.tx',cmds.getAttr(tempOrgTetris_list[i]+'.tx'))
		cmds.setAttr(theAcTetris_list[i]+'.ty',cmds.getAttr(tempOrgTetris_list[i]+'.ty'))
		#设置显示层
		cmds.editDisplayLayerMembers(colorlayers[randint],theAcTetris_list[i],noRecurse=1)
	cmds.setAttr(theAcTetris+'.ty',1750)
	cmds.setAttr(theAcTetris+'.visibility',1)
	theAcButtomBricks=BottomBricks(theAcTetris)#生成的Tetris并计算其bottomBricks
	theAcLeftBricks=LeftBricks(theAcTetris)#生成的Tetris并计算其theAcLeftBricks
	theAcRightBricks=RightBricks(theAcTetris)#生成的Tetris并计算其theAcRightBricks
	cmds.select(theAcTetris)
def IsGetLowest():	#判断Tetris是否已经到底
	global theAcButtomBricks
	if cmds.getAttr(theAcTetris+'.ty')<=0:
		return True
	else:
		for item in theAcButtomBricks:
			indexCoord=GetIndexPos(item)
			if FrameAllIndex[indexCoord[0]][indexCoord[1]-1]:
				return True
	return False
def IsGetLeftest():	#判断Tetris是否已经到最左边	
	global theAcLeftBricks
	for item in theAcLeftBricks:
		indexCoord=GetIndexPos(item)
		if indexCoord[0]-1<0 or indexCoord[1]>35 or FrameAllIndex[indexCoord[0]-1][indexCoord[1]]:
			return True
		continue
	return False
def IsGetRightest():	#判断Tetris是否已经到最右边	
	global theAcRightBricks
	for item in theAcRightBricks:
		indexCoord=GetIndexPos(item)
		if indexCoord[0]+1>18 or indexCoord[1]>35 or FrameAllIndex[indexCoord[0]+1][indexCoord[1]]:
			return True
		continue
	return False
def TetrisDown():
	#如果到达底线
	if IsGetLowest():
		FillFrame()#把theAcTetris的四个方块填充进FrameAllIndex
		GenerateTetri()#生成新的Tetris
	else:	#如果没有到达底线
		cmds.move(0,-50,0,theAcTetris,r=1)

#键盘按键接口函数
def LeftPressF():
	if not IsGetLeftest():
		cmds.move(-50,0,0,theAcTetris,r=1)
def LeftReleaseF():
	pass
def RightPressF():
	if not IsGetRightest():
		cmds.move(50,0,0,theAcTetris,r=1)
def RightReleaseF():
	pass
def DownPressF():
	global interval
	interval*=0.2
def DownReleaseF():
	global interval
	interval*=5
def UpPressF():
	TetrisRotes[theAcTetris.split('_grp')[0]](theAcTetris)
	theAcButtomBricks=BottomBricks(theAcTetris)#生成的Tetris并计算其bottomBricks
	theAcLeftBricks=LeftBricks(theAcTetris)#生成的Tetris并计算其theAcLeftBricks
	theAcRightBricks=RightBricks(theAcTetris)#生成的Tetris并计算其theAcRightBricks
def UpReleaseF():
	pass
def TetrisDownLowest():
	#遍历最底层的方块所在列为1的最大行号
	theMinDownStep=36
	for item in theAcButtomBricks:
		coordIndex=GetIndexPos(item)
		#lowermost=True
		for rowdex in range(coordIndex[1]-1,-1,-1):
			if FrameAllIndex[coordIndex[0]][rowdex]:
				#print(rowdex)
				#lowermost=False
				rowdex+=1
				break
		downstep=coordIndex[1]-rowdex
		if downstep<theMinDownStep:
			theMinDownStep=downstep
	cmds.move(0,-theMinDownStep*50,0,theAcTetris,r=1)
	FillFrame()#把theAcTetris的四个方块填充进FrameAllIndex
	GenerateTetri()#生成新的Tetris
def SpacePressF():
	cmds.setAttr('staticBricks_grp.spaceDown',1)
def SpaceReleaseF():
	cmds.setAttr('staticBricks_grp.spaceDown',0)
#时刻监测事件队列和更新场景
def Tick():
	ZjhGlobals.gametime=0
	pretime=time.time()
	downpretime=time.time()
	global gameRun
	global interval
	interval=1.0
	global theAcTetris
	while gameRun:
		if cmds.getAttr('staticBricks_grp.spaceDown'):
			TetrisDownLowest()
			cmds.setAttr('staticBricks_grp.spaceDown',0)
		if time.time()-downpretime >= interval:
			downpretime=time.time()
			TetrisDown()
		if time.time()-pretime >= 1:
			interval-=0.0005#随着游戏时间的增长,俄罗斯方块向下跳动的时间间隔会越来越短
			ZjhGlobals.gametime+=1
			ShowIntDigits('haoshi_',ZjhGlobals.gametime)
			ZjhGlobals.currentscoreRate=round(ZjhGlobals.currentscore/ZjhGlobals.gametime,2)
			ShowFloatDigits('defenlv_',ZjhGlobals.currentscoreRate)
			pretime=time.time()

def InitTetrisGameScene():
	cmds.file(projectPath+'scenes/Scene_Tetris.ma', open=1,force=1)
	#初始化Tetris游戏场景
	gameRun=True
	interval=1.0
	theAcButtomBricks=[]
	theAcLeftBricks=[]
	theAcRightBricks=[]
	FrameAllIndex=[]
	for i in range(19):
		FrameAllIndex.append([0]*36)
	GenerateTetri()
	#启动tick线程
	TickThread=thrd.Thread(target=Tick)#专门为Tick函数开辟一个线程
	TickThread.start()
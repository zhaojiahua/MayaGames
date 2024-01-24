from maya import utils
import random
import json
import time
import math
import threading as thrd
from Globals import projectPath
from Globals import ZjhGlobals
from CommonFuns import *

###全局变量
global gameRun
gameRun=True
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

#键盘按键接口函数
def LeftPressF():
	pass
def LeftReleaseF():
	pass
def RightPressF():
	pass
def RightReleaseF():
	pass
def DownPressF():
	pass
def DownReleaseF():
	pass
def UpPressF():
	cmds.setAttr('theCar.refuel',1)
def UpReleaseF():
	cmds.setAttr('theCar.refuel',0)
def SpacePressF():
	pass
def SpaceReleaseF():
	pass
#时刻监测事件队列和更新场景
def Tick():
	ZjhGlobals.gametime=0
	pretime=time.time()
	tickpretime=time.time()
	startTime=time.time()
	cmds.setAttr('theCar.refuel',0)
	while gameRun:
		if time.time()-tickpretime>=0.02:
			tickpretime=time.time()
			Force=0	#牵引力
			if cmds.getAttr('theCar.refuel'):
				#油门踩下的那一刻,汽车牵引力随时间变化(0-1) 接下来是受力分析
				Force=(1.0/(1.0+math.exp(0.1*(startTime-time.time())))-0.5)
			else:
				Force=0
			Friction=0	#动摩擦力
			if cmds.getAttr('theCar.carSpeed')>0:
				Friction=0.2
			else:
				if Force<0.2:
					Friction=Force
				if cmds.getAttr('theCar.carSpeed')<0:
					cmds.setAttr('theCar.carSpeed',0)
			acc=(Force-Friction)/cmds.getAttr('theCar.carMass')#更新加速度
			speed=cmds.getAttr('theCar.carSpeed')+acc#更新速度
			cmds.setAttr('theCar.carSpeed',speed)
			cmds.move(0,0,-speed,'theCar',r=1)#更新位置
		if time.time()-pretime >= 1:
			ZjhGlobals.gametime+=1
			ShowIntDigits('haoshi_',ZjhGlobals.gametime)
			ZjhGlobals.currentscoreRate=round(ZjhGlobals.currentscore/ZjhGlobals.gametime,2)
			ShowFloatDigits('defenlv_',ZjhGlobals.currentscoreRate)
			pretime=time.time()

def InitRaceCarGameScene():
	cmds.file(projectPath+'scenes/Scene_RaceCar.ma', open=1,force=1)
	#初始化Tetris游戏场景
	gameRun=True
	#启动tick线程
	TickThread=thrd.Thread(target=Tick)#专门为Tick函数开辟一个线程
	TickThread.start()
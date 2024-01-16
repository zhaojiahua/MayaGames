from maya import utils
import random
import json
import time
import threading as thrd
from Globals import projectPath
from Globals import ZjhGlobals
from CommonFuns import *

###全局变量
global Spacedoonce
Spacedoonce=False
global interval
interval=1.0
global FrameAllIndex	#用来记录所有方块的填充状况
FrameAllIndex=[[0]*36]*19	#一共19列,每列有36个元素
###全局变量

restartBtnCommand_lines=Getcmdlines(projectPath+'scripts/tetris_scripts/CommandsLines/restartBtnCommand_lines.py')
gobackBtnCommand_lines=Getcmdlines(projectPath+'scripts/tetris_scripts/CommandsLines/gobackBtnCommand_lines.py')
nextLevelBtnCommand_lines=Getcmdlines(projectPath+'scripts/tetris_scripts/CommandsLines/nextLevelBtnCommand_lines.py')
addJiFenBangUICommand_lines=Getcmdlines(projectPath+'scripts/tetris_scripts/CommandsLines/addJiFenBangUI_lines.py')

#颜色和层名字的枚举对应
colorlayers={0:'defaultcolorLayer',1:'redLayer',2:'greenLayer',3:'blueLayer',4:'blackLayer'}
#颜色和shadingEngine的对应
colorSets={0:'initialShadingGroup',1:'bcolor_mat1SG',2:'bcolor_mat2SG',3:'bcolor_mat3SG',4:'bcolor_mat4SG'}
#颜色和得分的对应(默认色1分,红色2分,绿色3分,蓝色4分,黑色0分)
colorScores={0:1,1:2,2:3,3:4,4:0}
#颜色和小球加速值的对应(小球碰撞到不同颜色的方块会获得不同的加速,白色减速6%,红色加速10%,绿色加速8%,蓝色加速6%,黑色减速18%)
coloraccelerates={0:0.94,1:1.1,2:1.08,3:1.06,4:0.82}
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

global theAcTetris
theAcTetris=''
#键盘按键接口函数
def LeftPressF():
	cmds.move(-50,0,0,theAcTetris,r=1)
def LeftReleaseF():
	pass
def RightPressF():
	cmds.move(50,0,0,theAcTetris,r=1)
def RightReleaseF():
	pass
def DownPressF():
	global interval
	interval*=0.2
def DownReleaseF():
	global interval
	interval*=5
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
def UpPressF():
	global theAcTetris
	TetrisRotes[theAcTetris.split('_grp')[0]](theAcTetris)
def UpReleaseF():
	pass
def SpacePressF():
	ChangeSlideSpeed(2)
def SpaceReleaseF():
	ChangeSlideSpeed(0.5)
	ChangeSphereV('pSphere1',[1,3,0])
#数字和Tetris类型的对应
TetrisTypes={0:'O_grp',1:'L_grp',2:'J_grp',3:'Z_grp',4:'I_grp',5:'T_grp',6:'S_grp'}

#给定一个方块元素,把它的世界坐标转换成索引坐标
def GetIndexPos(inbrick):
	wspos=cmds.xform(inbrick,q=1,t=1,ws=1)
	return [int(wspos[0]/50)+9,int(wspos[1]/50)]
#填充FrameAllIndex并更新TheHightests列表
def FillFrame(inTetris):
	global FrameAllIndex
	global TheHighests
	for item in cmds.listRelatives(inTetris):
		indexCoord=GetIndexPos(item)
		FrameAllIndex[indexCoord[0]][indexCoord[1]]=1	#y轴坐标是行,x轴坐标是列
		if TheHighests[indexCoord[0]]<indexCoord[1]:	#更新TheHightests列表
			TheHighests[indexCoord[0]]=indexCoord[1]
#给一个Tetris,判定它的位置是否合法(如果它的四个元素有任何一个的索引位置不是0的,就不合法)(这个函数同样可以用来判断旋转是否合法)
def IsValidMove(inTetris):
	for item in cmds.listRelatives(inTetris):
		indexCoord=GetIndexPos(item)
		if FrameAllIndex[indexCoord[0]][indexCoord[1]]==1:
			return False
	return True
def GenerateTetri():
	global theAcTetris
	randTetris_grp=TetrisTypes[random.randint(0,6)]
	theAcTetris=cmds.instance(randTetris_grp,lf=1)[0]
	theAcTetris_list=cmds.listRelatives(theAcTetris)
	tempOrgTetris_list=cmds.listRelatives(randTetris_grp)
	for i in range(4):
		cmds.setAttr(theAcTetris_list[i]+'.tx',cmds.getAttr(tempOrgTetris_list[i]+'.tx'))
		cmds.setAttr(theAcTetris_list[i]+'.ty',cmds.getAttr(tempOrgTetris_list[i]+'.ty'))
	cmds.setAttr(theAcTetris+'.ty',1600)
	cmds.setAttr(theAcTetris+'.visibility',1)
	cmds.select(theAcTetris)
def IsGetLowest(inTetris):	#判断Tetris是否已经到底
	#每一个Tetris都有ty为0的方块元素,这些ty为0的方块元素就是这个Tetris最底层的元素,不是最底层的元素不用判断
	if cmds.getAttr(inTetris+'.ty')<=0:
		return True
	else:
		for item in cmds.listRelatives(inTetris):
			if cmds.getAttr(item+'.ty')==0:
				indexcood=GetIndexPos(item)
				if indexcood[1]-1<=TheHighests[indexcood[0]]:
					return True
	return False
def TetrisDown(ingrp):
	#如果到达底线
	if IsGetLowest(ingrp):
		FillFrame(theAcTetris)#把theAcTetris的四个方块填充进FrameAllIndex,并更新TheHighests列表
		GenerateTetri()#生成新的Tetris
	else:	#如果没有到达底线
		cmds.move(0,-50,0,ingrp,r=1)

#时刻监测事件队列和更新场景
def Tick():
	ZjhGlobals.gametime=0
	pretime=time.time()
	downpretime=time.time()
	gameRun=True
	global interval
	interval=1.0
	global theAcTetris
	while gameRun:
		if time.time()-downpretime >= interval:
			downpretime=time.time()
			TetrisDown(theAcTetris)
		if time.time()-pretime >= 1:
			interval-=0.0005#随着游戏时间的增长,俄罗斯方块向下跳动的时间间隔会越来越短
			ZjhGlobals.gametime+=1
			ShowIntDigits('haoshi_',ZjhGlobals.gametime)
			ZjhGlobals.currentscoreRate=round(ZjhGlobals.currentscore/ZjhGlobals.gametime,2)
			ShowFloatDigits('defenlv_',ZjhGlobals.currentscoreRate)
			pretime=time.time()

def InitTetrisGameScene():
	#初始化Tetris游戏场景
	cmds.file(projectPath+'scenes/Scene_Tetris.ma', open=1,force=1)
	GenerateTetri()
	#启动tick线程
	TickThread=thrd.Thread(target=Tick)#专门为Tick函数开辟一个线程
	TickThread.start()

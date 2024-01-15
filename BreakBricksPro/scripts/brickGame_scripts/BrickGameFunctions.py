from maya import cmds
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
global gametime
###全局变量


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

restartBtnCommand_lines=Getcmdlines(projectPath+'scripts/brickGame_scripts/CommandsLines/restartBtnCommand_lines.py')
gobackBtnCommand_lines=Getcmdlines(projectPath+'scripts/brickGame_scripts/CommandsLines/gobackBtnCommand_lines.py')
nextLevelBtnCommand_lines=Getcmdlines(projectPath+'scripts/brickGame_scripts/CommandsLines/nextLevelBtnCommand_lines.py')
addJiFenBangUICommand_lines=Getcmdlines(projectPath+'scripts/brickGame_scripts/CommandsLines/addJiFenBangUI_lines.py')

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


#向键盘事件队列添加键盘事件(给定按键名称和相应的数值)
def AddEvent2evQueue(keyname,keyvalue):
	cmds.addAttr('opQueue',ln='event'+keyname,at='short',k=1,dv=keyvalue)
#从键盘事件队列的末尾移除事件
def RemoveEvent4evQueue(keyname):
	cmds.deleteAttr('opQueue',attribute='event'+keyname)
#
def ChangeSlideSpeed(inc):
	cmds.setAttr('pCube1.speed',inc*cmds.getAttr('pCube1.speed'))

#改变inSphere的速度为invalue(空格键释放触发此函数,只能在开始的时候触发一次)
def ChangeSphereV(inSphere,invalue):
	global Spacedoonce
	if not Spacedoonce:
		temprand=2*random.random()-1#随机数在正负1之间
		cmds.setAttr(inSphere+'.zjhVX',temprand*invalue[0])
		cmds.setAttr(inSphere+'.zjhVY',invalue[1])
		cmds.setAttr(inSphere+'.zjhVZ',invalue[2])
		Spacedoonce=True

#键盘按键接口函数
def LeftPressF():
	AddEvent2evQueue('zjhleft',-1)
def LeftReleaseF():
	RemoveEvent4evQueue('zjhleft')
def RightPressF():
	AddEvent2evQueue('zjhright',1)
def RightReleaseF():
	RemoveEvent4evQueue('zjhright')
def SpacePressF():
	ChangeSlideSpeed(2)
def SpaceReleaseF():
	ChangeSlideSpeed(0.5)
	ChangeSphereV('pSphere1',[1,3,0])

#时刻监测事件队列和更新场景
def Tick():
	global score
	score=0
	global scoreRate
	scoreRate=0.0
	global gametime
	gametime=0
	pretime=time.time()
	gameRun=True
	while gameRun:
		cubeDir=0
		if cmds.listAttr('opQueue',k=1)[-1]=='eventzjhright' and cmds.getAttr('pCube1.tx')<450:
			cmds.move(0.05*cmds.getAttr('pCube1.speed'),0,0,'pCube1',r=1)
			cubeDir=1
		if cmds.listAttr('opQueue',k=1)[-1]=='eventzjhleft' and cmds.getAttr('pCube1.tx')>-450:
			cmds.move(-0.05*cmds.getAttr('pCube1.speed'),0,0,'pCube1',r=1)
			cubeDir=-1
		#时刻监测小球的速度值,并根据其速度时刻更新位置
		cmds.move(cmds.getAttr('pSphere1.zjhVX'),cmds.getAttr('pSphere1.zjhVY'),cmds.getAttr('pSphere1.zjhVZ'),'pSphere1',r=1)
		#随后就监测碰撞
		#与墙壁碰撞
		if cmds.getAttr('pSphere1.tx')>550-cmds.getAttr('pSphere1.sx') or cmds.getAttr('pSphere1.tx')<-550+cmds.getAttr('pSphere1.sx'):
			cmds.setAttr('pSphere1.zjhVX',-cmds.getAttr('pSphere1.zjhVX'))#触碰到两遍墙壁改变其X轴向上的速度
		if cmds.getAttr('pSphere1.ty')>1950-cmds.getAttr('pSphere1.sy'):
			cmds.setAttr('pSphere1.zjhVY',-cmds.getAttr('pSphere1.zjhVY'))#触碰到两遍墙壁改变其Y轴向上的速度
		#监测与pCube1的碰撞情况
		tempCollision=DetectCollision('pSphere1','pCube1')
		if tempCollision==0:
			pass
		elif tempCollision==1 or tempCollision==3:
			cmds.setAttr('pSphere1.zjhVX',-cmds.getAttr('pSphere1.zjhVX'))#改变其X轴向上的速度
		elif tempCollision==2:#不可能为4的
			cmds.setAttr('pSphere1.zjhVY',-cmds.getAttr('pSphere1.zjhVY'))#改变其Y轴向上的速度
			#根据滑块的运动方向随机改变X轴向上的速度
			cmds.setAttr('pSphere1.zjhVX',0.01*cubeDir*(random.random()+1)*cmds.getAttr('pCube1.speed')+cmds.getAttr('pSphere1.zjhVX'))
		thebricks=cmds.listRelatives('bricksGrp',c=1)
		if thebricks is None:
			gameRun=False
			cmds.window('zjhGameWinWindow',e=1,visible=1)
		else:
			#遍历所有的brick,监测它们与小球的碰撞情况
			for brick in thebricks:
				tbcolor=cmds.getAttr(brick+'.bcolor')
				tempCollision=DetectCollision('pSphere1',brick)
				if tempCollision==0:
					continue
				elif tempCollision==1 or tempCollision==3:
					addscore=colorScores[tbcolor]+SpeedExtraScore([cmds.getAttr('pSphere1.zjhVX'),cmds.getAttr('pSphere1.zjhVY')])
					score+=addscore
					cmds.setAttr('pSphere1.zjhVX',-coloraccelerates[tbcolor]*cmds.getAttr('pSphere1.zjhVX'))#改变其X轴向上的速度
					utils.executeInMainThreadWithResult("cmds.inViewMessage(amg='+{}分',pos='midLeft',fade=True,fadeInTime=0.1,fadeOutTime=0.1)".format(addscore))
					ShowIntDigits('defen_',score)
					cmds.delete(brick)#每删除一个方块得分,并刷新分数
					break
				elif tempCollision==2 or tempCollision==4:
					addscore=colorScores[tbcolor]+SpeedExtraScore([cmds.getAttr('pSphere1.zjhVX'),cmds.getAttr('pSphere1.zjhVY')])
					score+=addscore
					cmds.setAttr('pSphere1.zjhVY',-coloraccelerates[tbcolor]*cmds.getAttr('pSphere1.zjhVY'))#改变其Y轴向上的速度
					utils.executeInMainThreadWithResult("cmds.inViewMessage(amg='+{}分',pos='midLeft',fade=True,fadeInTime=0.1,fadeOutTime=0.1)".format(addscore))
					ShowIntDigits('defen_',score)
					cmds.delete(brick)#每删除一个方块得分
					break
		if cmds.getAttr('pSphere1.ty')<-50:
			gameRun=False
			utils.executeInMainThreadWithResult("cmds.inViewMessage(amg='游戏结束!!',pos='midCenter',backColor=0x7B5353,fade=True,fadeInTime=3,fadeOutTime=1)")
			SettleAccounts()
			cmds.window('zjhGameOverWindow',e=1,visible=1)
			#间隔一小段时间再向界面添加排名元素
			utils.executeInMainThreadWithResult(addJiFenBangUICommand_lines)#在主线程执行添加积分榜UI
		if time.time()-pretime >= 1:
			gametime+=1
			ShowIntDigits('haoshi_',gametime)
			scoreRate=round(score/gametime,2)
			ShowFloatDigits('defenlv_',scoreRate)
			pretime=time.time()

#实例化一个新的inCubeBase对象,并将其放置在inPos位置
def InstanceBricks(inCubeBase,inPos):
	tempname=cmds.instance(inCubeBase,lf=1)[0]
	cmds.setAttr(tempname+'.tx',inPos[0])
	cmds.setAttr(tempname+'.ty',inPos[1])
	cmds.setAttr(tempname+'.tz',inPos[2])
	return tempname

def InitBrickGameScene():
	global Spacedoonce
	#加载初始化场景
	cmds.file(projectPath+'scenes/Scene_BrickGame.ma', open=1,force=1)
	#场景加载完毕后#生成9行砖块,每行11块
	for i in range(9):
		for j in range(11):
			tempbrick=InstanceBricks('brick0',[-500+j*100,1925-i*50,0])
			#设置碰撞属性数据
			cmds.setAttr(tempbrick+'.corn011',cmds.getAttr('brick0.corn011'))
			cmds.setAttr(tempbrick+'.corn012',cmds.getAttr('brick0.corn012'))
			cmds.setAttr(tempbrick+'.corn021',cmds.getAttr('brick0.corn021'))
			cmds.setAttr(tempbrick+'.corn022',cmds.getAttr('brick0.corn022'))
			cmds.setAttr(tempbrick+'.corn031',cmds.getAttr('brick0.corn031'))
			cmds.setAttr(tempbrick+'.corn032',cmds.getAttr('brick0.corn032'))
			cmds.setAttr(tempbrick+'.corn041',cmds.getAttr('brick0.corn041'))
			cmds.setAttr(tempbrick+'.corn042',cmds.getAttr('brick0.corn042'))
			cmds.setAttr(tempbrick+'.corn01b',cmds.getAttr('brick0.corn01b'))
			cmds.setAttr(tempbrick+'.corn02b',cmds.getAttr('brick0.corn02b'))
			cmds.setAttr(tempbrick+'.corn03b',cmds.getAttr('brick0.corn03b'))
			cmds.setAttr(tempbrick+'.corn04b',cmds.getAttr('brick0.corn04b'))
			#随机分配一个颜色
			templayer=random.randint(0,4)
			cmds.setAttr(tempbrick+'.bcolor',templayer)
			#设置显示层
			cmds.editDisplayLayerMembers(colorlayers[templayer],tempbrick,noRecurse=1)
			#设置渲染层
			cmds.sets(tempbrick,e=1,forceElement=colorSets[templayer])
			cmds.parent(tempbrick,'bricksGrp')
	Spacedoonce=False
	#选中小球
	cmds.select('pSphere1')
	#启动tick线程
	TickThread=thrd.Thread(target=Tick)#专门为Tick函数开辟一个线程
	TickThread.start()
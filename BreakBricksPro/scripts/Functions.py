from maya import cmds
import math
import threading as thrd
from Globals import projectPath
def Getcmdlines(path):
    with open(path,'r',encoding="UTF-8") as f:
        cmdlines=f.read()
    return cmdlines

registerBtnCommand_lines=Getcmdlines(projectPath+'scripts/CommandsLines/registerBtnCommand_lines.py')
okBtnCommand_lines=Getcmdlines(projectPath+'scripts/CommandsLines/okBtnCommand_lines.py')
okRegisterBtnCommand_lines=Getcmdlines(projectPath+'scripts/CommandsLines/okRegisterBtnCommand_lines.py')
cencelRegisterBtnCommand_lines=Getcmdlines(projectPath+'scripts/CommandsLines/cencelRegisterBtnCommand_lines.py')
#Start界面
def CreateStartWindow():
    if cmds.window('zjhStartWindow',q=1,ex=1):
    	cmds.deleteUI('zjhStartWindow')
    cmds.window('zjhStartWindow',title='游戏启动界面',wh=[550,400],bgc=[0.4,0.3,0.3])
    cmds.columnLayout('zjhColumnLayout1',adjustableColumn=1)
    cmds.text('seperateLabel1',l=' ',height=50,bgc=[0.4,0.3,0.3])#---------分隔符
    cmds.rowLayout('zjhrowLayout1',numberOfColumns=2,ad2=2)
    cmds.text('countLabel',l='  帐号: ',font='boldLabelFont',height=50)
    cmds.loadUI( uiFile=projectPath+'scripts/passwordui.ui')#从Qt.ui文件提取一个文本框对象
    cmds.textField('qtAccountTextline',e=1,parent='zjhrowLayout1',font='boldLabelFont',height=50)
    #cmds.textField('countTextField',font='boldLabelFont',insertText='请输入帐号',height=50)
    cmds.setParent('..')
    cmds.text('seperateLabel2',l=' ',height=5,bgc=[0.4,0.3,0.3])#---------分隔符
    cmds.rowLayout('zjhrowLayout2',numberOfColumns=2,ad2=2)
    cmds.text('passwordLabel',l='  密码: ',font='boldLabelFont',height=50)
    #cmds.textField('passwordTextField',font='boldLabelFont',insertText='请输入密码',height=50,tcc=textChangedCommand_lines)
    #在这里我们自己实现输入框变星号的话是比较麻烦的,所以这里们借助Qt直接创建出一个密码框,然后把这个密码框放在这里就行了
    cmds.textField('qtPasswordTextline',e=1,parent='zjhrowLayout2',font='boldLabelFont',height=50)
    cmds.deleteUI('Form')
    cmds.setParent('..')
    cmds.text('seperateLabel3',l=' ',height=5,bgc=[0.4,0.3,0.3])#---------分隔符
    cmds.rowLayout('zjhrowLayout3',numberOfColumns=2,ad2=2,columnAttach=[(1,'left',50),(2,'right',50)])
    cmds.button('okBtn',l='  登录游戏  ',width=200,height=50,bgc=[0.4,0.35,0.35],c=okBtnCommand_lines)
    cmds.button('registerBtn',l='  注册帐号  ',width=200,height=50,bgc=[0.4,0.35,0.35],c=registerBtnCommand_lines)
    cmds.setParent('..')
    cmds.showWindow('zjhStartWindow')
def CreateRegisterWindow():
    if cmds.window('zjhStartWindow',q=1,ex=1):
        cmds.deleteUI('zjhStartWindow')
    cmds.loadUI(uiFile=projectPath+'scripts/registerui.ui')
    cmds.window('zjhRegisterWindow',e=1,wh=[550,300],bgc=[0.28,0.31,0.3])
    cmds.button('okRegisterBtn',e=1,c=okRegisterBtnCommand_lines)
    cmds.button('cencelRegisterBtn',e=1,c=cencelRegisterBtnCommand_lines)
    cmds.showWindow('zjhRegisterWindow')

#计算两个向量的距离的平方
def GetDistance(v1,v2):
	return math.sqrt((v1[0]-v2[0])*(v1[0]-v2[0])+(v1[1]-v2[1])*(v1[1]-v2[1])+(v1[2]-v2[2])*(v1[2]-v2[2]))
#返回向量的normalized
def GetVectorNormal(ve):
	norm=math.sqrt(ve[0]*ve[0]+ve[1]*ve[1]+ve[2]*ve[2])
	return [ve[0]/norm,ve[1]/norm,ve[2]/norm]
#获取向量的角度(相对于x轴的角度,取值范围在0-2*pi之间)
def GetAngle(v1):
	mv1=GetVectorNormal(v1)
	if mv1[1]>=0:
		return math.acos(mv1[0])
	else:
		return 6.2831852-math.acos(mv1[0])
#新的碰撞检测算法
def DetectCollision(inSphere,inCube):
	sptx=cmds.getAttr(inSphere+'.tx')
	spty=cmds.getAttr(inSphere+'.ty')
	cutx=cmds.getAttr(inCube+'.tx')
	cuty=cmds.getAttr(inCube+'.ty')
	sphereR=0.5*cmds.getAttr(inSphere+'.sx')
	helfCubeW=0.5*cmds.getAttr(inCube+'.sx')
	helfCubeH=0.5*cmds.getAttr(inCube+'.sy')
	if abs(sptx-cutx)>(sphereR+helfCubeW) or abs(spty-cuty)>(sphereR+helfCubeH):
		return '距离太远'
	else:
		corn4Ps=[[cutx+helfCubeW,cuty+helfCubeH,0],[cutx-helfCubeW,cuty+helfCubeH,0],[cutx-helfCubeW,cuty-helfCubeH,0],[cutx-helfCubeW,cuty+helfCubeH,0]]#四个角上的点
		disDir=[sptx-cutx,spty-cuty,0]#小球在方块的方位
		orient=GetAngle(disDir)
		if orient<cmds.getAttr('brick0.corn011'):
			return '小于拐角1,返回1'
		elif orient<cmds.getAttr('brick0.corn012'):
			if GetDistance([sptx,spty,0],corn4Ps[0])>sphereR:
				return '大于拐角1半径，返回0'
			else:
				if orient<cmds.getAttr('brick0.corn01b'):
					return '交于角1,返回1'
				else:
					return '交于角1,返回2'
		elif orient<cmds.getAttr('brick0.corn021'):
			return '小于拐角2,返回2'
		elif orient<cmds.getAttr('brick0.corn022'):
			if GetDistance([sptx,spty,0],corn4Ps[1])>sphereR:
				return '大于拐角2半径，返回0'
			else:
				if orient<cmds.getAttr('brick0.corn02b'):
					return '交于角2,返回2'
				else:
					return '交于角2,返回3'
		elif orient<cmds.getAttr('brick0.corn031'):
			return '小于拐角3,返回3'
		elif orient<cmds.getAttr('brick0.corn032'):
			if GetDistance([sptx,spty,0],corn4Ps[2])>sphereR:
				return '大于拐角3半径，返回0'
			else:
				if orient<cmds.getAttr('brick0.corn03b'):
					return '交于角3,返回3'
				else:
					return '交于角3,返回4'
		elif orient<cmds.getAttr('brick0.corn041'):
			return '小于拐角4,返回4'
		elif orient<cmds.getAttr('brick0.corn042'):
			if GetDistance([sptx,spty,0],corn4Ps[3])>sphereR:
				return '大于拐角4半径，返回0'
			else:
				if orient<cmds.getAttr('brick0.corn04b'):
					return '交于角4,返回4'
				else:
					return '交于角4,返回1'
		else:
			return '最后返回1'

#向键盘事件队列添加键盘事件(给定按键名称和相应的数值)
def AddEvent2evQueue(keyname,keyvalue):
	cmds.addAttr('opQueue',ln='event'+keyname,at='short',k=1,dv=keyvalue)
#从键盘事件队列的末尾移除事件
def RemoveEvent4evQueue(keyname):
	cmds.deleteAttr('opQueue',attribute='event'+keyname)
#从键盘事件队列读取键盘事件
def EventsConsumer():
	while True:
		if cmds.listAttr('opQueue',k=1)[-1]=='eventzjhright' and cmds.getAttr('pCube1.tx')<400:
			cmds.move(0.02*cmds.getAttr('pCube1.speed'),0,0,'pCube1',r=1)
		if cmds.listAttr('opQueue',k=1)[-1]=='eventzjhleft' and cmds.getAttr('pCube1.tx')>-400:
			cmds.move(-0.02*cmds.getAttr('pCube1.speed'),0,0,'pCube1',r=1)

#时刻监测小球的速度值,并根据其速度时刻更新位置
def UpdateSphere():
	while True:
		cmds.move(cmds.getAttr('pSphere1.zjhVX'),cmds.getAttr('pSphere1.zjhVY'),cmds.getAttr('pSphere1.zjhVZ'),'pSphere1',r=1)
#改变小球的速度
def ChangeSphereV(invalue):
	cmds.setAttr('pSphere1.zjhVX',invalue[0])
	cmds.setAttr('pSphere1.zjhVY',invalue[1])
	cmds.setAttr('pSphere1.zjhVZ',invalue[2])
def InstanceBricks(inPos):
	tempname=cmds.instance('brick0',lf=1)[0]
	#cmds.addAttr('bricksGrp',ln=tempname,at='short',k=1)
	cmds.setAttr(tempname+'.tx',inPos[0])
	cmds.setAttr(tempname+'.ty',inPos[1])
	cmds.setAttr(tempname+'.tz',inPos[2])
def InitBrickGameScene():
    #生成10行砖块,每行11块
    for i in range(10):
        for j in range(11):
            InstanceBricks([-500+j*100,1925-i*50,0])
    #启动tick线程
    keyMoveThread=thrd.Thread(target=EventsConsumer)#开一个线程专门用来检测和处理键盘事件
    keyMoveThread.start()
    sphereThread=thrd.Thread(target=UpdateSphere)#开一个线程专门用来更新小球位置
    sphereThread.start()
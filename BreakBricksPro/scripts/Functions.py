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
#新的碰撞检测算法(这是个通用算法,监测inSphere和inCube的碰撞情况,所有inCube都是从inCubeBase实例化而来,inCubeBase上有他们通用的拐角属性)
def DetectCollision(inSphere,inCube,inCubeBase):
	sptx=cmds.getAttr(inSphere+'.tx')
	spty=cmds.getAttr(inSphere+'.ty')
	cutx=cmds.getAttr(inCube+'.tx')
	cuty=cmds.getAttr(inCube+'.ty')
	sphereR=0.5*cmds.getAttr(inSphere+'.sx')
	helfCubeW=0.5*cmds.getAttr(inCube+'.sx')
	helfCubeH=0.5*cmds.getAttr(inCube+'.sy')
	if abs(sptx-cutx)>(sphereR+helfCubeW) or abs(spty-cuty)>(sphereR+helfCubeH):
		return 0#'距离太远'
	else:
		corn4Ps=[[cutx+helfCubeW,cuty+helfCubeH,0],[cutx-helfCubeW,cuty+helfCubeH,0],[cutx-helfCubeW,cuty-helfCubeH,0],[cutx-helfCubeW,cuty+helfCubeH,0]]#四个角上的点
		disDir=[sptx-cutx,spty-cuty,0]#小球在方块的方位
		orient=GetAngle(disDir)
		if orient<cmds.getAttr(inCubeBase+'.corn011'):
			return 1#'小于拐角1,返回1'
		elif orient<cmds.getAttr(inCubeBase+'.corn012'):
			if GetDistance([sptx,spty,0],corn4Ps[0])>sphereR:
				return 0#'大于拐角1半径，返回0'
			else:
				if orient<cmds.getAttr(inCubeBase+'.corn01b'):
					return 1#'交于角1,返回1'
				else:
					return 2#'交于角1,返回2'
		elif orient<cmds.getAttr(inCubeBase+'.corn021'):
			return 2#'小于拐角2,返回2'
		elif orient<cmds.getAttr(inCubeBase+'.corn022'):
			if GetDistance([sptx,spty,0],corn4Ps[1])>sphereR:
				return 0#'大于拐角2半径，返回0'
			else:
				if orient<cmds.getAttr(inCubeBase+'.corn02b'):
					return 2#'交于角2,返回2'
				else:
					return 3#'交于角2,返回3'
		elif orient<cmds.getAttr(inCubeBase+'.corn031'):
			return 3#'小于拐角3,返回3'
		elif orient<cmds.getAttr(inCubeBase+'.corn032'):
			if GetDistance([sptx,spty,0],corn4Ps[2])>sphereR:
				return 0#'大于拐角3半径，返回0'
			else:
				if orient<cmds.getAttr(inCubeBase+'.corn03b'):
					return 3#'交于角3,返回3'
				else:
					return 4#'交于角3,返回4'
		elif orient<cmds.getAttr(inCubeBase+'.corn041'):
			return 4#'小于拐角4,返回4'
		elif orient<cmds.getAttr(inCubeBase+'.corn042'):
			if GetDistance([sptx,spty,0],corn4Ps[3])>sphereR:
				return 0#'大于拐角4半径，返回0'
			else:
				if orient<cmds.getAttr(inCubeBase+'.corn04b'):
					return 4#'交于角4,返回4'
				else:
					return 1#'交于角4,返回1'
		else:
			return 1#'最后返回1'

#向键盘事件队列添加键盘事件(给定按键名称和相应的数值)
def AddEvent2evQueue(keyname,keyvalue):
	cmds.addAttr('opQueue',ln='event'+keyname,at='short',k=1,dv=keyvalue)
#从键盘事件队列的末尾移除事件
def RemoveEvent4evQueue(keyname):
	cmds.deleteAttr('opQueue',attribute='event'+keyname)

#改变inSphere的速度为invalue
def ChangeSphereV(inSphere,invalue):
	cmds.setAttr(inSphere+'.zjhVX',invalue[0])
	cmds.setAttr(inSphere+'.zjhVY',invalue[1])
	cmds.setAttr(inSphere+'.zjhVZ',invalue[2])

#时刻监测事件队列和更新场景
def Tick():
	gameRun=True
	while gameRun:
		if cmds.getAttr('pSphere1.ty')<-50:
			cmds.inViewMessage(amg='游戏结束!!',pos='midCenter',backColor=0x7B5353,fade=True,fadeInTime=0.2,fadeOutTime=0.2)
			print('游戏结束!!')
			gameRun=False
		if cmds.listAttr('opQueue',k=1)[-1]=='eventzjhright' and cmds.getAttr('pCube1.tx')<450:
			cmds.move(0.05*cmds.getAttr('pCube1.speed'),0,0,'pCube1',r=1)
		if cmds.listAttr('opQueue',k=1)[-1]=='eventzjhleft' and cmds.getAttr('pCube1.tx')>-450:
			cmds.move(-0.05*cmds.getAttr('pCube1.speed'),0,0,'pCube1',r=1)
		#时刻监测小球的速度值,并根据其速度时刻更新位置
		cmds.move(cmds.getAttr('pSphere1.zjhVX'),cmds.getAttr('pSphere1.zjhVY'),cmds.getAttr('pSphere1.zjhVZ'),'pSphere1',r=1)
		
		#随后就监测碰撞
		if cmds.getAttr('pSphere1.tx')>550-cmds.getAttr('pSphere1.sx') or cmds.getAttr('pSphere1.tx')<-550+cmds.getAttr('pSphere1.sx'):
			cmds.setAttr('pSphere1.zjhVX',-cmds.getAttr('pSphere1.zjhVX'))#触碰到两遍墙壁改变其X轴向上的速度
		#监测与pCube1的碰撞情况
		tempCollision=DetectCollision('pSphere1','pCube1','pCube1')
		if tempCollision==0:
			pass
		elif tempCollision==1 or tempCollision==3:
			cmds.setAttr('pSphere1.zjhVX',-cmds.getAttr('pSphere1.zjhVX'))#改变其X轴向上的速度
		elif tempCollision==2:#不可能为4的
			cmds.setAttr('pSphere1.zjhVY',-cmds.getAttr('pSphere1.zjhVY'))#改变其Y轴向上的速度
		#遍历所有的brick,监测它们与小球的碰撞情况
		for brick in cmds.listRelatives('bricksGrp',c=1):
			tempCollision=DetectCollision('pSphere1',brick,'brick0')
			if tempCollision==0:
				continue
			elif tempCollision==1 or tempCollision==3:
				cmds.setAttr('pSphere1.zjhVX',-cmds.getAttr('pSphere1.zjhVX'))#改变其X轴向上的速度
				cmds.delete(brick)
				break
			elif tempCollision==2 or tempCollision==4:
				cmds.setAttr('pSphere1.zjhVY',-cmds.getAttr('pSphere1.zjhVY'))#改变其Y轴向上的速度
				cmds.delete(brick)
				break

#实例化一个新的inCubeBase对象,并将其放置在inPos位置
def InstanceBricks(inCubeBase,inPos):
	tempname=cmds.instance(inCubeBase,lf=1)[0]
	cmds.setAttr(tempname+'.tx',inPos[0])
	cmds.setAttr(tempname+'.ty',inPos[1])
	cmds.setAttr(tempname+'.tz',inPos[2])
	return tempname
def InitBrickGameScene():
	#生成9行砖块,每行11块
	for i in range(9):
		for j in range(11):
			tempbrick=InstanceBricks('brick0',[-500+j*100,1925-i*50,0])
			cmds.parent(tempbrick,'bricksGrp')
	#启动tick线程
	TickThread=thrd.Thread(target=Tick)#专门为Tick函数开辟一个线程
	TickThread.start()
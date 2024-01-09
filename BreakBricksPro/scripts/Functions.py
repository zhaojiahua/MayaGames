from maya import cmds
from maya import utils
import math
import random
import json
import time
import threading as thrd
from Globals import projectPath
from Globals import ZjhGlobals

###全局变量
global Spacedoonce
Spacedoonce=False
global score
score=0
global scoreRate
scoreRate=0.0
global sortedScores
global sortedScoresRate
###全局变量

def Getcmdlines(path):
    with open(path,'r',encoding="UTF-8") as f:
        cmdlines=f.read()
    return cmdlines

registerBtnCommand_lines=Getcmdlines(projectPath+'scripts/CommandsLines/registerBtnCommand_lines.py')
okBtnCommand_lines=Getcmdlines(projectPath+'scripts/CommandsLines/okBtnCommand_lines.py')
okRegisterBtnCommand_lines=Getcmdlines(projectPath+'scripts/CommandsLines/okRegisterBtnCommand_lines.py')
cencelRegisterBtnCommand_lines=Getcmdlines(projectPath+'scripts/CommandsLines/cencelRegisterBtnCommand_lines.py')
restartBtnCommand_lines=Getcmdlines(projectPath+'scripts/CommandsLines/restartBtnCommand_lines.py')
gobackBtnCommand_lines=Getcmdlines(projectPath+'scripts/CommandsLines/gobackBtnCommand_lines.py')
accountCheckBoxOnCmdLines=Getcmdlines(projectPath+'scripts/CommandsLines/accountCheckBoxOnCmdLines.py')
accountCheckBoxOffCmdLines=Getcmdlines(projectPath+'scripts/CommandsLines/accountCheckBoxOffCmdLines.py')
nextLevelBtnCommand_lines=Getcmdlines(projectPath+'scripts/CommandsLines/nextLevelBtnCommand_lines.py')

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
	with open(projectPath+'data/ServerDatas/theRememberAccountAndPassword.json','r') as checkfr:
		theRemembers=json.load(checkfr)
	cmds.textField('qtAccountTextline',e=1,parent='zjhrowLayout1',font='boldLabelFont',height=50,text=theRemembers['theAccount'])
	#cmds.textField('countTextField',font='boldLabelFont',insertText='请输入帐号',height=50)
	cmds.setParent('..')
	cmds.text('seperateLabel2',l=' ',height=5,bgc=[0.4,0.3,0.3])#---------分隔符
	cmds.rowLayout('zjhrowLayout2',numberOfColumns=2,ad2=2)
	cmds.text('passwordLabel',l='  密码: ',font='boldLabelFont',height=50)
	#cmds.textField('passwordTextField',font='boldLabelFont',insertText='请输入密码',height=50,tcc=textChangedCommand_lines)
	#在这里我们自己实现输入框变星号的话是比较麻烦的,所以这里们借助Qt直接创建出一个密码框,然后把这个密码框放在这里就行了
	cmds.textField('qtPasswordTextline',e=1,parent='zjhrowLayout2',font='boldLabelFont',height=50,text=theRemembers['thePassword'])
	cmds.deleteUI('Form')
	cmds.setParent('..')
	cmds.text('seperateLabel3',l=' ',height=5,bgc=[0.4,0.3,0.3])#---------分隔符
	cmds.rowLayout('zjhrowLayout3',numberOfColumns=2,ad2=2,columnAttach=[(1,'left',50),(2,'right',50)])
	cmds.button('okBtn',l='  登录游戏  ',width=200,height=50,bgc=[0.4,0.35,0.35],c=okBtnCommand_lines)
	cmds.button('registerBtn',l='  注册帐号  ',width=200,height=50,bgc=[0.4,0.35,0.35],c=registerBtnCommand_lines)
	cmds.setParent('..')
	cmds.text('seperateLabel4',l=' ',height=5,bgc=[0.4,0.3,0.3])#---------分隔符
	cmds.rowLayout('zjhrowLayout4',numberOfColumns=3,ad2=2,columnAttach=[(1,'left',50),(2,'both',20),(3,'right',50)])
	cmds.checkBox('accountCheckBox',l=' 记住账号 ',bgc=[0.4,0.3,0.3],value=int(theRemembers['rememberAccount']),offCommand=accountCheckBoxOffCmdLines,onCommand=accountCheckBoxOnCmdLines)
	cmds.text('seperateLabel41',l='    ',height=5,bgc=[0.4,0.3,0.3])
	cmds.checkBox('passwordCheckBox',l=' 记住密码 ',bgc=[0.4,0.3,0.3],value=int(theRemembers['rememberPassword']),editable=int(theRemembers['rememberAccount']))
	cmds.setParent('..')
	cmds.showWindow('zjhStartWindow')
def CreateRegisterWindow():
    if cmds.window('zjhRegisterWindow',q=1,ex=1):
        cmds.deleteUI('zjhRegisterWindow')
    cmds.loadUI(uiFile=projectPath+'scripts/registerui.ui')
    cmds.window('zjhRegisterWindow',e=1,wh=[550,300],bgc=[0.28,0.31,0.3])
    cmds.button('okRegisterBtn',e=1,c=okRegisterBtnCommand_lines)
    cmds.button('cencelRegisterBtn',e=1,c=cencelRegisterBtnCommand_lines)
    cmds.showWindow('zjhRegisterWindow')
def CreateGameOverWindow():
	if cmds.window('zjhGameOverWindow',q=1,ex=1):
		cmds.deleteUI('zjhGameOverWindow')
	cmds.loadUI(uiFile=projectPath+'scripts/gameoverui.ui')
	cmds.showWindow('zjhGameOverWindow')
	cmds.window('zjhGameOverWindow',e=1,wh=[550,300],bgc=[0.31,0.28,0.3],visible=0)
	cmds.button('restartBtn',e=1,bgc=[0.38,0.3,0.31],c=restartBtnCommand_lines)
	cmds.button('gobackBtn',e=1,bgc=[0.38,0.3,0.31],c=gobackBtnCommand_lines)
def CreateGameWinWindow():
	if cmds.window('zjhGameWinWindow',q=1,ex=1):
		cmds.deleteUI('zjhGameWinWindow')
	cmds.loadUI(uiFile=projectPath+'scripts/gamewinui.ui')
	cmds.showWindow('zjhGameWinWindow')
	cmds.window('zjhGameWinWindow',e=1,wh=[550,300],bgc=[0.28,0.31,0.3],visible=0)
	cmds.button('restartBtn_win',e=1,bgc=[0.3,0.32,0.31],c=restartBtnCommand_lines)
	cmds.button('nextLevelBtn',e=1,bgc=[0.3,0.32,0.31],c=nextLevelBtnCommand_lines)

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
#新的碰撞检测算法(这是个通用算法,监测inSphere和inCube的碰撞情况)
def DetectCollision(inSphere,inCube):
	sptx=cmds.getAttr(inSphere+'.tx')
	spty=cmds.getAttr(inSphere+'.ty')
	cutx=cmds.getAttr(inCube+'.tx')
	cuty=cmds.getAttr(inCube+'.ty')
	sphereR=cmds.getAttr(inSphere+'.sx')
	helfCubeW=0.5*cmds.getAttr(inCube+'.sx')
	helfCubeH=0.5*cmds.getAttr(inCube+'.sy')
	if abs(sptx-cutx)>(sphereR+helfCubeW) or abs(spty-cuty)>(sphereR+helfCubeH):
		return 0#'距离太远'
	else:
		corn4Ps=[[cutx+helfCubeW,cuty+helfCubeH,0],[cutx-helfCubeW,cuty+helfCubeH,0],[cutx-helfCubeW,cuty-helfCubeH,0],[cutx-helfCubeW,cuty+helfCubeH,0]]#四个角上的点
		disDir=[sptx-cutx,spty-cuty,0]#小球在方块的方位
		orient=GetAngle(disDir)
		if orient<cmds.getAttr(inCube+'.corn011'):
			return 1#'小于拐角1,返回1'
		elif orient<cmds.getAttr(inCube+'.corn012'):
			if GetDistance([sptx,spty,0],corn4Ps[0])>sphereR:
				return 0#'大于拐角1半径，返回0'
			else:
				if orient<cmds.getAttr(inCube+'.corn01b'):
					return 1#'交于角1,返回1'
				else:
					return 2#'交于角1,返回2'
		elif orient<cmds.getAttr(inCube+'.corn021'):
			return 2#'小于拐角2,返回2'
		elif orient<cmds.getAttr(inCube+'.corn022'):
			if GetDistance([sptx,spty,0],corn4Ps[1])>sphereR:
				return 0#'大于拐角2半径，返回0'
			else:
				if orient<cmds.getAttr(inCube+'.corn02b'):
					return 2#'交于角2,返回2'
				else:
					return 3#'交于角2,返回3'
		elif orient<cmds.getAttr(inCube+'.corn031'):
			return 3#'小于拐角3,返回3'
		elif orient<cmds.getAttr(inCube+'.corn032'):
			if GetDistance([sptx,spty,0],corn4Ps[2])>sphereR:
				return 0#'大于拐角3半径，返回0'
			else:
				if orient<cmds.getAttr(inCube+'.corn03b'):
					return 3#'交于角3,返回3'
				else:
					return 4#'交于角3,返回4'
		elif orient<cmds.getAttr(inCube+'.corn041'):
			return 4#'小于拐角4,返回4'
		elif orient<cmds.getAttr(inCube+'.corn042'):
			if GetDistance([sptx,spty,0],corn4Ps[3])>sphereR:
				return 0#'大于拐角4半径，返回0'
			else:
				if orient<cmds.getAttr(inCube+'.corn04b'):
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

#传入带有数字的组合一个数字,然后用这个组里面的数字显示这个数字
def ShowIntDigits(digitsGrp,digit):
	gewei=digit%10
	shiwei=int(digit/10)%10
	baiwei=int(digit/100)%10
	qianwei=int(digit/1000)%10
	for i in range(10):
		cmds.setAttr(digitsGrp+'gewei_digit{}.visibility'.format(i),i == gewei)
		cmds.setAttr(digitsGrp+'shiwei_digit{}.visibility'.format(i),i == shiwei)
		cmds.setAttr(digitsGrp+'baiwei_digit{}.visibility'.format(i),i == baiwei)
		cmds.setAttr(digitsGrp+'qianwei_digit{}.visibility'.format(i),i == qianwei)
#设置小数
def ShowFloatDigits(digitsGrp,digit):
	gewei=int(digit)%10
	shiwei=int(digit/10)%10
	xiaoshuwei1=int(digit*10)%10
	xiaoshuwei2=int(digit*100)%10
	for i in range(10):
		cmds.setAttr(digitsGrp+'gewei_digit{}.visibility'.format(i),i == gewei)
		cmds.setAttr(digitsGrp+'shiwei_digit{}.visibility'.format(i),i == shiwei)
		cmds.setAttr(digitsGrp+'xiaoshuwei1_digit{}.visibility'.format(i),i == xiaoshuwei1)
		cmds.setAttr(digitsGrp+'xiaoshuwei2_digit{}.visibility'.format(i),i == xiaoshuwei2)

#速度加成(小球的速度越快会获得更多的额外分)(忽略z轴向的速度)
def SpeedExtraScore(spherespeed):
	tempspeed=math.sqrt(spherespeed[0]*spherespeed[0]+spherespeed[1]*spherespeed[1])
	if tempspeed >3.6:
		return 9
	elif tempspeed>3.2:
		return 6
	elif tempspeed>2.8:
		return 3
	else:
		return 0

#游戏结束的时候结算得分和排名
def SettleAccounts():
	global score
	global scoreRate
	global sortedScores
	global sortedScoresRate
	with open(projectPath+'data/ServerDatas/accountsMaxScores.json','r') as sfr:
		accountScores=json.load(sfr)
	if int(accountScores[ZjhGlobals.CurrentAccountName])<score:
		accountScores[ZjhGlobals.CurrentAccountName]=str(score)
		with open(projectPath+'data/ServerDatas/accountsMaxScores.json','w') as sfw:
			json.dump(accountScores,sfw)
	sortedScores=sorted(accountScores.items(),key=lambda i:i[1],reverse=True)#对最终得分进行排序
	with open(projectPath+'data/ServerDatas/accountsMaxScoresRate.json','r') as srfr:
		accountScoresrate=json.load(srfr)
	if float(accountScoresrate[ZjhGlobals.CurrentAccountName])<scoreRate:
		accountScoresrate[ZjhGlobals.CurrentAccountName]=str(scoreRate)
		with open(projectPath+'data/ServerDatas/accountsMaxScoresRate.json','w') as srfw:
			json.dump(accountScoresrate,srfw)
	sortedScoresRate=sorted(accountScoresrate.items(),key=lambda i:i[1],reverse=True)#对最终得分率进行排序
			

#时刻监测事件队列和更新场景
def Tick():
	global score
	global scoreRate
	gametime=0
	pretime=time.time()
	gameRun=True
	global sphereBaseSpeedX
	global sphereBaseSpeedY
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
			time.sleep(0.5)
			for item in sortedScores:
				cmds.text('temptet1',label=item,parent='horizontalLayout')
				time.sleep(0.05)

		if time.time()-pretime >= 1:
			gametime+=1
			ShowIntDigits('haoshi_',gametime)
			scoreRate=score/gametime
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
	cmds.file(projectPath+'scenes/Scene1_main.ma', open=1,force=1)
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
	cmds.select('pSphere1')
	#启动tick线程
	TickThread=thrd.Thread(target=Tick)#专门为Tick函数开辟一个线程
	TickThread.start()
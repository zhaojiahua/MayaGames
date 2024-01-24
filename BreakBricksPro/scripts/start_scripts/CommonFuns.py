from maya import cmds
import math
import random
import json
import time
from Globals import projectPath
from Globals import ZjhGlobals

def Getcmdlines(path):
    with open(path,'r',encoding="UTF-8") as f:
        cmdlines=f.read()
    return cmdlines

registerBtnCommand_lines=Getcmdlines(projectPath+'scripts/start_scripts/CommandsLines/registerBtnCommand_lines.py')
okBtnCommand_lines=Getcmdlines(projectPath+'scripts/start_scripts/CommandsLines/okBtnCommand_lines.py')
okRegisterBtnCommand_lines=Getcmdlines(projectPath+'scripts/start_scripts/CommandsLines/okRegisterBtnCommand_lines.py')
cencelRegisterBtnCommand_lines=Getcmdlines(projectPath+'scripts/start_scripts/CommandsLines/cencelRegisterBtnCommand_lines.py')
restartBtnCommand_lines=Getcmdlines(projectPath+'scripts/start_scripts/CommandsLines/restartBtnCommand_lines.py')
gobackBtnCommand_lines=Getcmdlines(projectPath+'scripts/start_scripts/CommandsLines/gobackBtnCommand_lines.py')
accountCheckBoxOnCmdLines=Getcmdlines(projectPath+'scripts/start_scripts/CommandsLines/accountCheckBoxOnCmdLines.py')
accountCheckBoxOffCmdLines=Getcmdlines(projectPath+'scripts/start_scripts/CommandsLines/accountCheckBoxOffCmdLines.py')
nextLevelBtnCommand_lines=Getcmdlines(projectPath+'scripts/start_scripts/CommandsLines/nextLevelBtnCommand_lines.py')
addJiFenBangUICommand_lines=Getcmdlines(projectPath+'scripts/start_scripts/CommandsLines/addJiFenBangUI_lines.py')

#Start界面
def CreateStartWindow():
	if cmds.window('zjhStartWindow',q=1,ex=1):
		cmds.deleteUI('zjhStartWindow')
	cmds.window('zjhStartWindow',title='游戏登录界面',wh=[550,400],bgc=[0.4,0.3,0.3])
	cmds.columnLayout('zjhColumnLayout1',adjustableColumn=1)
	cmds.text('loginLabel',l='请先登录zjhMayaGame盒子',font='boldLabelFont',height=50,bgc=[0.4,0.3,0.3])#---------分隔符
	cmds.text('seperateLabel1',l=' ',height=10,bgc=[0.4,0.3,0.3])#---------分隔符
	cmds.rowLayout('zjhrowLayout1',numberOfColumns=2,ad2=2)
	cmds.text('countLabel',l='  帐号: ',font='boldLabelFont',height=50)
	cmds.loadUI( uiFile=projectPath+'scripts/start_scripts/passwordui.ui')#从Qt.ui文件提取一个文本框对象
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

icBtnsList=['brickGame_icBtn','tetris_icBtn','raceCar_icBtn','moreGames_icBtn']
def IconChangeColor(icBtns,act_icBtn):
	for item in icBtnsList:
		cmds.iconTextButton(item,e=1,bgc=[0.4,0.32,0.44])
	cmds.iconTextButton(act_icBtn,e=1,bgc=[0.64,0.3,0.54])
def BrickGame_icBtn_cmd():
	IconChangeColor(icBtnsList,'brickGame_icBtn')
	cmds.image('GBviewimage',e=1,image=projectPath+'sourceimages/2dPaintTextures/SlideBrickPictures/jiemian01.png')
	cmds.button('StartGameBtn',e=1,c=Getcmdlines(projectPath+'scripts/brickGame_scripts/CommandsLines/StartGameCommand_lines.py'))
def Tetris_icBtn_cmd():
	IconChangeColor(icBtnsList,'tetris_icBtn')
	cmds.image('GBviewimage',e=1,image=projectPath+'sourceimages/2dPaintTextures/TetrisPictures/tetris001.png')
	cmds.button('StartGameBtn',e=1,c=Getcmdlines(projectPath+'scripts/tetris_scripts/CommandsLines/StartGameCommand_lines.py'))
def RaceCar_icBtn_cmd():
	IconChangeColor(icBtnsList,'raceCar_icBtn')
	cmds.image('GBviewimage',e=1,image=projectPath+'sourceimages/2dPaintTextures/RaceCarPictures/racecar001.png')
	cmds.button('StartGameBtn',e=1,c=Getcmdlines(projectPath+'scripts/raceCar_scripts/CommandsLines/StartGameCommand_lines.py'))
def MoreGames_icBtn_cmd():
	IconChangeColor(icBtnsList,'moreGames_icBtn')
	cmds.image('GBviewimage',e=1,image=projectPath+'sourceimages/2dPaintTextures/MoreGamesPictures/moregames.png')
def CreateGameBoxWindow():
	if cmds.window('zjhGameBoxWindow',q=1,ex=1):
		cmds.deleteUI('zjhGameBoxWindow')
	cmds.window('zjhGameBoxWindow',title='Maya游戏盒子',wh=[700,420],bgc=[0.38,0.35,0.4])
	cmds.columnLayout('zjhGBColumnLayout1',adjustableColumn=1)
	cmds.text('GBseperateLabel1',l=' ',height=10,bgc=[0.38,0.35,0.4])#---------分隔符
	cmds.rowLayout('zjhGBrowLayout1',numberOfColumns=2,ad2=2,columnAttach=[(1,'both',10),(2,'both',10)])#----------------------------游戏按钮和预览页面
	cmds.columnLayout('zjhGBColumnLayout1',adjustableColumn=1)#-------游戏按钮
	cmds.text('countLabel',l='  游戏列表: ',font='boldLabelFont',height=30)
	cmds.text(l=' ',height=5,bgc=[0.38,0.35,0.4])#---------分隔符
	cmds.iconTextButton( 'brickGame_icBtn',bgc=[0.4,0.32,0.44],style='iconAndTextHorizontal', image1=projectPath+'/sourceimages/icons/brickgame_min.png',label='Brick Game 滑块接球',c=BrickGame_icBtn_cmd)
	cmds.text(l=' ',height=5,bgc=[0.38,0.35,0.4])#---------分隔符
	cmds.iconTextButton( 'tetris_icBtn',bgc=[0.4,0.32,0.44],style='iconAndTextHorizontal', image1=projectPath+'/sourceimages/icons/tetris_min.png',label='Tetris 俄罗斯方块',c=Tetris_icBtn_cmd)
	cmds.text(l=' ',height=5,bgc=[0.38,0.35,0.4])#---------分隔符
	cmds.iconTextButton( 'raceCar_icBtn',bgc=[0.4,0.32,0.44],style='iconAndTextHorizontal', image1=projectPath+'/sourceimages/icons/raceCar_min.png',label='race car 极品飞车',c=RaceCar_icBtn_cmd)
	cmds.text(l=' ',height=5,bgc=[0.38,0.35,0.4])#---------分隔符
	cmds.iconTextButton( 'moreGames_icBtn',bgc=[0.4,0.32,0.44],style='iconAndTextHorizontal', image1=projectPath+'/sourceimages/icons/moreGames_min.png',label='更多游戏···',c=MoreGames_icBtn_cmd)
	cmds.setParent('..')
	cmds.image('GBviewimage',image=projectPath+'sourceimages/2dPaintTextures/mayagame.png')
	cmds.setParent('..')
	cmds.text(l=' ',height=10,bgc=[0.38,0.35,0.4])#---------分隔符
	cmds.rowLayout('zjhGBrowLayout2',numberOfColumns=2,ad2=1,columnAttach=[(1,'left',20),(2,'right',20)])#----------------------------开始游戏按钮
	cmds.text(l=' ',bgc=[0.38,0.35,0.4])#---------分隔符
	cmds.button('StartGameBtn',l='  开始游戏  ',width=200,height=50,bgc=[0.4,0.32,0.44],c="print('请先选择游戏')")
	cmds.showWindow('zjhGameBoxWindow')

def CreateRegisterWindow():
    if cmds.window('zjhRegisterWindow',q=1,ex=1):
        cmds.deleteUI('zjhRegisterWindow')
    cmds.loadUI(uiFile=projectPath+'scripts/start_scripts/registerui.ui')
    cmds.window('zjhRegisterWindow',e=1,wh=[550,300],bgc=[0.28,0.31,0.3])
    cmds.button('okRegisterBtn',e=1,c=okRegisterBtnCommand_lines)
    cmds.button('cencelRegisterBtn',e=1,c=cencelRegisterBtnCommand_lines)
    cmds.showWindow('zjhRegisterWindow')
def CreateGameOverWindow():
	if cmds.window('zjhGameOverWindow',q=1,ex=1):
		cmds.deleteUI('zjhGameOverWindow')
	cmds.loadUI(uiFile=projectPath+'scripts/start_scripts/gameoverui.ui')
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
	cmds.loadUI(uiFile=projectPath+'scripts/start_scripts/gamewinui.ui')
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


#键盘按键接口函数(不同的游戏里都要重写这些函数)
def LeftPressF():
	pass
def LeftReleaseF():
	pass
def RightPressF():
	pass
def RightReleaseF():
	pass
def SpacePressF():
	pass
def SpaceReleaseF():
	pass

#传入带有数字的组合一个数字,然后用这个组里面的数字显示这个数字
def ShowIntDigits(digitsGrp,digit):
	gewei=digit%10
	shiwei=int(digit/10)%10
	baiwei=int(digit/100)%10
	qianwei=int(digit/1000)%10
	cmds.setAttr(digitsGrp+'gewei_chilun.rotateX',36*gewei)
	cmds.setAttr(digitsGrp+'shiwei_chilun.rotateX',36*shiwei)
	cmds.setAttr(digitsGrp+'baiwei_chilun.rotateX',36*baiwei)
	cmds.setAttr(digitsGrp+'qianwei_chilun.rotateX',36*qianwei)
#设置小数
def ShowFloatDigits(digitsGrp,digit):
	gewei=int(digit)%10
	shiwei=int(digit/10)%10
	xiaoshuwei1=int(digit*10)%10
	xiaoshuwei2=int(digit*100)%10
	cmds.setAttr(digitsGrp+'gewei_chilun.rotateX',36*gewei)
	cmds.setAttr(digitsGrp+'shiwei_chilun.rotateX',36*shiwei)
	cmds.setAttr(digitsGrp+'xiaoshuwei1_chilun.rotateX',36*xiaoshuwei1)
	cmds.setAttr(digitsGrp+'xiaoshuwei2_chilun.rotateX',36*xiaoshuwei2)

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
	with open(projectPath+'data/ServerDatas/accountsMaxScores.json','r') as sfr:
		accountScores=json.load(sfr)
	if int(accountScores[ZjhGlobals.CurrentAccountName])<ZjhGlobals.currentscore:
		accountScores[ZjhGlobals.CurrentAccountName]=str(ZjhGlobals.currentscore)
		with open(projectPath+'data/ServerDatas/accountsMaxScores.json','w') as sfw:
			json.dump(accountScores,sfw)
	for item in accountScores:
		accountScores[item]=int(accountScores[item])#先把字典里的字符转换成整形数字
	ZjhGlobals.sortedScores=sorted(accountScores.items(),key=lambda i:i[1],reverse=True)#对最终得分进行排序
	with open(projectPath+'data/ServerDatas/accountsMaxScoresRate.json','r') as srfr:
		ZjhGlobals.accountScoresrate=json.load(srfr)
	if float(ZjhGlobals.accountScoresrate[ZjhGlobals.CurrentAccountName])<ZjhGlobals.currentscoreRate:
		ZjhGlobals.accountScoresrate[ZjhGlobals.CurrentAccountName]=str(ZjhGlobals.currentscoreRate)
		with open(projectPath+'data/ServerDatas/accountsMaxScoresRate.json','w') as srfw:
			json.dump(ZjhGlobals.accountScoresrate,srfw)			

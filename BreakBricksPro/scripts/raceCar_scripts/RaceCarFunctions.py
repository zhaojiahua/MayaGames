from maya import utils
import threading as thrd
from CommonFuns import *
from ZjhClasses import *
###全局变量
global gameRun
gameRun=True
global refuelTime
refuelTime=0.0
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

def SSmoothCrv(inx):
	cmds.setAttr('S_Smooth_Crv.input',inx)
	return cmds.getAttr('S_Smooth_Crv.output')
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
	global refuelTime
	cmds.setAttr('theCar.refuel',-10)
	refuelTime=time.time()
def DownReleaseF():
	cmds.setAttr('theCar.refuel',0)
def UpPressF():
	global refuelTime
	cmds.setAttr('theCar.refuel',11)
	refuelTime=time.time()
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
	global refuelTime
	refuelTime=time.time()
	cmds.setAttr('theCar.refuel',0)
	while gameRun:
		if time.time()-tickpretime>=0.02:
			tickpretime=time.time()
			carmass=cmds.getAttr('theCar.carMass')
			cartoward=ZVector(cmds.getAttr('theCar.toward')[0])#汽车前方向
			carupward=ZVector(cmds.getAttr('theCar.upward')[0])#汽车的上方向
			frontWheelward=ZVector(cmds.getAttr('theCar.frontWheelward')[0])#汽车前轮的方向(初始状态都是和汽车前方方向保持一致,(默认此汽车为前驱))
			carvelocity=ZVector(cmds.getAttr('theCar.carVelocity')[0])
			carvelocity_dir=carvelocity.Normalize()
			carspeedS=carvelocity.LengthSquare()	#速度的模长既是速率的大小
			#油门踩下的那一刻,汽车牵引力随时间变化(0-1) 接下来是受力分析(carPower和carTorsion是汽车固有性能参数)
			DrForce=200*cmds.getAttr('theCar.refuel')*SSmoothCrv(10*cmds.getAttr('theCar.carPower')*(time.time()-refuelTime))*frontWheelward
			#把发动机的驱动力分解成汽车前轮方向和汽车前向相切的方向(一个用于计算牵引力,一个用于计算汽车旋转扭矩)
			ForceAndTorque=carvelocity.DecomposeVector(cartoward)
			#接下来是转动惯量和角速度的分析(转动惯量和车身质量和轴距有关)
			angleVelocity_dir=cartoward.Cross(ForceAndTorque[1]).Normalize()#角加速度的方向
			angleVelocity=ForceAndTorque[1].Length()*angleVelocity_dir
			cmds.setAttr('theCar.angleVelocity',angleVelocity.x,angleVelocity.y,angleVelocity.z)
			rotMatrix=ZMatrix.GetMatrixByAxisAngle(angleVelocity_dir,angleVelocity.Length())#求出旋转矩阵
			cartoward=rotMatrix*cartoward##############更新汽车的前方向
			cmds.setAttr('theCar.toward',cartoward.x,cartoward.y,cartoward.z)
			frontWheelward=rotMatrix*frontWheelward#######更新汽车前轮的方向
			cmds.setAttr('theCar.frontWheelward',frontWheelward.x,frontWheelward.y,frontWheelward.z)
			orgtoward=ZVector([0,0,-1])
			tn=(orgtoward.Cross(cartoward)).Normalize()
			tradius=math.acos(orgtoward.CosToVector(cartoward))
			orgRotMatrix=ZMatrix.GetMatrixByAxisAngle(tn,tradius)
			cmds.xform('theCar',ro=orgRotMatrix.GetEulerXYZ())#更新汽车的旋转
			#下面是运动速度的更新
			Windage=-6*carspeedS*carvelocity_dir	#风阻(空气阻力和速率的平方成正比,方向与运动方向相反)
			Friction=ZVector([0,0,0])	#摩擦力和车身的重力成正比
			if carspeedS>0.001:
				Friction=-0.009*carmass*carvelocity_dir	#动摩擦(方向与运动方向相反)
			else:
				#print(DrForce.Length())
				if DrForce.Length()<0.01*carmass:	#静摩擦(牵引力方向相反)
					Friction=-1*DrForce
				cmds.setAttr('theCar.carVelocity',0,0,0)
				carvelocity=ZVector([0,0,0])
			acc=(DrForce+Friction+Windage)/cmds.getAttr('theCar.carMass')#更新加速度
			ncarvelocity=carvelocity+acc#更新速度
			cmds.setAttr('theCar.carVelocity',ncarvelocity.x,ncarvelocity.y,ncarvelocity.z)
			cmds.move(ncarvelocity.x,ncarvelocity.y,ncarvelocity.z,'theCar',r=1)#更新位置

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
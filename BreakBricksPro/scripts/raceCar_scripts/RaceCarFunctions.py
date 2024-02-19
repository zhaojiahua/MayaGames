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
	utils.executeInMainThreadWithResult("cmds.setAttr('S_Smooth_Crv.input',{})".format(inx))
	return cmds.getAttr('S_Smooth_Crv.output')
#键盘按键接口函数
def TurnFrontWheel(indir):
	if indir != 0:
		rotMatrix=ZMatrix.GetMatrixByAxisAngle(indir*ZVector(cmds.getAttr('theCar.upward')[0]),0.005)#求出旋转矩阵
		frontWheelward=rotMatrix*ZVector(cmds.getAttr('theCar.frontWheelward')[0]).Normalize()
		cmds.setAttr('theCar.frontWheelward',frontWheelward.x,frontWheelward.y,frontWheelward.z)
		#旋转前轮朝向
		cmds.rotate(0,indir*0.286478866,0,'qianlunL_grp',r=1)
		cmds.rotate(0,indir*0.286478866,0,'qianlunR_grp',r=1)
	else:
		frontWheelward=ZVector(cmds.getAttr('theCar.frontWheelward')[0]).Normalize()
		toward=ZVector(cmds.getAttr('theCar.toward')[0]).Normalize()
		if frontWheelward!=toward:
			cosvalue=round(frontWheelward.CosToVector(toward),10)
			#print(cosvalue)
			if math.acos(cosvalue)<0.005:
				frontWheelward=toward
			else:
				#恢复前轮朝向(只要不打转向,就尽量使前轮朝向和汽车方向一致)
				frontWheelward=ZVector.TurnToVector(frontWheelward,toward,0.005)
			cmds.setAttr('theCar.frontWheelward',frontWheelward.x,frontWheelward.y,frontWheelward.z)
		tdir=1
		if cmds.getAttr('qianlunL_grp.ry')>0:
			tdir=-1
		cmds.rotate(0,tdir*0.286478866,0,'qianlunL_grp',r=1)
		cmds.rotate(0,tdir*0.286478866,0,'qianlunR_grp',r=1)
def LeftPressF():
	cmds.setAttr('theCar.TurnDirection',1)
def LeftReleaseF():
	cmds.setAttr('theCar.TurnDirection',0)
def RightPressF():
	cmds.setAttr('theCar.TurnDirection',-1)
def RightReleaseF():
	cmds.setAttr('theCar.TurnDirection',0)
def DownPressF():
	global refuelTime
	refuelTime=time.time()
	cmds.setAttr('theCar.refuel',-0.6)
def DownReleaseF():
	cmds.setAttr('theCar.refuel',0)
def UpPressF():
	global refuelTime
	refuelTime=time.time()
	cmds.setAttr('theCar.refuel',1)
def UpReleaseF():
	cmds.setAttr('theCar.refuel',0)
def SpacePressF():
	cmds.setAttr('theCar.brake',30)
def SpaceReleaseF():
	cmds.setAttr('theCar.brake',1)

#首先把所有的解算数据加载进来
global allFrames
global allGlassFrames
global allCameraFrames
allFrames=[]
allGlassFrames=[]
allCameraFrames=[]
luzhang1=ZCrushes()
luzhang2=ZCrushes()
luzhang3=ZCrushes()
luzhang4=ZCrushes()
luzhang_glass=ZCrushes()
zcamera1=ZCamera()
def LuZhangPlayAnim():
	global allFrames
	global allGlassFrames
	luzhang1.PlayAnim(allFrames)
	luzhang2.PlayAnim(allFrames)
	luzhang3.PlayAnim(allFrames)
	luzhang4.PlayAnim(allFrames)
	luzhang_glass.PlayAnim(allGlassFrames)

#时刻监测事件队列和更新场景
def Tick():
	ZjhGlobals.gametime=0
	pretime=time.time()
	tickpretime=time.time()
	animpretime=time.time()#动画播放的时间间隔

	#首先把所有的解算数据加载进来
	global allFrames
	allFrames=ZCrushes.LoadAllFrames(projectPath+"scenes/Houdini/outDatas/Roadblock1",200)
	global allGlassFrames
	allGlassFrames=ZCrushes.LoadAllFrames(projectPath+"scenes/Houdini/outDatas/Roadblock2",200)
	global allCameraFrames
	allCameraFrames=ZCamera.LoadAllFrames(projectPath+"scenes/Maya/camShake.json")
	zcamera1.ZInit('camera1_grp')
	luzhang1.ZInit("luzhang1_grp")
	luzhang2.ZInit("luzhang2_grp")
	luzhang3.ZInit("luzhang3_grp")
	luzhang4.ZInit("luzhang4_grp")
	luzhang_glass.ZInit("glasses_grp")
	luzhang1.mFrame=8
	luzhang2.mFrame=8
	luzhang3.mFrame=8
	luzhang4.mFrame=8
	luzhang_glass.mFrame=26

	global refuelTime
	refuelTime=time.time()
	cmds.setAttr('theCar.refuel',0)
	#获取机车的固定属性
	lunzhouchang=cmds.getAttr('qianlun_grp.lunZhouChang')#获取轮周长(默认前后轮周长一样)
	carpower=cmds.getAttr('theCar.carPower')
	carmass=cmds.getAttr('theCar.carMass')
	while gameRun:
		if time.time()-tickpretime>=0.02:
			tickpretime=time.time()
			TurnFrontWheel(cmds.getAttr('theCar.TurnDirection'))
			cartoward=ZVector(cmds.getAttr('theCar.toward')[0])#汽车前方向
			carupward=ZVector(cmds.getAttr('theCar.upward')[0])#汽车的上方向
			frontWheelward=ZVector(cmds.getAttr('theCar.frontWheelward')[0]).Normalize()#汽车前轮的方向(初始状态都是和汽车前方方向保持一致,(默认此汽车为前驱))
			carvelocity=ZVector(cmds.getAttr('theCar.carVelocity')[0])
			carvelocity_dir=carvelocity.Normalize()
			#碰撞检测(会影响车速)
			thecarBB=cmds.xform('theCar',q=1,bb=1)			
			if luzhang1.DetactBBCollision(thecarBB):
				luzhang1.Brock()
				carvelocity*=0.5#碰撞减速50%
				zcamera1.Shake()#相机抖动
			if luzhang2.DetactBBCollision(thecarBB):
				luzhang2.Brock()
				carvelocity*=0.5
				zcamera1.Shake()#相机抖动
			if luzhang3.DetactBBCollision(thecarBB):
				luzhang3.Brock()
				carvelocity*=0.5
				zcamera1.Shake()#相机抖动
			if luzhang4.DetactBBCollision(thecarBB):
				luzhang4.Brock()
				carvelocity*=0.5
				zcamera1.Shake()#相机抖动
			if luzhang_glass.DetactBBCollision(thecarBB):
				luzhang_glass.Brock()
				carvelocity*=-0.6	#碰撞减速100%
				zcamera1.Shake()#相机抖动
			carspeedS=carvelocity.LengthSquare()	#速度的模长既是速率的大小
			#油门踩下的那一刻,汽车牵引力随时间变化(0-1) 接下来是受力分析(carPower和carTorsion是汽车固有性能参数,它们分别决定了汽车百公里加速的时间和最高时速)
			DrForce=cmds.getAttr('theCar.refuel')*SSmoothCrv(2*carpower*(time.time()-refuelTime))*frontWheelward
			#下面是运动速度的更新
			Windage=-1*carspeedS*carvelocity_dir	#风阻(空气阻力和速率的平方成正比,方向与运动方向相反-(空气阻力的公式：F=(1/2)CρSV^2,由公式可知风阻与汽车速度的平方成正比))
			Friction=ZVector([0,0,0])	#摩擦力和车身的重力成正比
			if carspeedS>0.001:
				Friction=-0.001*cmds.getAttr('theCar.brake')*carmass*carvelocity_dir	#动摩擦(方向与运动方向相反)(滚动摩擦,刹车的时候是静摩擦,直接增大10倍)
			else:
				if DrForce.Length()<0.0012*carmass:	#静摩擦(牵引力方向相反)(静滚动摩擦)
					Friction=-1*DrForce
				cmds.setAttr('theCar.carVelocity',0,0,0)
				carvelocity=ZVector([0,0,0])
			acc=(DrForce+Friction+Windage)/carmass#更新加速度
			carvelocity=carvelocity+acc#更新速度
			cmds.setAttr('theCar.carVelocity',carvelocity.x,carvelocity.y,carvelocity.z)
			carspeed=carvelocity.Length()
			cmds.setAttr('theCar.speed',carspeed*80)#这里乘80是为了使数据接近现实汽车时速(最高时速达200左右)
			cmds.setAttr('mabiao_zhizhen.rz',-carspeed*180/4)#码表
			cmds.move(carvelocity.x,carvelocity.y,carvelocity.z,'theCar',r=1)#更新位置
			temprotx=-1*carspeed/lunzhouchang*360#旋转大小
			if carvelocity.CosToVector(cartoward)<0:#用汽车速度的方向和汽车的前方向判断车轮的转动方向
				temprotx*=-1
			cmds.rotate(temprotx,0,0,'qianlunL',r=1)#更新前轮的转动
			cmds.rotate(temprotx,0,0,'qianlunR',r=1)#更新前轮的转动
			cmds.rotate(temprotx,0,0,'houlun_grp',r=1)#更新后轮的转动

			#接下来是转动惯量和角速度的分析(转动惯量和车身质量和轴距有关)
			angleVelocity_dir=cartoward.Cross(frontWheelward).Normalize()#角速度的方向
			if carvelocity.CosToVector(frontWheelward)<0:
				angleVelocity_dir*=-1
			angleVelocity_value=0.1*carspeed*(1-frontWheelward.CosToVector(cartoward))#角速度的大小
			angleVelocity=angleVelocity_value*angleVelocity_dir
			cmds.setAttr('theCar.angleVelocity',angleVelocity.x,angleVelocity.y,angleVelocity.z)
			rotMatrix=ZMatrix.GetMatrixByAxisAngle(angleVelocity_dir,angleVelocity_value)#求出旋转矩阵
			cartoward=rotMatrix*cartoward##############更新汽车的前方向
			cmds.setAttr('theCar.toward',cartoward.x,cartoward.y,cartoward.z)
			frontWheelward=rotMatrix*frontWheelward#######更新汽车前轮的方向
			cmds.setAttr('theCar.frontWheelward',frontWheelward.x,frontWheelward.y,frontWheelward.z)
			orgtoward=ZVector([0,0,-1])
			orgRotMatrix=ZMatrix.GetMatrixByAxisAngle(orgtoward.Cross(cartoward).Normalize(),math.acos(orgtoward.CosToVector(cartoward)))
			cmds.xform('theCar',ro=orgRotMatrix.GetEulerXYZ())#更新汽车的旋转
			#相机跟进
			zcamera1.Follow('theCar')
		if time.time()-animpretime>0.04:
			LuZhangPlayAnim()#传入不同的状态,播放不同的动画
			zcamera1.PlayAnim(allCameraFrames)#播放相机抖动动画
			animpretime=time.time()
		if time.time()-pretime >= 1:
			ZjhGlobals.gametime+=1
			ShowIntDigits('haoshi_',ZjhGlobals.gametime)
			pretime=time.time()

def InitRaceCarGameScene():
	cmds.file(projectPath+'scenes/Scene_RaceCar.ma', open=1,force=1)
	#初始化Tetris游戏场景
	gameRun=True
	#启动tick线程
	TickThread=thrd.Thread(target=Tick)#专门为Tick函数开辟一个线程
	TickThread.start()

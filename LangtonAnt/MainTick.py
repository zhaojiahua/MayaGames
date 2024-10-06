import time
import threading
from maya import cmds
from maya import utils
import Globals as Gl
from Globals import *
#定义一个Tick函数,每帧都执行
def Tick():
    print('tick')
#自定义时间间隔调用一次的Update函数
def Update():
    dpicoord=dpi.GetAntCoord(cmds.xform('ant',q=1,t=1,ws=1))
    if(not dpi.metas[dpicoord[0]*10000+dpicoord[1]]):
        Gl.antDirection=Gl.antDirection.RotateByAxisAngle(Vector3D([0,1,0]),1.5707963)
        cmds.setAttr('ant.rotateY',cmds.getAttr('ant.rotateY')-90)
        tdcu=cmds.duplicate('baseCU',n='CU_{}_{}'.format(dpicoord[0],dpicoord[1]))[0]
        dpi.metas[dpicoord[0]*10000+dpicoord[1]]=tdcu
        cmds.xform(tdcu,t=cmds.xform('ant',q=1,t=1))
        cmds.setAttr(tdcu+'.visibility',1)
        cmds.sets(tdcu,e=1,fe='lambert3SG')
        cmds.setAttr(tdcu+'.ShadingGroup',3)
    else:
        tdcu=dpi.metas[dpicoord[0]*10000+dpicoord[1]]
        if(cmds.getAttr(tdcu+'.ShadingGroup')==2):
            Gl.antDirection=Gl.antDirection.RotateByAxisAngle(Vector3D([0,1,0]),1.5707963)
            cmds.setAttr('ant.rotateY',cmds.getAttr('ant.rotateY')-90)
            cmds.setAttr(tdcu+'.ShadingGroup',3)
            cmds.sets(tdcu,e=1,fe='lambert3SG')
        else:
            Gl.antDirection=Gl.antDirection.RotateByAxisAngle(Vector3D([0,1,0]),-1.5707963)
            cmds.setAttr('ant.rotateY',cmds.getAttr('ant.rotateY')+90)
            cmds.setAttr(tdcu+'.ShadingGroup',2)
            cmds.sets(tdcu,e=1,fe='lambert2SG')
        cmds.xform(tdcu,t=cmds.xform('ant',q=1,t=1))
    currentpos=Vector3D(cmds.xform('ant',q=1,t=1,ws=1))
    cmds.xform('ant',t=(currentpos+Gl.antDirection).GetList(),ws=1)
#线程调用的函数(游戏运行时一直运行中的线程)
def MainRunThread():
    start_time=time.time()
    current_time=time.time()
    count=0
    while Gl.gamerun:
        utils.executeInMainThreadWithResult(Tick)
        current_time = time.time()
        if current_time-start_time > 1.0/Gl.moveSpeed:
            utils.executeInMainThreadWithResult(Update)
            start_time=current_time

def GetCmdLines(path):
    with open(path) as f:
        return f.read()
    return "print('{} read nothing !')".format(path)
def ShowStartUI():
    if cmds.window('LangtonStartUI',exists=1):
        cmds.deleteUI('LangtonStartUI')
    StartUI=cmds.loadUI(f=Gl.workRoot+'scripts/startMenu.ui',v=1)
    cmds.showWindow(StartUI)
    cmds.button('StartStopBtn',e=1,bgc=[0.2,0.2,0.4],c=GetCmdLines(Gl.workRoot+'scripts/BtnCmdLines/StartBtn_cmdlines.py'))
    cmds.intSlider('speedSlider',e=1,bgc=Gl.SpeedSliderColorGradient.GetColor(Gl.moveSpeed/100.0),min=1,max=100,value=Gl.moveSpeed,dc=GetCmdLines(Gl.workRoot+'scripts/BtnCmdLines/SpeedSliderBtn_cmdlines.py'))
    cmds.button('slowBtn',e=1,bgc=[0.2,0.3,0.2],c=GetCmdLines(Gl.workRoot+'scripts/BtnCmdLines/SlowBtn_cmdlines.py'))
    cmds.button('speedUpBtn',e=1,bgc=[0.3,0.2,0.2],c=GetCmdLines(Gl.workRoot+'scripts/BtnCmdLines/UpspeedBtn_cmdlines.py'))
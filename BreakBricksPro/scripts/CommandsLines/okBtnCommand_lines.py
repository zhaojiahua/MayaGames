import json
import Functions
from Globals import projectPath
theaccount=cmds.textField('qtAccountTextline',q=1,text=1)
thepassword=cmds.textField('qtPasswordTextline',q=1,text=1)
#按钮动画效果

if theaccount == '' or thepassword == '':
    cmds.inViewMessage(amg='请输入帐号和密码',pos='midCenter',backColor=0x7B5353,fade=True,fadeInTime=0.2,fadeOutTime=0.2)
else:
    with open(projectPath+'data/ServerDatas/accountAndpassword.json','r') as fr:
        localAccounts=json.load(fr)
        if theaccount in localAccounts.keys():
            if localAccounts[theaccount]==thepassword:
                Scene1_main_path=cmds.file( q=True, expandName=True)
                cmds.file(Scene1_main_path.replace('Sence_start.ma','Scene1_main.ma'), open=1)
                #场景读取完成之后
                Functions.InitBrickGameScene()
                cmds.deleteUI('zjhStartWindow')
            else:
                cmds.inViewMessage(amg='密码错误!',pos='midCenter',backColor=0x7B5353,fade=True,fadeInTime=0.2,fadeOutTime=0.2)
        else:
            #注册帐号信息
            cmds.inViewMessage(amg='帐号不存在,请注册帐号',pos='midCenter',backColor=0x7B5353,fade=True,fadeInTime=0.2,fadeOutTime=0.2)
import json
import Functions
from Globals import projectPath
from Globals import ZjhGlobals

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
            #检查是否记住账号和密码
            with open(projectPath+'data/ServerDatas/theRememberAccountAndPassword.json','r') as checkfr:
                theRemembers=json.load(checkfr)
            with open(projectPath+'data/ServerDatas/theRememberAccountAndPassword.json','w') as checkfw:
                if cmds.checkBox('accountCheckBox',q=1,value=1):
                    theRemembers['theAccount']=theaccount
                    theRemembers['rememberAccount']="1"
                    if cmds.checkBox('passwordCheckBox',q=1,value=1):
                        theRemembers['thePassword']=thepassword
                        theRemembers['rememberPassword']="1"
                    else:
                        theRemembers['thePassword']=""
                        theRemembers['rememberPassword']="0"
                else:
                    theRemembers['theAccount']=""
                    theRemembers['thePassword']=""
                    theRemembers['rememberAccount']="0"
                json.dump(theRemembers,checkfw)
            #设置当前账户
            ZjhGlobals.CurrentAccountName=theaccount
            #初始化游戏场景
            Functions.CreateGameOverWindow()#事先创建好GameOver窗口和GameWin窗口,并隐藏起来,等游戏结束的时候显示就行了
            Functions.CreateGameWinWindow()
            Functions.InitBrickGameScene()
            cmds.deleteUI('zjhStartWindow')
            cmds.inViewMessage(amg='请按空格键发射小球',pos='midCenter',backColor=0x006400,alpha=0.5,fade=True,fadeInTime=1,fadeOutTime=1)
        else:
            cmds.inViewMessage(amg='密码错误!',pos='midCenter',backColor=0x7B5353,fade=True,fadeInTime=0.2,fadeOutTime=0.2)
    else:
        #注册帐号信息
        cmds.inViewMessage(amg='帐号不存在,请注册帐号',pos='midCenter',backColor=0x7B5353,fade=True,fadeInTime=0.2,fadeOutTime=0.2)
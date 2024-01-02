import json
projectPath=cmds.file(q=True,expandName=True).split('scenes/')[0]#当前场景的存放路径
theaccount=cmds.textField('qtAccountTextline',q=1,text=1)
thepassword=cmds.textField('qtPasswordTextline',q=1,text=1)
if theaccount is not None and thepassword is not None:
    with open(projectPath+'data/ServerDatas/accountAndpassword.json','r') as fr:
        localAccounts=json.load(fr)
        if theaccount in localAccounts.keys():
            if localAccounts[theaccount]==thepassword:
                Scene1_main_path=cmds.file( q=True, expandName=True)
                cmds.file(Scene1_main_path.replace('Sence_start.ma','Scene1_main.ma'), open=1)
                cmds.deleteUI('zjhStartWindow')
            else:
                cmds.inViewMessage(amg='密码错误!',pos='midCenter',backColor=0x7B5353,fade=True,fadeInTime=0.2,fadeOutTime=0.2)
        else:
            #注册帐号信息
           cmds.loadUI(uiFile=projectPath+'scripts/registerui.ui')
           cmds.showWindow('zjhRegisterWindow')
else:
    cmds.inViewMessage(amg='请输入帐号和密码',pos='midCenter',backColor=0x7B5353,fade=True,fadeInTime=0.2,fadeOutTime=0.2)
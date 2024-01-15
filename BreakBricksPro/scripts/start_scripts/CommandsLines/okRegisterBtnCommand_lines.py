import json
from Globals import projectPath
theregisteaccount=cmds.textField('registerLineText1',q=1,text=1)
theregistepassword1=cmds.textField('registerLineText2',q=1,text=1)
theregistepassword2=cmds.textField('registerLineText3',q=1,text=1)
if theregisteaccount=='' or theregistepassword1=='' or theregistepassword2=='':
    cmds.inViewMessage(amg='请输入帐号和密码以及确认密码',pos='midCenter',backColor=0x7B5353,fade=True,fadeInTime=0.2,fadeOutTime=0.2)
else:
    if theregistepassword1 != theregistepassword2:
        cmds.inViewMessage(amg='两次密码不一致!请确认密码',pos='midCenter',backColor=0x7B5353,fade=True,fadeInTime=0.2,fadeOutTime=0.2)
    else:
        with open(projectPath+'data/ServerDatas/accountAndpassword.json','r') as fr:
            localAccounts=json.load(fr)
            if theregisteaccount in localAccounts.keys():
                cmds.inViewMessage(amg='帐号已存在!',pos='midCenter',backColor=0x7B5353,fade=True,fadeInTime=0.2,fadeOutTime=0.2)
            else:
                with open(projectPath+'data/ServerDatas/accountAndpassword.json','w') as fw:
                    localAccounts.update({theregisteaccount:theregistepassword1})
                    json.dump(localAccounts,fw)
                    fw.write('\n')
                    cmds.inViewMessage(amg='恭喜! 注册成功!',pos='midCenter',backColor=0x3CB371,fade=True,fadeInTime=0.2,fadeOutTime=0.2)
                    CommonFuns.CreateStartWindow()
                    cmds.deleteUI('zjhRegisterWindow')

from maya import cmds
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
    cmds.loadUI( uiFile='E:/myself/mayaProjects/mayaGames/BreakBricksPro/scripts/passwordui.ui')#从Qt.ui文件提取一个文本框对象
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
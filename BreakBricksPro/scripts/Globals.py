from maya import cmds
#全局变量
projectPath=cmds.file(q=True,expandName=True).split('scenes/')[0]#当前场景的存放路径
gameRun=False#用于控制线程的生死
#全局变量
from maya import cmds
class ZjhGlobals:
    CurrentAccountName=''#直接在类中声明一个静态变量
    
#全局变量
projectPath=cmds.file(q=True,expandName=True).split('scenes/')[0]#当前场景的存放路径
#全局变量

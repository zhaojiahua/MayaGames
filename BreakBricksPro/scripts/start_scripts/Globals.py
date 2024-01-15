from maya import cmds
class ZjhGlobals:
    #直接在类中声明一个静态变量
    CurrentAccountName=''
    sortedScores=None
    accountScoresrate=None
    currentscore=0
    currentscoreRate=0.0
    gametime=0.0#从开始游戏到此时此刻的时间间隔
    
#全局变量
projectPath=cmds.file(q=True,expandName=True).split('scenes/')[0]#当前场景的存放路径
#全局变量

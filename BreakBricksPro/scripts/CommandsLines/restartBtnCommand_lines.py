import Functions
from Globals import projectPath
cmds.file(projectPath+'scenes/Scene1_main.ma', open=1)
#场景读取完成之后
Functions.InitBrickGameScene()
cmds.deleteUI('zjhGameOverWindow')
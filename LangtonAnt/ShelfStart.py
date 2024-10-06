######################
#设置当前路径，展示UI界面#
######################
from maya import cmds
import sys
import os
scenepath=cmds.file(query=1,list=1)[0]
workRoot=scenepath.split('scenes')[0]
scriptpath=workRoot+'scripts/'
if scriptpath not in sys.path:
    sys.path.append(scriptpath)
import Globals as Gl
Gl.workRoot=workRoot
import MainTick as MT
MT.ShowStartUI()
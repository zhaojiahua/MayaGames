Gl.gamerun=False
for item in cmds.listRelatives('cubes_Grp',c=1):
    cmds.setAttr(item+'.ShadingGroup',2)
    cmds.sets(item,e=1,fe='lambert2SG')
    cmds.setAttr(item+'.visibility',0)
cmds.button('StartStopBtn',e=1,label='||Start>>',bgc=[0.2,0.2,0.4])
cmds.delete(cmds.listRelatives('ants_Grp',c=1))
nant=cmds.duplicate('baseAnt',n='ant01')[0]
cmds.parent(nant,'ants_Grp')
cmds.setAttr(nant+'.visibility',1)
Gl.ants=cmds.listRelatives('ants_Grp',c=1)
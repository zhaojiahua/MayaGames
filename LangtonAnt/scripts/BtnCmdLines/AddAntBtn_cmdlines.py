nant=cmds.duplicate('baseAnt',n='ant01')[0]
cmds.parent(nant,'ants_Grp')
cmds.setAttr(nant+'.visibility',1)
Gl.ants.append(nant)
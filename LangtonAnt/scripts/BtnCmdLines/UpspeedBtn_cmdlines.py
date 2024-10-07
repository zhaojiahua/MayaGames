if Gl.moveSpeed<100:
    Gl.moveSpeed+=1
    cmds.intSlider('speedSlider',e=1,value=Gl.moveSpeed)
    cmds.intSlider('speedSlider',e=1,bgc=Gl.SpeedSliderColorGradient.GetColor(Gl.moveSpeed/100.0))
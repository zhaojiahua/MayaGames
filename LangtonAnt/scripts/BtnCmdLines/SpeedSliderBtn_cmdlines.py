Gl.moveSpeed=cmds.intSlider('speedSlider',q=1,value=1)
cmds.intSlider('speedSlider',e=1,bgc=Gl.SpeedSliderColorGradient.GetColor(Gl.moveSpeed/100.0))
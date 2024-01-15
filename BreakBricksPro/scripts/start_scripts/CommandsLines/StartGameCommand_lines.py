CommonFuns.CreateGameOverWindow()#事先创建好GameOver窗口和GameWin窗口,并隐藏起来,等游戏结束的时候显示就行了
CommonFuns.CreateGameWinWindow()
CommonFuns.InitBrickGameScene()
cmds.deleteUI('zjhGameBoxWindow')#启动游戏删除盒子界面窗口
cmds.inViewMessage(amg='请按空格键发射小球',pos='midCenter',backColor=0x006400,alpha=0.5,fade=True,fadeInTime=1,fadeOutTime=1)

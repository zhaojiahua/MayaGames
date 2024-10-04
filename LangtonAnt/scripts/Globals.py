#全局变量
gamerun=False
workRoot=None
moveSpeed=1
class GradientColorRamp:
    gradient_L=None
    gradient_R=None
    def __init__(self,inLcolor,inRcolor):
        self.gradient_L=inLcolor
        self.gradient_R=inRcolor
    def GetColor(self,invalue):#传入百分比输出相应的渐变色
        return [(self.gradient_R[0]-self.gradient_L[0])*invalue+self.gradient_L[0],(self.gradient_R[1]-self.gradient_L[1])*invalue+self.gradient_L[1],(self.gradient_R[2]-self.gradient_L[2])*invalue+self.gradient_L[2]]
SpeedSliderColorGradient=GradientColorRamp([0.2,0.4,0.2],[0.8,0.3,0.3])

import math
class Vector3D:
    x=0
    y=0
    z=0
    def __init__(self,inv):
        self.x=inv[0]
        self.y=inv[1]
        self.z=inv[2]
    def __add__(self,inv):
        return Vector3D([self.x+inv.x,self.y+inv.y,self.z+inv.z])
    def __mul__(self,inv):
        if isinstance(inv,Vector3D):
            return self.x*inv.x+self.y*inv.y+self.z*inv.z
        else:
            return Vector3D([self.x*inv,self.y*inv,self.z*inv])
    def Cross(self,inv):
        x1=self.x
        y1=self.y
        z1=self.z
        x2=inv.x
        y2=inv.y
        z2=inv.z
        return Vector3D([(y1*z2-y2*z1),(x1*z2-x2*z1),(x1*y2-x2*y1)])
    def GetList(self):
        return [self.x,self.y,self.z]
    def RotateByAxisAngle(self,inaxis,intheta):
        selfq=Quaternion([0,self])
        q=Quaternion([math.cos(0.5*intheta),inaxis*math.sin(0.5*intheta)])
        fv=(q*selfq*q.Contrary()).v
        return Vector3D([round(fv.x),round(fv.y),round(fv.z)])#四舍五入取整之后这里只支持上下左右四个方向
antDirection=Vector3D([0,0,-1])
class DPI:
    metas=[0]*100000000
    row=0
    col=0
    def GetAntCoord(self,inantT):
        return [int(inantT[0])+5000,int(inantT[2])+5000]
dpi=DPI();

class Quaternion:
    s=0
    v=Vector3D([0,0,0])
    def __init__(self,inq):
        self.s=inq[0]
        self.v=inq[1]
    def __mul__(self,inq):
        if isinstance(inq,Quaternion):
            return Quaternion([self.s*inq.s-self.v*inq.v,inq.v*self.s+self.v*inq.s+self.v.Cross(inq.v)])
        else:
            return Quaternion([self.s*inq,self.v*inq])
    def Conjugate(self):
        return Quaternion([self.s,self.v*-1])
    def SquareLength(self):
        return self.s*self.s+self.v*self.v
    def Contrary(self):
        return self.Conjugate()*(1.0/self.SquareLength())
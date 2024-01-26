# -*- coding: utf-8 -*-
####################################################
#######################类库#########################
####################################################
#向量类(三维向量)
import math
class ZVector:
    def __init__(self,ix,iy,iz):
        self.x=ix
        self.y=iy
        self.z=iz
    def __str__(self):
        return ('---->>: '+str(self.x)+' '+str(self.y)+' '+str(self.z))
    def __add__(self,inv):  #重载+
        if type(inv)==ZVector:
            return ZVector(self.x+inv.x,self.y+inv.y,self.z+inv.z)
        return ZVector(self.x+inv,self.y+inv,self.z+inv)
    def __radd__(self,inv):  #重载+在右边
        return self.__add__(inv)
    def __iadd__(self,inv): #重载+=
        if type(inv)==ZVector:
            self.x+=inv.x
            self.y+=inv.y
            self.z+=inv.z
        else:
            self.x+=inv
            self.y+=inv
            self.z+=inv
        return self
    def __mul__(self,inv):  #重载*
        if type(inv)==ZVector:  #这里向量的乘法是单纯的数字对应相乘,更适合向量和标量的相乘
            return ZVector(self.x*inv.x,self.y*inv.y,self.z*inv.z)
        return ZVector(self.x*inv,self.y*inv,self.z*inv)
    def __rmul__(self,inv):  #重载*在右边
        return self*inv
    def __imul__(self,inv):  #重载*=
        if type(inv)==ZVector:  #这里向量的乘法是单纯的数字对应相乘,更适合向量和标量的相乘
            self.x*=inv.x
            self.y*=inv.y
            self.z*=inv.z
        else:
            self.x*=inv
            self.y*=inv
            self.z*=inv
        return self
    def __sub__(self,inv):
        return self+(-1*inv)
    def __isub__(self,inv):
        self+=(-1*inv)
        return self
    def __truediv__(self,inv):  #只支持向量和标量的之间的除法
        return self*(1.0/inv)
    def __rtruediv__(self,inv):  #只支持向量和标量的之间的除法
        return inv*ZVector(1.0/self.x, 1.0/self.y, 1.0/self.z)
    def Dot(self,inv):  #向量间点乘
        return self.x*inv.x+self.y*inv.y+self.z*inv.z
    def Cross(self,inv):  #向量叉乘
        return ZVector((self.y*inv.z-self.z*inv.y), (self.z*inv.x-self.x*inv.z), (self.x*inv.y-self.y*inv.x))
    def LengthSquare(self):   #返回向量的模长的平方
        return self.x*self.x+self.y*self.y+self.z*self.z
    def Length(self):   #返回向量的模长
        return math.sqrt(self.LengthSquare())
    def Normalize(self):   #返回该向量方向上的单位向量
        if self.Length()!=0:
            return 1.0/self.Length()*self
        return self
    def Normalized(self):   #使该向量归一化
        self*=1.0/self.Length()
        return self

#矩阵类(3X3矩阵,主要用于计算三维向量旋转)
class ZMatrix:
    def __init__(self):#初始化一个零矩阵
        self.row0=ZVector(0,0,0)
        self.row1=ZVector(0,0,0)
        self.row2=ZVector(0,0,0)

# -*- coding: utf-8 -*-
####################################################
#######################类库#########################
####################################################
#向量类(三维向量)
import math
class ZVector:
    def __init__(self,inl):
        self.x=inl[0]
        self.y=inl[1]
        self.z=inl[2]
    def __str__(self):
        return ('---->>: '+str(self.x)+' '+str(self.y)+' '+str(self.z))
    def __repr__(self):
        return ('---->>: '+str(self.x)+' '+str(self.y)+' '+str(self.z))
    def ItemList(self):
        return [self.x,self.y,self.z]
    def __add__(self,inv):  #重载+
        if type(inv)==ZVector:
            return ZVector([self.x+inv.x,self.y+inv.y,self.z+inv.z])
        return ZVector([self.x+inv,self.y+inv,self.z+inv])
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
            return ZVector([self.x*inv.x,self.y*inv.y,self.z*inv.z])
        return ZVector([self.x*inv,self.y*inv,self.z*inv])
    def __rmul__(self,inv):  #重载*在右边
        return self*inv
    def __imul__(self,inv):  #重载*=
        if type(inv)==ZVector:  #这里向量的乘法是单纯的数字对应相乘,更适合向量和标量的相乘
            self.x*=inv.x
            self.y*=inv.y
            self.z*=inv.z
        elif type(inv)==ZMatrix:
            self.x=inv.row1.Dot(self)
            self.y=inv.row2.Dot(self)
            self.z=inv.row3.Dot(self)
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
        return inv*ZVector([1.0/self.x, 1.0/self.y, 1.0/self.z])
    def Dot(self,inv):  #向量间点乘
        return self.x*inv.x+self.y*inv.y+self.z*inv.z
    def Cross(self,inv):  #向量叉乘
        return ZVector([(self.y*inv.z-self.z*inv.y), (self.z*inv.x-self.x*inv.z), (self.x*inv.y-self.y*inv.x)])
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
    def AngleToVector(self,inv1):#计算两个向量间的夹角(弧度值)
        return math.acos(inv1.Normalize().Dot(self.Normalize()))
    def CosToVector(self,inv1):#返回两个向量间夹角的cos值
        return self.Normalize().Dot(inv1.Normalize())
    def DecomposeVector(self,inv):#给定一个向量,将向量投影到此向量的方向上,同时返回此方向向量的垂直向量
        TVector=ZVector([0,0,0])
        if self.CosToVector(inv)==1:
            return [self,TVector]
        else:
            tinv=inv.Normalize()
            temp=self.Cross(tinv)
            TVector=tinv.Cross(temp).Normalize()
            return [self.CosToVector(tinv)*self.Length()*tinv,self.CosToVector(TVector)*self.Length()*TVector]

#矩阵类(3X3的矩阵,用于计算三维向量的旋转)
class ZMatrix:
    def __init__(self,inv1,inv2,inv3):#给定三个三维向量初始化一个矩阵
        self.row1=inv1
        self.row2=inv2
        self.row3=inv3
    def __repr__(self):
        return '\n'+self.row1.__repr__()+'\n'+self.row2.__repr__()+'\n'+self.row3.__repr__()
    @classmethod
    def OneMatrix(self):    #返回一个单位矩阵
        return ZMatrix(ZVector([1,0,0]),ZVector([0,1,0]),ZVector([0,0,1]))
    @classmethod
    def ZeroMatrix(self):    #返回一个零矩阵
        return ZMatrix(ZVector([0,0,0]),ZVector([0,0,0]),ZVector([0,0,0]))
    ##运算符重载
    def __add__(self,inm):  #矩阵加法只支持矩阵之间的相加
        return ZMatrix(self.row1+inm.row1,self.row2+inm.row2,self.row3+inm.row3)
    def __iadd__(self,inm):
        self.row1+=inm.row1
        self.row2+=inm.row2
        self.row3+=inm.row3
        return self
    def __mul__(self,inv):
        if type(inv)==ZVector:#矩阵与三维向量相乘(注意只能左乘)
            tx=self.row1.x*inv.x+self.row1.y*inv.y+self.row1.z*inv.z
            ty=self.row2.x*inv.x+self.row2.y*inv.y+self.row2.z*inv.z
            tz=self.row3.x*inv.x+self.row3.y*inv.y+self.row3.z*inv.z
            return ZVector([tx,ty,tz])
        elif type(inv)==ZMatrix:#矩阵与矩阵相乘
            tv1=self*ZVector([inv.row1.x,inv.row2.x,inv.row3.x])
            tv2=self*ZVector([inv.row1.y,inv.row2.y,inv.row3.y])
            tv3=self*ZVector([inv.row1.z,inv.row2.z,inv.row3.z])
            return ZMatrix(ZVector([tv1.x,tv2.x,tv3.x]),ZVector([tv1.y,tv2.y,tv3.y]),ZVector([tv1.z,tv2.z,tv3.z]))
        else:
            return ZMatrix(self.row1*inv,self.row2*inv,self.row3*inv)
    def __rmul__(self,inv):#只支持标量和矩阵的右乘
        if type(inv)==ZVector:
            raise Exception("与向量不支持右乘!")
        else:
            return self*inv
    @classmethod
    def GetMatrixByAxisAngle(cls,n,theta):#给定旋转轴和旋转角度(弧度制),返回旋转矩阵
        trow1=ZVector([math.cos(theta)+n.x*n.x*(1-math.cos(theta)),n.x*n.y*(1-math.cos(theta))-n.z*math.sin(theta),n.y*math.sin(theta)+n.x*n.z*(1-math.cos(theta))])
        trow2=ZVector([n.z*math.sin(theta)+n.x*n.y*(1-math.cos(theta)),math.cos(theta)+n.y*n.y*(1-math.cos(theta)),n.y*n.z*(1-math.cos(theta))-n.x*math.sin(theta)])
        trow3=ZVector([n.x*n.z*(1-math.cos(theta))-n.y*math.sin(theta),n.x*math.sin(theta)+n.y*n.z*(1-math.cos(theta)),math.cos(theta)+n.z*n.z*(1-math.cos(theta))])
        return ZMatrix(trow1,trow2,trow3)
    def GetEulerXYZ(self):#从旋转矩阵获取欧拉角(旋转顺序XYZ)
        roll = math.atan2(self.row3.y, self.row3.z)
        pitch = math.asin(-self.row3.x)
        yaw = math.atan2(self.row2.x, self.row1.x)
        return [roll*180/3.14159,pitch*180/3.14159,yaw*180/3.14159]
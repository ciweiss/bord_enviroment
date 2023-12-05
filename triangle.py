import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos,sqrt
class joint:
    def __init__(self, _points):
        self.points=np.append(np.identity(3),np.array([[1,1,1]]),axis=0)
        self.points[2][2]=0
        self.points[0][0]=_points[0][0]
        self.points[0][1]=_points[0][1]
        self.points[0][2]=_points[0][2]
        self.points[1][0]=_points[1][0]
        self.points[1][1]=_points[1][1]
        self.points[1][2]=_points[1][2]
        self.orientation=np.identity(4)
    def move_to_angle(self, phi, teta):
        self.orientation[0][0]=1-cos(phi)**2*sin(teta/2)**2
        self.orientation[0][1]=-sin(2*phi)*sin(teta/2)**2
        self.orientation[0][2]=sin(teta)*cos(phi)
        self.orientation[0][3]=0
        self.orientation[1][0]=-sin(2*phi)*sin(teta/2)**2
        self.orientation[1][1]=1-2*sin(phi)**2*sin(teta/2)**2
        self.orientation[1][2]=sin(teta)*sin(phi)
        self.orientation[1][3]=0
        self.orientation[2][0]=-sin(teta)*cos(phi)
        self.orientation[2][1]=-sin(teta)*sin(phi)
        self.orientation[2][2]=cos(teta)
        self.orientation[2][3]=0

r=1
points=[[r,-r/2,-r/2],[0,sqrt(3)/2*r,-sqrt(3)/2*r],[0,0,0]]
test=joint(points)
print(test.points)

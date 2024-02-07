from utility/serial.py import *
from utility/geometry.py import *
import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos,sqrt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
from time import sleep
class joint:
    def __init__(self, _points, h:float):
        self.points=np.append(np.identity(3),np.array([[1,1,1]]),axis=0)
        self.points[2][2]=0
        self.points[0][0]=_points[0][0]
        self.points[0][1]=_points[0][1]
        self.points[0][2]=_points[0][2]
        self.points[1][0]=_points[1][0]
        self.points[1][1]=_points[1][1]
        self.points[1][2]=_points[1][2]
        self.orientation=np.identity(4)
        self.orientation[2][3]=h
        self.h=h
    def move_to_angle(self, phi: float, teta: float):
        self.orientation[0][0]=1-cos(phi)**2*sin(teta/2)**2
        self.orientation[0][1]=-sin(2*phi)*sin(teta/2)**2
        self.orientation[0][2]=sin(teta)*cos(phi)
        self.orientation[0][3]=self.h*sin(teta/2)*cos(phi)
        self.orientation[1][0]=-sin(2*phi)*sin(teta/2)**2
        self.orientation[1][1]=1-2*sin(phi)**2*sin(teta/2)**2
        self.orientation[1][2]=sin(teta)*sin(phi)
        self.orientation[1][3]=self.h*sin(teta/2)*sin(phi)
        self.orientation[2][0]=-sin(teta)*cos(phi)
        self.orientation[2][1]=-sin(teta)*sin(phi)
        self.orientation[2][2]=cos(teta)
        self.orientation[2][3]=self.h*cos(teta/2)
    def calc_len(self):
        values=[0,0,0]
        temp=np.matmul(self.orientation,self.points)
        for i in range(3):
            values[i]=sqrt((temp[0][i]-self.points[0][i])**2+(temp[1][i]-self.points[1][i])**2+(temp[2][i]-self.points[2][i])**2)
        return values

def move_angle(j:joint,phi,teta, ser_mot:serial):
    j.move_to_angle(phi,teta)
    signs=[1,1,1]
      
    values=[]
    ba = bytearray()
    temp=test.calc_len()
    print(temp)
    for i in range(len(temp)):
        temp[i]-=h
        temp[i]/=r_rolle
        temp[i]*=signs[i]
    print(temp)
    for j in range(4):
        ba.extend(struct.pack("f", 0))
    for i in range(3):
        ba.extend(struct.pack("f",temp[i]))
        ba.extend(struct.pack("f", 5.0))
        for j in range(2):
            ba.extend(struct.pack("f", 0))
    for i in range(128):
        ba.extend(struct.pack("f", i))
    send_all(wrapper(ba),ser_mot)
    values=get_all(ser_mot)
    
ser_mot = serial.Serial('COM7', 115200,timeout=None) 
r=56.5
h=107
r_rolle=9
points=[[r,-r/2,-r/2],[0,sqrt(3)/2*r,-sqrt(3)/2*r],[0,0,0]]
test=joint(points,h)
move_angle(test,np.pi/2,np.pi/4,ser_mot)
'''
sleep(5)
move_angle(test,0,0,ser_mot)
sleep(5)
move_angle(test,np.pi/2*3,np.pi/3,ser_mot)
sleep(5)
move_angle(test,0,0,ser_mot)
sleep(5)
move_angle(test,0,np.pi/3,ser_mot)
sleep(5)
move_angle(test,0,0,ser_mot)
'''

ser_mot.close()

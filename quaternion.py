from math import sin, cos,sqrt
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from scipy.optimize import root
import time
from scipy.spatial.transform import Rotation as R

def HomMat(phi: float, teta: float,h: float):
    cp=cos(phi)
    ct=cos(teta)
    sp_2=sin(phi*2)
    sp=sin(phi)
    st=sin(teta)
    st_2=sin(teta/2)
    orientation=np.identity(4)
    orientation[0][0]=1-cp*cp*st_2*st_2
    orientation[0][1]=-sp_2*st_2*st_2
    orientation[0][2]=st*cp
    orientation[0][3]=h*st_2*cp
    orientation[1][0]=-sp_2*st_2*st_2
    orientation[1][1]=1-2*sp**2*st_2*st_2
    orientation[1][2]=st*sp
    orientation[1][3]=h*st_2*sp
    orientation[2][0]=-st*cp
    orientation[2][1]=-st*sp
    orientation[2][2]=ct
    orientation[2][3]=h*cos(teta/2)
    return orientation

def rotate_triangle(triangle,degree):
    rad=degree/180*np.pi
    rotation_matrix=np.matrix([[cos(rad),-sin(rad)],[sin(rad),cos(rad)]])
    return np.matmul(rotation_matrix,triangle)

def generate_triangles(r):
    triangle=np.zeros((2,3))
    triangles=np.zeros((2,3))
    triangle[0]=[r,-r/2,-r/2]
    triangle[1]=[0,sqrt(3)/2*r,-sqrt(3)/2*r]
    triangles=triangle
    for i in range(1,12):
        triangles=np.append(triangles,rotate_triangle(triangle,10*i),axis=1)
    triangles_3d=np.append(triangles,np.zeros((1,12*3)),axis=0)
    return triangles_3d

def calc_dist_matrix(mat1,mat2):
    ###calc distance for n lines stored as 2 3xn matrices or as 4xn matrices
    len=np.size(mat1[0,:])
    results=np.zeros(len)
    for i in range(len):
        for j in range(3):
            results[i]+=(mat1[j,i]-mat2[j,i])**2
        results[i]=sqrt(results[i])
    return results

class continuum_arm:
    def __init__(self,h:float,r:float,r_rolle:float,d:float):
        self.h=h
        self.r=r
        self.r_rolle=r_rolle
        self.d=d
        self.angles=np.zeros((12,2))
        self.triangles_ground=generate_triangles(r)
        self.triangles=[]
        self.triangles.append(self.triangles_ground)
        for i in range(12):
            self.triangles.append(self.triangles[0][:,3*i:])
       
    def move_to_angles(self,angles):
        quat=np.zeros((12,4))
        trans=np.zeros((12,3))
        for i in range(12):
            s=sin(angles[i][1]/2)
            r=sin(angles[i][0])*s
            p=cos(angles[i][0])*s
            n=sqrt(1-s*s)
            quat[i,:]=[n,r,p,0]
            trans[i,:]=[self.h*p,self.h*r,self.h*n]
        rot=R.from_quat(quat)
        for i in range(10,-1,-1):
            for j in range(i+1,12):
                rot[j]=rot[j]*rot[i]
        for i in range(1,12):
            trans[i]=rot[i-1].apply(trans[i])
        self.triangles=[self.triangles_ground]
        for i in range(12):
            self.triangles.append(self.triangles[0][:,3*i:])
        for i in range(12):
            self.triangles.append(rot[i].apply(self.triangles[0][:,3*i:]))
                
        print(rot.as_quat())

    def calc_len(self):
        dists=[]
        results=np.zeros(36)
        for i in range(12):
            dists.append(calc_dist_matrix(self.triangles[12-i],self.triangles[11-i]))
        for i in range(12):
            for j in range(i+1):
                for k in range(3):
                    results[3*j+k]+=dists[i][j*3+k]
        return results

    def inverse_kinematic(self,target):
        def F(angles):
            res=np.identity(4)
            for i in range(12):
                mat=HomMat(angles[i],angles[i+12],h)
                res=np.matmul(mat,res)
            res=res-target
            ret=np.zeros(24)
            for i in range(12):
                ret[i]=res[i>>2,i&3]
            return ret
        sol=np.zeros(24)
        nsol=root(F, sol, method='lm')###,options= {'maxiter':30000}
        angles=[]
        for i in range(12):
            angles.append([nsol.x[i],nsol.x[i+12]])
        return angles

r=56.5
h=107
r_rolle=9
arm=continuum_arm(h,r,r_rolle,12.0)
angles=[]
angles=np.zeros((12,2))
for i in range(12):
    angles[i,:]=[np.pi/12*i,np.pi/72*i]
arm.move_to_angles(angles)


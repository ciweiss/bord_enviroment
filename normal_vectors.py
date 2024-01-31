from math import sin, cos,sqrt
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from scipy.optimize import root
import time

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
def normalizer(y):
    x=np.arctan(y)
    x+=np.pi/2
    x/=3
    return x
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
    triangles_3d=np.append(triangles_3d,np.ones((1,12*3)),axis=0)
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
class joint:
    def __init__(self, h:float):
        self.orientation=np.identity(4)
        self.orientation[2][3]=h
        self.h=h
        self.phi=0
        self.teta=0
    def move_to_angle(self, phi: float, teta: float):
        self.phi=phi
        self.teta=teta
        self.orientation=HomMat(phi,teta,self.h)

class continuum_arm:
    def __init__(self,h:float,r:float,r_rolle:float,d:float):
        self.h=h
        self.r=r
        self.r_rolle=r_rolle
        self.d=d
        self.joints=[]
        for i in range(12):
            self.joints.append(joint(h))
        self.triangles_ground=generate_triangles(r)
        self.triangles=[]
        self.triangles.append(self.triangles_ground)
        for i in range(12):
            self.triangles.append(self.triangles[0][:,3*i:])
        for i in range(12,0,-1):
            for j in range(12,i-1,-1):
                self.triangles[j]=np.matmul(self.joints[i-1].orientation,self.triangles[j])
    def show(self):
        _x=[]
        _y=[]
        _z=[]
        _i=[]
        _j=[]
        _k=[]
        _l=[]
        for j in range(12*3):
                _x.append(self.triangles[0][0,j])
                _y.append(self.triangles[0][1,j])
                _z.append(self.triangles[0][2,j])
        for i in range(1,13):
            for j in range(12*3-(i-1)*3):
                _x.append(self.triangles[i][0,j])
                _y.append(self.triangles[i][1,j])
                _z.append(self.triangles[i][2,j])
        for i in range(90*3):
            _l.append(i/(90*3))
        for i in range(90):
            _i.append(i*3)
            _j.append(i*3+1)
            _k.append(i*3+2)
        fig = go.Figure(data=[
            go.Mesh3d(
                x=_x,
                y=_y,
                z=_z,
                
                colorscale=[[0, 'gold'],
                            [0.5, 'mediumturquoise'],
                            [1, 'magenta']],
                # Intensity of each vertex, which will be interpolated and color-coded
                intensity=_l,
                # i, j and k give the vertices of triangles
                i=_i,
                j=_j,
                k=_k,
                name='y',
                showscale=False
            )
        ])
        ###fig.show()
        return  _x, _y, _z, _i,_j,_k,_l
           
    def show_arrows(self):
        coords=np.zeros((4,1))
        coords[3,0]=1
        for i in range(12):
            coords=np.matmul(self.joints[11-i].orientation,coords)
            coords=np.append(np.zeros((4,1)),coords,axis=1)
            coords[3,0]=1
        x=coords[0,:12]
        y=coords[1,:12]
        z=coords[2,:12]
        u=coords[0,1:]
        u=u-x
        v=coords[1,1:]
        v=v-y
        w=coords[2,1:]
        w=w-z
        ax = plt.figure().add_subplot(projection='3d')
        ax.quiver(x, y, z, u, v, w, normalize=False)
 
        ax.set_xlim([-600,600])
        ax.set_ylim([-600,600])
        ax.set_zlim([0,1000])
        plt.show()
        
    def move_to_angles(self,angles):
        for i in range(12):
            self.joints[i].move_to_angle(angles[i][0],angles[i][1])
        self.triangles=[]
        self.triangles.append(self.triangles_ground)
        for i in range(12):
            self.triangles.append(self.triangles[0][:,3*i:])
        for i in range(12,0,-1):
            for j in range(12,i-1,-1):
                self.triangles[j]=np.matmul(self.joints[i-1].orientation,self.triangles[j])
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
                teta=normalizer(angles[23-i])
                mat=HomMat(angles[11-i],teta,h)
                res=np.matmul(mat,res)
            res=res-target
            ret=np.zeros(24)
            for i in range(12):
                ret[i]=res[i>>2,i&3]
            return ret
        sol=np.zeros(24)
        for i in range(12,24):
            sol[i]=-20
        nsol=root(F, sol, method='lm')
        angles=[]
        for i in range(12):
            angles.append([nsol.x[i],normalizer(nsol.x[i+12])])
        return angles
    
    def inverse_kinematic2(self,target):
        def F(angles):
            res=np.identity(4)
            for i in range(12):
                teta=normalizer(angles[23-i])
                mat=HomMat(angles[11-i],teta,h)
                res=np.matmul(mat,res)
            res=res-target
            ret=np.zeros(24)
            ret[0]=res[0][3]
            ret[1]=res[1][3]
            ret[2]=res[2][3]
            return ret
        sol=np.zeros(24)
        for i in range(12,24):
            sol[i]=-20
        nsol=root(F, sol, method='lm')
        angles=[]
        for i in range(12):
            angles.append([nsol.x[i],normalizer(nsol.x[i+12])])
        return angles
    def inverse_kinematic3(self,target,fixed_angles):
        fixed=np.identity(4)
        for i in range(6):
            fixed=np.matmul(fixed,HomMat(fixed_angles[i][0],fixed_angles[i][1],self.h))
        def F(angles):
            res=np.identity(4)
            for i in range(5,-1,-1):
                teta=normalizer(angles[i+6])
                mat=HomMat(angles[i],teta,h)
                res=np.matmul(mat,res)
            res=np.matmul(fixed,res)
            res=res-target
            ret=np.zeros(12)
            for i in range(12):
                ret[i]=res[i>>2,i&3]
            return ret
        sol=np.zeros(12)
        nsol=root(F, sol, method='lm')
        angles=[]
        for i in range(6):
            angles.append(fixed_angles[i])
        for i in range(6):
            angles.append([nsol.x[i],normalizer(nsol.x[i+6])])
        return angles
r=56.5
h=107
r_rolle=9
arm=continuum_arm(h,r,r_rolle,12.0)
angles=[]
for i in range(12):
    angles.append([np.pi/12*i,np.pi/60*i])
arm.move_to_angles(angles)
testMat=np.identity(4)
for i in range(12):
    testMat=np.matmul(arm.joints[11-i].orientation,testMat)
print(testMat)
###print(arm.triangles[12][:,0]/3+arm.triangles[12][:,1]/3+arm.triangles[12][:,2]/3)
_x,_y,_z,_i,_j,_k,_l=arm.show()
ti=time.time_ns()
angles=arm.inverse_kinematic2(testMat)
angles=arm.inverse_kinematic3(testMat,angles)
ti2=time.time_ns()

arm.move_to_angles(angles)
testMat=np.identity(4)
for i in range(12):
    testMat=np.matmul(arm.joints[11-i].orientation,testMat)
print(testMat)
###print(arm.triangles[12][:,0]/3+arm.triangles[12][:,1]/3+arm.triangles[12][:,2]/3)
_x2,_y2,_z2,_i2,_j2,_k2,_l2=arm.show()
for i in range(len(_i2)):
    _i2[i]+=len(_i2)*3
    _j2[i]+=len(_i2)*3
    _k2[i]+=len(_i2)*3
for i in range(len(_l)):
    _l2[i]=1
    _l[i]=0
_x=_x+_x2
_y=_y+_y2
_z=_z+_z2
_i=_i+_i2
_j=_j+_j2
_k=_k+_k2
_l=_l+_l2
fig = go.Figure(data=[
            go.Mesh3d(
                x=_x,
                y=_y,
                z=_z,
                
                colorscale=[[0, 'gold'],
                            [0.5, 'mediumturquoise'],
                            [1, 'magenta']],
                # Intensity of each vertex, which will be interpolated and color-coded
                intensity=_l,
                # i, j and k give the vertices of triangles
                i=_i,
                j=_j,
                k=_k,
                name='y',
                showscale=False
            )
        ])
fig.show()
print((ti2-ti)/1000000000)

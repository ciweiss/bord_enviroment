from utility.geometry import *
from math import sin, cos,sqrt
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from scipy.optimize import root
import time
import struct
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
    def __init__(self,h:float,r:float,r_rolle:float,d:float,index_list):
        self.h=h
        self.r=r
        self.r_rolle=r_rolle
        self.d=d
        self.joints=[]
        self.index_list=index_list
        for i in range(12):
            self.joints.append(joint(h))
        self.triangles_ground=generate_triangles(r,index_list)
        self.triangles=[]
        self.triangles.append(self.triangles_ground)
        temp_list=[]
        self.motor_list=[]
        for i in range(12):
            temp_list.append(index_list[i])
            temp_list.append(index_list[i]+12)
            temp_list.append(index_list[i]+24)
        for i in range(36):
            self.motor_list.append(temp_list.index(i))
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
        fig.show()
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
    def send_len(self):
        list_len=self.calc_len()
        for i in range(12):
            list_len[35-i*3]-=(i+1)*self.h
            list_len[34-i*3]-=(i+1)*self.h
            list_len[33-i*3]-=(i+1)*self.h
        values=np.zeros(36)
        for i in range(36):
            values[i]=list_len[self.motor_list[i]]/self.r_rolle
            if i % 3==2:
                values[i]*=-1
        ba=bytearray()
        for i in range(36):
            ba.extend(struct.pack("f",  values[i]))
            ba.extend(struct.pack("f",10))
            ba.extend(struct.pack("f",0))
            ba.extend(struct.pack("f",0))
        return ba


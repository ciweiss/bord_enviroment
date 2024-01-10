from math import sin, cos,sqrt
import numpy as np
import plotly.graph_objects as go
class joint:
    def __init__(self, h:float):
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
        for i in range(13):
            for j in range(12*3-i*3):
                _x.append(self.triangles[i][0,j])
                _y.append(self.triangles[i][1,j])
                _z.append(self.triangles[i][2,j])
        for i in range(78*3):
            _l.append(i/(78*3))
        for i in range(78):
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
            
r=56.5
h=107
r_rolle=9
arm=continuum_arm(h,r,r_rolle,12.0)
angles=[]
for i in range(12):
    angles.append([np.pi/12*i,np.pi/72*i])
print(arm.calc_len())
arm.move_to_angles(angles)
arm.show()


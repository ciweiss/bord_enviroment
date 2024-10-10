from math import sin, cos,sqrt
import numpy as np

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
    triangle[1]=[0,-sqrt(3)/2*r,sqrt(3)/2*r]
    triangles=triangle
    for i in range(1,12):
        triangles=np.append(triangles,rotate_triangle(triangle,-10*i),axis=1)
    triangles_3d=np.append(triangles,np.zeros((1,12*3)),axis=0)
    triangles_3d=np.append(triangles_3d,np.ones((1,12*3)),axis=0)
    return triangles_3d

def generate_triangles(r,index_list):
    triangle=np.zeros((2,3))
    triangles=np.zeros((2,3))
    triangle[0]=[r,-r/2,-r/2]
    triangle[1]=[0,sqrt(3)/2*r,-sqrt(3)/2*r]
    triangles=triangle
    for i in range(1,12):
        triangles=np.append(triangles,rotate_triangle(triangle,10*i),axis=1)
    triangles_3d=np.append(triangles,np.zeros((1,12*3)),axis=0)
    triangles_3d=np.append(triangles_3d,np.ones((1,12*3)),axis=0)
    triangles_perm=np.zeros((4,36))

    for i in range(12):
        triangles_perm[:,i*3]   = triangles_3d[:,index_list[i]*3].flatten()
        triangles_perm[:,i*3+1] = triangles_3d[:,index_list[i]*3+1].flatten()
        triangles_perm[:,i*3+2] = triangles_3d[:,index_list[i]*3+2].flatten()
    return triangles_perm

def calc_dist_matrix(mat1,mat2):
    ###calc distance for n lines stored as 2 3xn matrices or as 4xn matrices
    len=np.size(mat1[0,:])
    results=np.zeros(len)
    for i in range(len):
        for j in range(3):
            results[i]+=(mat1[j,i]-mat2[j,i])**2
        results[i]=sqrt(results[i])
    return results

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
        return valu

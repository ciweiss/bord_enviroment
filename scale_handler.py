import serial
import struct
import numpy as np
import matplotlib.pyplot as plt
import time
eichung=[1.080597996711731,1.0395885705947876,1.0741096735,1.0886378288269043,1.0733023881912231,1.0121699571609497]
def save_values(filename,values):
    file=open(filename,"wb")
    ba=bytearray()
    for value_point in values:
        ba.extend(struct.pack("f",float(value_point)))
    file.write(ba)
    file.close()
def load_values(filename):
    file=open(filename,"rb")
    ba=file.read()
    temp=struct.iter_unpack("f",ba)
    values=[]
    for i in temp:
        values.append(i[0])
    file.close()
    return values
def scale_connect(port):
    values=[]
    ser_scale = serial.Serial(port, 57600,timeout=None)
    ba=bytearray(24)
    time.sleep(5)
    ser_scale.reset_input_buffer()
    for i in range(100):
        ser_scale.readinto(ba)
        temp=struct.iter_unpack("f",ba)
        for i in temp:
            values.append(i[0])
    ser_scale.close()
    return values


def split(values, count):
    return_values=[]
    for i in range(count):
        return_values.append([])
    for i in range(len(values)):
            return_values[i%count].append((values[i]-1*eichung[i%count]))
    return return_values
def plotthis():
    values=load_values("scales.sav")
    X=np.arange(0,10,0.1)
    temp=split(values,6)
    Y1=np.array(temp[0])
    Y2=np.array(temp[1])
    Y3=np.array(temp[2])
    Y4=np.array(temp[3])
    Y5=np.array(temp[4])
    Y6=np.array(temp[5])
    plt.plot(X,Y1,label="1")
    plt.plot(X,Y2,label="2")
    plt.plot(X,Y3,label="3")
    plt.plot(X,Y4,label="4")
    plt.plot(X,Y5,label="5")
    plt.plot(X,Y6,label="6")
    plt.legend()
    plt.show()
save_values("scales.sav",scale_connect("COM14"))
plotthis()

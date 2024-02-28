import serial
import struct
def save_values(filename,values):
    file=open(filename,"wb")
    ba=bytearray()
    for value_point in values:
        ba.extend(struct.pack("f",float(value_point)))
    file.write(ba)
    file.close()

def scale_connect(port):
    values=[]
    ser_scale = serial.Serial(port, 115200,timeout=None)
    ba=bytearray(24)
    for i in range(600):
        ser_scale.read(ba)
        temp=struct.iter_unpack("f",ba)
        for i in temp:
            values.append(i)
    return values


array=[0.001,1.1,12]
save_values("scales.sv",array)
f=open("scales.sv","rb")
temp=struct.iter_unpack("f",f.read())
values=[]
for i in temp:
    values.append(i)
print(values)
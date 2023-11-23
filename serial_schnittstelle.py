import serial
import struct

ser_mot1 = serial.Serial('COM21', 115200,timeout=None) 
def wrapper(bytearray):
    package=[]
    for i in range(int(len(bytearray)/64)):
        temp=bytearray[i*64:i*64+64]
        package.append(temp)
    return package    
def send_all(package, serial_connection):
    serial_connection.reset_input_buffer
    for i in range(len(package)):
        serial_connection.write(package[i])
        print(serial_connection.read(1))
def get_all(serial_connection):
    values=[]
    for i in range(9):
        temp=serial_connection.read(64)
        temp=struct.iter_unpack("f",temp)
        for i in temp:
            values.append(float(i[0]))
    return values  
values=[]
ba = bytearray()
for j in range(4):
    ba.extend(struct.pack("f", 0))
for i in range(3):
    temp=float(input())
    ba.extend(struct.pack("f",temp))
    temp=float(input())
    ba.extend(struct.pack("f",temp))
    for j in range(2):
        ba.extend(struct.pack("f", 0))
for i in range(128):
    ba.extend(struct.pack("f", i))
send_all(wrapper(ba),ser_mot1)
values=get_all(ser_mot1)
for i in values:
    print(i)
ser_mot1.close()

import serial
import struct

ser_mot1 = serial.Serial('COM23', 115200,timeout=None) 
value = 5.14321
def wrapper(bytearray):
    package=[]
    for i in range(int(len(bytearray)/16)):
        temp=bytearray[i*16:i*16+16]
        package.append(temp)
    return package    
def send_all(package, serial_connection):
    for i in range(len(package)):
        serial_connection.write(package[i])


ba = bytearray(struct.pack("f", value))
for i in range(143):
    ba.extend(struct.pack("f", i))
send_all(wrapper(ba),ser_mot1)
print(ser_mot1.read(4))
ser_mot1.close()

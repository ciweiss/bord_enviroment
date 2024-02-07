import serial
import struct

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

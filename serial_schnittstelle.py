import serial
import struct

ser_mot1 = serial.Serial('COM4', 115200) 
data="12345.000"
value = 5.14321
print(value)
ba = bytearray(struct.pack("f", value))
print(len(ba))
print(type(ba))
print(struct.unpack('f', ba))
ser_mot1.write(ba)
ser_mot1.close()
###https://forum.arduino.cc/t/how-to-convert-byte-array-to-float-array/1030827/5
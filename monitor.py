import serial
import sys
import atexit
def end(ser:serial):
    ser.close()
atexit.register(end)
port=sys.argv[0]
ser_mot = serial.Serial(port, 115200,timeout=None)
while True: 
    print(ser_mot.read())
    

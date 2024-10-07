import serial
import sys
import atexit
def end(ser:serial):
    ser.close()

port=sys.argv[0]
ser_mot = serial.Serial(port, 115200,timeout=None)
atexit.register(end(ser_mot))
while True: 
    print(ser_mot.read())
    

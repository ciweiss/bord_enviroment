import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation 
import time
from datetime import datetime, timedelta
import threading
import logging
import tkinter as tk
from tkinter import Entry, Button
from simple_pid import PID


#serielle schnittstelle von twin m2 
ser_mot1 = serial.Serial('COM23', 115200) 

monitor_m1_array = []


# Plot  Soll und ist winkel für MOTOR1

#*********************************************************************************************
def get_current_time():
    return datetime.now()

# hier werden die variablen von m2 an terminal geprintet
def read_data_from_serial_m1():
    while True:
        try:
            line = ser_mot1.readline().decode('UTF-8').strip()
            data = line.split('\t')
            if len(data) == 3:
                angle_m1, current_m1, velocity_m1 = map(float, data)
                current_time = get_current_time()
                monitor_m1_array.append([angle_m1, current_m1, velocity_m1, current_time])
                print(f"angle_m1: {angle_m1}\tcurrent_m1: {current_m1}\tvelocity_m1: {velocity_m1}")
        except Exception as e:
             print(f"Error reading from serial port: {e}")
             
def send_data_to_serial_m1(data):
    try:
        ser_mot1.write(data.encode() + b'\n')  # Send data with a newline c0haracter
        logging.debug(f"Sent data: {data}")
    except Exception as e:
        logging.error(f"Exception while sending data: {e}")             


root = tk.Tk()
root.title("Microcontroller Communication")

entry_label_m1 = tk.Label(root, text="sende Motor 1:")
entry_label_m1.pack()

entry_m1= Entry(root)
entry_m1.pack()

#hier wird ein user input in form von 10;20;30 eingegeben wo ; für die trennung steht 
#dabei wird die erste variable hier also 10 an den motor m2 weitergegeben und als target gesetzt die zweote variable 20 wird an den motor m1 weitergegeben 

def send_button_click_m1():
    user_input = entry_m1.get()
    send_data_to_serial_m1(user_input)

send_button_m1 = Button(root, text="Send", command=send_button_click_m1)
send_button_m1.pack()

serial_thread = threading.Thread(target=read_data_from_serial_m1)
serial_thread.daemon = True  # Setzen Sie den Thread als Daemon, damit er beendet wird, wenn das Hauptprogramm beendet wird.
serial_thread.start()

             
try:
   
   root.mainloop() 

   read_data_from_serial_m1()

except KeyboardInterrupt:
    logging.info("Script terminated by user.")
finally:
    ser_mot1.close()
               
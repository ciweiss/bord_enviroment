#! /usr/bin/env python3
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 8.0
#  in conjunction with Tcl version 8.6
#    Feb 07, 2024 01:51:24 PM CET  platform: Windows NT

from ast import Interactive
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
import numpy as np
from utility.serial import *
import normal_vectors
import serial
import ui2
import struct
import random

_debug = True # False to eliminate debug printing from callback functions.

def main(*args):
    '''Main entry point for the application.'''
    global root
    root = tk.Tk()
    root.protocol( 'WM_DELETE_WINDOW' , on_closing)
    global _top1, _w1
    global positions
    global ser_mot, connected, arm, permutation,scales, coms,entries, angles
    angles=[]
    _top1 = root
    _w1 = ui2.Toplevel1(_top1)
    _w1.angle.set(45)
    _w1.com.set(10)
    ser_mot=serial.Serial(None, 115200,timeout=None) 
    scales=[]
    entries=[]
    scales.append(serial.Serial(None, 57600,timeout=None))
    scales.append(serial.Serial(None, 57600,timeout=None))
    scales.append(serial.Serial(None, 57600,timeout=None))
    entries.append(_w1.s1)
    entries.append(_w1.s2)
    entries.append(_w1.s3)
    entries.append(_w1.s4)
    entries.append(_w1.s5)
    entries.append(_w1.s6)
    entries.append(_w1.s7)
    entries.append(_w1.s8)
    entries.append(_w1.s9)
    entries.append(_w1.s10)
    entries.append(_w1.s11)
    entries.append(_w1.s12)
    entries.append(_w1.s13)
    entries.append(_w1.s14)
    entries.append(_w1.s15)
    entries.append(_w1.s16)
    entries.append(_w1.s17)
    entries.append(_w1.s18)
    entries.append(_w1.s19)
    entries.append(_w1.s20)
    entries.append(_w1.s21)
    entries.append(_w1.s22)
    entries.append(_w1.s23)
    entries.append(_w1.s24)
    entries.append(_w1.s25)
    entries.append(_w1.s26)
    entries.append(_w1.s27)
    entries.append(_w1.s28)
    entries.append(_w1.s29)
    entries.append(_w1.s30)
    entries.append(_w1.s31)
    entries.append(_w1.s32)
    entries.append(_w1.s33)
    entries.append(_w1.s34)
    entries.append(_w1.s35)
    entries.append(_w1.s36)
    entries.append(_w1.Entry4)
    entries.append(_w1.Entry5)
    entries.append(_w1.Entry6)
    entries.append(_w1.Entry7)
    entries.append(_w1.Entry8)
    entries.append(_w1.Entry9)
    entries.append(_w1.Entry10)
    entries.append(_w1.Entry11)
    entries.append(_w1.Entry12)
    entries.append(_w1.Entry13)
    entries.append(_w1.Entry14)
    entries.append(_w1.Entry15)
    entries.append(_w1.Entry16)
    entries.append(_w1.Entry17)
    entries.append(_w1.Entry18)
    entries.append(_w1.Entry19)
    entries.append(_w1.Entry20)
    entries.append(_w1.Entry21)
    entries.append(_w1.Entry22)
    entries.append(_w1.Entry23)
    entries.append(_w1.Entry24)
    entries.append(_w1.Entry25)
    entries.append(_w1.Entry26)
    entries.append(_w1.Entry27)
    entries.append(_w1.Entry28)
    entries.append(_w1.Entry29)
    entries.append(_w1.Entry30)
    entries.append(_w1.Entry31)
    entries.append(_w1.Entry32)
    entries.append(_w1.Entry33)
    entries.append(_w1.Entry34)
    entries.append(_w1.Entry35)
    entries.append(_w1.Entry36)
    entries.append(_w1.Entry37)
    entries.append(_w1.Entry38)
    entries.append(_w1.Entry39)
    angles.append([_w1.phi1,_w1.teta1])
    angles.append([_w1.phi2,_w1.teta2])
    angles.append([_w1.phi3,_w1.teta3])
    angles.append([_w1.phi4,_w1.teta4])
    angles.append([_w1.phi5,_w1.teta5])
    angles.append([_w1.phi6,_w1.teta6])
    angles.append([_w1.phi7,_w1.teta7])
    angles.append([_w1.phi8,_w1.teta8])
    angles.append([_w1.phi9,_w1.teta9])
    angles.append([_w1.phi10,_w1.teta10])
    angles.append([_w1.phi11,_w1.teta11])
    angles.append([_w1.phi12,_w1.teta12])
    connected=False
    positions =np.zeros(36)
    for i in range(12):
        angles[i][0].set(0)
        angles[i][1].set(0)
    coms=[]
    coms.append(_w1.com_scale1)
    coms.append(_w1.com_scale2)
    coms.append(_w1.com_scale3)
    coms[0].set(5)
    coms[1].set(16)
    coms[2].set(15)
    r=56.5
    h=107
    r_rolle=9
    arm=normal_vectors.continuum_arm(h,r,r_rolle,12.0,[0,9,6,3,8,5,2,11,10,7,4,1],[11,0,6,10,3,5,9,2,4,8,1,7])
    root.mainloop()
    
def on_closing():
    if connected:
        ser_mot.close()
    root.destroy()

def connect(*args):
    comport=int(_w1.com.get())
    connection="COM"+str(comport)
    ser_mot.port=connection
    ser_mot.open()
    connected=True
    print(connection, "connected")
def evaluate_scales():
    stop=False
    for i in range(3):
        values=[]
        ba=bytearray(48)
        ba2=bytearray(1)
        scales[i].reset_input_buffer()
        scales[i].write(ba2)
        scales[i].readinto(ba)
        temp=struct.iter_unpack("f",ba)
        for k in temp:
            values.append(k[0]/1000)
        for j in range(12):
            entries[i*12+j].set(values[j])
            if values[j]>1000 :
                stop=True
                entries[i*12+j+36].configure(bg="red")
    ###if not stop:
    root.after(100, evaluate_scales)  
def connect_scales(*args):
    for i in range(3):
        comport=int(coms[i].get())
        connection="COM"+str(comport)
        scales[i].port=connection
        scales[i].open()
        print(connection, "connected")
    root.after(20000, evaluate_scales) 
    
def send_proto():
    ba=bytearray()
    for i in range(36):
        ba.extend(struct.pack("f",  arm.positions_reset[i]))
        arm.positions[i]=arm.positions_reset[i]
        ba.extend(struct.pack("f",5))
        ba.extend(struct.pack("f",0))
        ba.extend(struct.pack("f",0))
    send_all(wrapper(ba),ser_mot)
    get_all(ser_mot)
    
def moven(*args):
    id=int(args[0])
    deg=int(_w1.angle.get())
    arm.positions_reset[id-1]-=deg*np.pi/180.0
    send_proto()

def movep(*args):
    id=int(args[0])
    deg=int(_w1.angle.get())
    arm.positions_reset[id-1]+=deg*np.pi/180.0
    send_proto()
    
def send_angle():
    listing=[]
    factor=np.pi/180
    for i in range(12):
        listing.append([int(angles[i][0].get()),int(angles[i][1].get())])
        
    flag=True
    for entry in listing:
        if entry[1]>40 or entry[1]<0:
            flag=False
        entry[0]*=factor
        entry[1]*=factor
    if flag:
        arm.move_to_angles(listing)
        send_all(wrapper(arm.send_len()),ser_mot)
        get_all(ser_mot)
        arm.show_arrows()     

if __name__ == '__main__':
    ui2.start_up()





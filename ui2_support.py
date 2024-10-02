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
    # Creates a toplevel widget.
    global _top1, _w1
    global positions
    global ser_mot, connected, arm, permutation, was_reseted,scales, coms,entries
    _top1 = root
    _w1 = ui2.Toplevel1(_top1)
    _w1.angle.set(45)
    _w1.com.set(20)
    ser_mot=serial.Serial(None, 115200,timeout=None) 
    scales=[]
    entries=[]
    scales.append(serial.Serial(None, 115200,timeout=None))
    scales.append(serial.Serial(None, 115200,timeout=None))
    scales.append(serial.Serial(None, 115200,timeout=None))
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
    connected=False
    was_reseted=True
    positions =np.zeros(36)

    coms=[]
    coms.append(_w1.com_scale1)
    coms.append(_w1.com_scale2)
    coms.append(_w1.com_scale3)
    coms[0].set(1)
    coms[1].set(2)
    coms[2].set(3)
    r=56.5
    h=107
    r_rolle=9
    arm=normal_vectors.continuum_arm(h,r,r_rolle,12.0)
    permutation=[6,8,7,0,2,1,4,3,5]
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
    print("scales evaluated")
    stop=False
    for i in range(36):
        value=random.random()
        entries[i].set(value)
        if value>0.98 :
            stop=True
            entries[i+36].configure(bg="red")
    if not stop:
        root.after(2000, evaluate_scales)  
def connect_scales(*args):
    for i in range(3):
        comport=int(coms[i].get())
        connection="COM"+str(comport)
        ###scales[i].port=connection
        ###scales[i].open()
        print(connection, "connected")
    root.after(2000, evaluate_scales) 
    
def send_proto():
    ba=bytearray()
    for i in range(36):
        ba.extend(struct.pack("f",  positions[i]*np.pi/180.0))
        ba.extend(struct.pack("f",10))
        ba.extend(struct.pack("f",0))
        ba.extend(struct.pack("f",0))
    send_all(wrapper(ba),ser_mot)
    get_all(ser_mot)
    
def moven(*args):
    id=int(args[0])
    deg=int(_w1.angle.get())
    positions[id-1]-=deg
    send_proto()

def movep(*args):
    id=int(args[0])
    deg=int(_w1.angle.get())
    positions[id-1]+=deg
    send_proto()


def reset():
    for i in range(9):
        positions[i]=0
    send_proto()
    global was_reseted
    was_reseted=True

if __name__ == '__main__':
    ui2.start_up()





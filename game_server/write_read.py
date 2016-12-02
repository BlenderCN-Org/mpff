#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## write_read.py

import threading
from time import time, sleep

string = ""

def read():
    global string
    while 1:
        print(string[-8:])

def read_thread():
    thread_r = threading.Thread(target=read)
    thread_r.start()

def write1():
    global string
    while 1:
        print(string[-64:])
        string += "11"
        if len(string) > 1000000:
            string = "01"

def write1_thread():
    thread_w = threading.Thread(target=write1)
    thread_w.start()

def write2():
    global string
    while 1:
        string += "22"
        if len(string) > 10000:
            string = "01"

def write2_thread():
    thread_w = threading.Thread(target=write2)
    thread_w.start()

write1_thread()
write2_thread()

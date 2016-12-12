#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## run_multiple_clients.py

import subprocess
from time import sleep

players = 9

for i in range(players):
    one_sp = subprocess.Popen(['xterm', '-e', 'blenderplayer MPFF.blend'], shell=False)
    print(i)
    sleep(2)

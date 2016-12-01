#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## run_multiple_clients.py

import os, sys
import subprocess
from time import sleep

players = 5

sp_list = []

for i in range(players):
    one_sp = subprocess.Popen(['xterm', '-e', 'python3 mpff_player_simul.py'], shell=False)
    print(one_sp.pid)
    sp_list.append(one_sp)

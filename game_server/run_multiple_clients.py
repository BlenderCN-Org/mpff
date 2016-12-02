#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## run_multiple_clients.py

import os, sys
import subprocess
from time import sleep

players = 120

for i in range(players):
    one_sp = subprocess.Popen(['xterm', '-e', 'python3 simul_clt_tcp_re.py'], shell=False)
    print(i)
    sleep(0.2)

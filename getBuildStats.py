#!/usr/bin/python

import sys
import subprocess
import os
import re

task = ""
if len(sys.argv) > 1:
 task = sys.argv[1]

#if len(task) > 0:
 #task = "*/" + task

sumed = 0.0

for root, dirs, files in os.walk("."):
    for name in files:
        if task == name:
            fp = open(os.path.join(root, name), "r")
            line = fp.readline()
            while len(line) > 0: 
                if "Elapsed" in line:
                    m = re.match('.* ([\d.]*) .*', line)
                    if m:
                        number = float(m.group(1))
                        print("%.2f + %.2f (%s)" % (sumed, number, os.path.join(root,name)))
                        sumed = sumed + number
                line = fp.readline()


print('%.2f' % sumed)

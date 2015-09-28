#!/usr/bin/python

import os
import subprocess

subprocess.call("tmux split-window /development/yocto-dizzy/build/tmp/work/imx6q_dmo_edm_qmx6-poky-linux-gnueabi/dmo-image-minimal/1.0-r0/temp/run.do_terminal.21354", shell=True)

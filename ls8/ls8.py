#!/usr/bin/env python3

"""Main."""
from cpu import *

cpu = CPU()
cpu.load('call.ls8')
cpu.run()

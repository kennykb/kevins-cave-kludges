#!/usr/bin/env python
'''
screencap.py --

    Quick&dirty script to capture the oscilloscope screen as a PNG image

Usage:
    screencap.py <filename.png>

Arguments:
    <filename.png> Path name of the PNG file where the image will be stored.

Notes:
    The PNG file is misformatted, and not all tools can read it.
    I usually recover it, if necessary, by opening it in GIMP and
    re-exporting it, which produces a correctly formatted PNG.
'''

from ds1054z import DS1054Z
from sys import argv

# IP address of the Rigol 1054Z oscilloscope
scope_ip = '192.168.2.101'

# Check arguments
if len(argv) != 2:
    print(f'usage: {argv[0]} filename.png')
    exit(1)

# Open the scope and copy the screen to a PNG file.
scope = DS1054Z(scope_ip)
with open(argv[1], "wb") as f:
    f.write(scope.display_data)




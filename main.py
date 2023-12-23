'''
Created on 2023-12-23

@author: Billy
'''

import sys
from time import sleep
import RF905_Py

try:
    sys.path.insert(0, '/home/pi/RF905-Py')

    rfn905 = RF905_Py.RF905(24, 7, 15, 13, 11, 12, 8)   # set Raspberry Pi pin
    rfn905.writeconfig(0xCC, 0xCC, 0xCC, 0xCC)         # set sender RF905 address

    def callback(received_string):
        print(received_string)

    rfn905.listen(callback)

except Exception as e:
    print(f"An error occurred: {e}")

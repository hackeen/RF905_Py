'''
Created on 2013-6-20

@author: Administrator
'''

import sys
sys.path.insert(0, '/home/pi/RF905-Py')
import RF905_Py

rfn905 = RF905_Py.RF905(24,7,15,13,11,12,8)   #set  raspberryPi pin
rfn905.writeconfig(0xCC,0xCC,0xCC,0xCC)       #set  sender RF905 address
#rfn905.sendstr("hello",0xCC,0xCC,0xCC,0xCC,) #set  Receive Rf905 address

def callback(str):
    print(str)
    
rfn905.listen(callback)
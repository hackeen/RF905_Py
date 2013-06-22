'''
Created on 2013-6-20

@author: hackeen
'''
import spi

from time import sleep
import RPi.GPIO as GPIO

class RF905:
    CSN = 24
    DR  = 7
    AM  = 15
    CD  = 13
    PWR = 11
    TRX_CE = 12
    TXEN = 8

    def __init__(self,csn,dr,am,cd,pwr,trx_ce,txen):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        CSN = csn
        DR  = dr
        AM  = am
        CD  = cd
        PWR = pwr
        TRX_CE = trx_ce
        TXEN = txen
        GPIO.setup(CSN,GPIO.OUT)
        GPIO.output(CSN,GPIO.HIGH)
        GPIO.setup(DR,GPIO.IN)
        GPIO.setup(AM,GPIO.IN)
        GPIO.setup(CD,GPIO.IN)
        GPIO.setup(PWR,GPIO.OUT)
        GPIO.output(PWR,GPIO.HIGH)
        GPIO.setup(TRX_CE,GPIO.OUT)
        GPIO.output(TRX_CE,GPIO.LOW)
        GPIO.setup(TXEN,GPIO.OUT)
        GPIO.output(TXEN,GPIO.LOW)
        
    def openSPI(self):
        spi.openSPI(speed=106000)
        
    def writeconfig(self,address1,address2,address3,address4):
        self.openSPI()
        GPIO.output(self.CSN,GPIO.LOW)
        spi.transfer((0x00,)) 
        spi.transfer((0x4C,)) 
        spi.transfer((0x0C,)) 
        spi.transfer((0x44,))
        spi.transfer((0x20,))
        spi.transfer((0x20,))
        spi.transfer((address1,))
        spi.transfer((address2,))
        spi.transfer((address3,))
        spi.transfer((address4,))
        spi.transfer((0x58,))
        GPIO.output(self.CSN,GPIO.HIGH)
        spi.closeSPI()
        
    def sendstr(self,content,address1,address2,address3,address4): 
        self.openSPI()       
        #SetTx
        GPIO.output(self.TRX_CE,GPIO.LOW)
        GPIO.output(self.TXEN,GPIO.HIGH)
        
        sleep(0.01)
        GPIO.output(self.CSN,GPIO.LOW)
        spi.transfer((0x20,))  
        for i in range(32):
            a = 32
            if i < len(content):
                a = ord(content[i])           
            spi.transfer((a,))    
        GPIO.output(self.CSN,GPIO.HIGH)
        sleep(0.01)
        GPIO.output(self.CSN,GPIO.LOW)
        spi.transfer((0x22,))
        spi.transfer((address1,))
        spi.transfer((address2,))
        spi.transfer((address3,))
        spi.transfer((address4,))
        GPIO.output(self.CSN,GPIO.HIGH)
     
        GPIO.output(self.TRX_CE,GPIO.HIGH)
        sleep(0.01)
        GPIO.output(self.TRX_CE,GPIO.LOW)
        spi.closeSPI()
        
    def listen(self,callback):
        self.openSPI()       
        #SetRx
        GPIO.output(self.TXEN,GPIO.LOW)
        GPIO.output(self.TRX_CE,GPIO.HIGH)   
             
        while 1==1:    
            while GPIO.input(self.DR) == GPIO.LOW:
                a=10
        
            GPIO.output(self.TRX_CE,GPIO.LOW)
            GPIO.output(self.CSN,GPIO.LOW)
            spi.transfer((0x24,))
            data = ""
            for x in range(32):
                data = data+chr(spi.transfer((0x00,))[0])              
            #print("2:"+data)
            callback(data)    
            GPIO.output(self.CSN,GPIO.HIGH)
            GPIO.output(self.TRX_CE,GPIO.HIGH)
        
            sleep(0.01)
            
        
        spi.closeSPI()

        
'''
Created on 2023-12-23

@author: billy
'''
import spi
from time import sleep
import RPi.GPIO as GPIO

class RF905:
    def __init__(self, csn, dr, am, cd, pwr, trx_ce, txen):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.CSN = csn
        self.DR  = dr
        self.AM  = am
        self.CD  = cd
        self.PWR = pwr
        self.TRX_CE = trx_ce
        self.TXEN = txen
        GPIO.setup(self.CSN, GPIO.OUT)
        GPIO.output(self.CSN, GPIO.HIGH)
        GPIO.setup(self.DR, GPIO.IN)
        GPIO.setup(self.AM, GPIO.IN)
        GPIO.setup(self.CD, GPIO.IN)
        GPIO.setup(self.PWR, GPIO.OUT)
        GPIO.output(self.PWR, GPIO.HIGH)
        GPIO.setup(self.TRX_CE, GPIO.OUT)
        GPIO.output(self.TRX_CE, GPIO.LOW)
        GPIO.setup(self.TXEN, GPIO.OUT)
        GPIO.output(self.TXEN, GPIO.LOW)

    def openSPI(self):
        spi.openSPI(speed=106000)

    def writeconfig(self, address1, address2, address3, address4):
        self.openSPI()
        GPIO.output(self.CSN, GPIO.LOW)
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
        GPIO.output(self.CSN, GPIO.HIGH)
        spi.closeSPI()

    def sendstr(self, content, address1, address2, address3, address4):
        self.openSPI()
        # SetTx
        GPIO.output(self.TRX_CE, GPIO.LOW)
        GPIO.output(self.TXEN, GPIO.HIGH)

        sleep(0.01)
        GPIO.output(self.CSN, GPIO.LOW)
        spi.transfer((0x20,))
        for i in range(32):
            a = 32
            if i < len(content):
                a = ord(content[i])
            spi.transfer((a,))
        GPIO.output(self.CSN, GPIO.HIGH)
        sleep(0.01)
        GPIO.output(self.CSN, GPIO.LOW)
        spi.transfer((0x22,))
        spi.transfer((address1,))
        spi.transfer((address2,))
        spi.transfer((address3,))
        spi.transfer((address4,))
        GPIO.output(self.CSN, GPIO.HIGH)

        GPIO.output(self.TRX_CE, GPIO.HIGH)
        sleep(0.01)
        GPIO.output(self.TRX_CE, GPIO.LOW)
        spi.closeSPI()

    def listen(self, callback):
        self.openSPI()
        # SetRx
        GPIO.output(self.TXEN, GPIO.LOW)
        GPIO.output(self.TRX_CE, GPIO.HIGH)

        while True:
            while GPIO.input(self.DR) == GPIO.LOW:
                pass

            GPIO.output(self.TRX_CE, GPIO.LOW)
            GPIO.output(self.CSN, GPIO.LOW)
            spi.transfer((0x24,))
            data = ""
            for _ in range(32):
                data += chr(spi.transfer((0x00,))[0])
            # print("2:" + data)
            callback(data)
            GPIO.output(self.CSN, GPIO.HIGH)
            GPIO.output(self.TRX_CE, GPIO.HIGH)

            sleep(0.01)

        spi.closeSPI()

        

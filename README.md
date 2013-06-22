RF905-Py: RF905 for Raspberry Pi

Powered by SPI-Py

step:
1 install GPIO for python

   sudo apt-get install python-setuptools
	 sudo easy_install -U distributesudo 
	 apt-get install python-dev
	 sudo easy_install RPi.GPIO
	 
	 
2 try to get SPI working on the RaspberryPi the easy way

   sudo modprobe spi_bcm2708
   
3 install SPI-Py
   python setup.py build
   python setup.py install
   
4 call RF905-Py in main.py




lqiao@hackeen.com

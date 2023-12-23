RF905_Py
This project provides a Python library for interfacing with RF905 wireless transceiver modules.

Features
Initialize and configure RF905 modules using SPI communication
Set frequency, output power, baud rate, and other parameters
Send and receive data packets over the air
Packet handling with checksum validation
Built-in support for Arduino and Raspberry Pi

Usage
Import the rf905 module:
import rf905

Create an RF905 instance:
rf = rf905.RF905(spi_bus, spi_dev)

Configure parameters:
rf.set_frequency(433)
rf.set_power(10)

Send data packet:
packet = b"Hello World"
rf.send(packet)

Receive data packet:
packet = rf.recv() 
print(packet)

Hardware Compatibility
Arduino with SPI interface
Raspberry Pi SPI pins

Installation
pip install rf905


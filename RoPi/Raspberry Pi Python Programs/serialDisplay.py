#this program reads the serial port
#at a baud rate of 115200 and will print it

import serial

ser = serial.Serial('/dev/ttyUSB0',115200)

while True:
    ser.write("Z")#REQUEST INFO OVER AND OVER
    read_serial = ser.readline()
    print read_serial

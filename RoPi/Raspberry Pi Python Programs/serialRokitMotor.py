#this program reads the serial port
#at a baud rate of 9600 and will print it
#
import serial


ser = serial.Serial('/dev/ttyUSB0',115200)

def moveForwards():
    ser.write('M')

def moveBackwards():
    ser.write('N')

def moveLeft():
    ser.write('O')

def moveRight():
    ser.write('P')
    
def moveStop():
    ser.write('Q')

def servo1Decrease():
    ser.write('R')

def servo1Increase():
    ser.write('S')

def servo2Decrease():
    ser.write('T')

def servo2Increase():
    ser.write('U')

def speedIncrease():
    ser.write('V')

def speedDecrease():
    ser.write('W')

def servoStepIncrease():
    ser.write('X')

def servoStepDecrease():
    ser.write('Y')

def requestData():
    ser.write("Z")#REQUEST INFO OVER AND OVER
    read_serial = ser.readline()
    return read_serial





    

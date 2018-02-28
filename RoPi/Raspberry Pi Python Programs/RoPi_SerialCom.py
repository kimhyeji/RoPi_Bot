#this program reads the serial port
#at a baud rate of 115200 and will print it
#
import serial

ser = serial.Serial('/dev/ttyUSB0',115200)

def requestBottomIRSensors():
    ser.write("L")
    read_serial = ser.readline()
    a,b,c,d,e,f,g,h = read_serial.split(" ")
    return int(a),int(b),int(c),int(d),int(e),int(f),int(g)

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
    a,b,c,d,e,f,g,h = read_serial.split(" ")
    return int(a),int(b),int(c),int(d),int(e),int(f),int(g)    

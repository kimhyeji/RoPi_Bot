#this program reads the serial port
#at a baud rate of 115200 and will print it
#
import serial

ser = serial.Serial('/dev/ttyUSB0',115200)

def requestBottomIRSensors():
    ser.write("L")
    read_serial = ser.readline()
    d11,d12,d13,d14,d16,d17,d18 = read_serial.split(" ")
    return int(d11),int(d12),int(d13),int(d14),int(d16),int(d17),int(d18)

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

#returns a tuple with the data as integers
def requestData():
    ser.write("Z")#REQUEST INFO
    read_serial = ser.readline()
    #read the Serial line the rokit should be sending a message

    #chop up that message
    servo1Angle,servo2Angle,servoStep,speed,a19,a20,a21 = read_serial.split(" ")
    #now return the data as integers
    return int(servo1Angle),int(servo2Angle),int(servoStep),int(speed),int(a19),int(a20),int(a21)    

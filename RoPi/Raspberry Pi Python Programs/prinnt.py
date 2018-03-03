import RoPi_SerialCom as ropi
import time
#this program shows how to request the data from the rokit board over serial
#and how to save it and use it

while(1):
    #information on the current servo angles, servo step size, and the motor speed
    #as well as the top IR sensors
    servo1Angle,servo2Angle,servoStep,speed,a19,a20,a21 = ropi.requestData()
    print(servo1Angle,servo2Angle,servoStep,speed,a19,a20,a21)

    #all of the bottom digital IR sensors
    d11,d12,d13,d14,d16,d17,d18 = ropi.requestBottomIRSensors()
    print(d11,d12,d13,d14,d16,d17,d18)

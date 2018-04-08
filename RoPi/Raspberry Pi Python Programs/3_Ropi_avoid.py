import RoPi_SerialCom as ropi
import time

startTime = time.time()

#this program will run the robot for 6 seconds
while((time.time()-startTime) < 20):

    servo1Angle,servo2Angle,servoStep,speed,a19,a20,a21 = ropi.requestData()
    #print(servo1Angle,servo2Angle,servoStep,speed,a19,a20,a21)
    d11,d12,d13,d14,d16,d17,d18 = ropi.requestBottomIRSensors()
    #print(d11,d12,d13,d14,d16,d17,d18)

    if a19 < 100:
        ropi.moveRight()
        print("right")
    elif a21 < 100:
        ropi.moveLeft()
        print("left")
    elif a20 < 100:
        print("Backwards")
        ropi.moveBackwards()
        time.sleep(1)
        ropi.moveLeft()

    else:
        print("Forwards")
        ropi.moveForwards()

#make sure to stop the robot at the very end        
ropi.moveStop()

import RoPi_SerialCom as ropi
import time
startTime = time.time()

#this robot will try to follow an object in front of it
#this program will run the robot for 15 seconds

while((time.time()-startTime) < 15):

    servo1Angle,servo2Angle,servoStep,speed,a19,a20,a21 = ropi.requestData()
    #d11,d12,d13,d14,d16,d17,d18 = ropi.requestBottomIRSensors()
    

    if a19 < 200:
        ropi.moveLeft()
        time.sleep(0.2)
        print("left")
    elif a21 < 200:
        ropi.moveRight()
        time.sleep(0.2)
        print("right")
    elif a20 < 200:
        print("Forwards")
        ropi.moveForwards()
        time.sleep(0.2)
    else:
        print("Stop")
        ropi.moveStop()

#make sure to stop the robot at the very end        
ropi.moveStop()

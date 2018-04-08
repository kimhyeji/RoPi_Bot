#This program combines basic driving commands with requesting sensor data
import RoPi_SerialCom as ropi
import time

state = 0
exit = 0
currentTime = time.time()

while exit == 0:
	servo1Angle,servo2Angle,servoStep,speed,a19,a20,a21 = ropi.requestData()
	print(servo1Angle,servo2Angle,servoStep,speed,a19,a20,a21)    
	
	if state == 0:
		ropi.moveForwards()
	elif state == 1:
		ropi.moveRight()
	elif state == 2:
		ropi.moveForwards()
	else:
		ropi.moveStop()
		exit = 1
	
	if time.time() - currentTime > 1:
		currentTime = time.time()
		state += 1

ropi.moveStop()

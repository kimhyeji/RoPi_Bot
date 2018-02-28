#robocar
#only runs code to track color


import os
#this lets you look for a library that the code cant find by itself
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

# import the necessary packages
#this is all for the pi camera to work
from picamera.array import PiRGBArray
from picamera import PiCamera
# time library for delays
from time import sleep 
import time
#this is open CV library
import cv2
from collections import deque
import numpy as np #math libraries
import argparse #to find and pass files
import imutils #resizing the image frame

#this is the library I made for RokitCommands over serial
import serialRokitMotor

#for importing a video file
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
        help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
        help="max buffer size")
args = vars(ap.parse_args())


showFrames = 1
lastSeenX = 0
lastSeenY = 0

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#we are tracking the color orange
greenLower =(27, 94, 79)
greenUpper =(47, 255, 255)

#create speed variable to keep track
speed = 100

# if we want to change threshholds 
#we have to change these numbers
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 

pts = deque(maxlen=args["buffer"])
 
# The tutorial to set up the PI camera comes from here
# http://www.pyimagesearch.com/2016/08/29/common-errors-using-the-raspberry-pi-camera-module/ 
# initialize the camera and grab a reference to the raw camera capture
#this is all to set up the pi camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 90
rawCapture = PiRGBArray(camera, size=(640, 480))

sleeptime=0.1
delay_period = 0.01

# allow the camera to warmup
time.sleep(0.1)


def speedUp():
	serialRokitMotor.speedIncrease()
	global speed
	if speed < 100:
		speed = speed + 10

def speedDown():
        serialRokitMotor.speedDecrease()
	global speed
        if speed > 0:
	        speed = speed - 10
                    

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	#this is for measuring time
	e1 = cv2.getTickCount()


	# grab the raw NumPy array representing the image - this array
	# will be 3D, representing the width, height, and # of channels
	image = frame.array

	#convert the image into a numpy array
	img_np = np.array(image)
	#then rename it frame
	frame = img_np

	#flips the frame since the camera is upside down
	#frame = cv2.flip(frame,0)
	
	#turn into HSV color space
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)#find within threshold range
	#mask = cv2.erode(mask, None, iterations=1)#destroy small specs noise
	#mask = cv2.dilate(mask, None, iterations=1)#dilate green blobs
	
	#this "res" frame pieces together 2 the mask frame and the original frame
	#this creates a frame that turns everything not within the threshold black
	if showFrames > 0:
		res = cv2.bitwise_and(frame,frame, mask= mask)

	# find contours in the mask
	#cnts is countours
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
#	cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, 
#		cv2.CHAIN_APPROX_NONE)
	#create variable for center
	center = None
	
	
#Only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)

		if int(M["m00"]) > 0:
			#center = (x,y) coordinates on 640,420 pixels
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			x_coordinate = int(M["m10"] / M["m00"])
			y_coordinate = int(M["m01"] / M["m00"])		

		
		lastSeenX = x_coordinate
		lastSeenY = y_coordinate

		print " Center ", center," Radius ", radius 

		if x_coordinate > 360 and radius > 10:				
			#serialRokitMotor.moveLeft()
			print "servo 1 increase"

			serialRokitMotor.servo1Increase()
			
		elif x_coordinate < 280 and radius > 10:
			print "servo 1 decrease"

                        #serialRokitMotor.moveRight()
			serialRokitMotor.servo1Decrease()

		elif x_coordinate < 360 and x_coordinate >280 and radius > 10:
			serialRokitMotor.servo2Increase()

		else:
			serialRokitMotor.moveStop()
			#serialRokitMotor.servo2Increase()

		if y_coordinate > 290 and radius > 10:#(640, 480)
			print "servo 2 decrease"
                        #serialRokitMotor.moveLeft()
		#	serialRokitMotor.servo2Decrease()

		elif y_coordinate < 190 and radius > 10:
                        #serialRokitMotor.moveRight()
			print "servo 2 increase"

		#	serialRokitMotor.servo2Increase()

		#elif x_coordinate < 350 and x_coordinate > 290 and radius > 10:
			#serialRokitMotor.moveForwards()			
		else:	
                        serialRokitMotor.moveStop()


		# only proceed if the radius meets a minimum size
		if radius > 10 and  showFrames:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(res, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			pts.appendleft(center)
	else: 
		print "Nothing detected" ,"last seen X:", lastSeenX, "Y", lastSeenY
		if lastSeenX > 320:
		#if the object was seen then move left and right servo
			serialRokitMotor.servo1Increase()
		else: 
			serialRokitMotor.servo1Decrease()

		if lastSeenY >240:
			serialRokitMotor.servo2Decrease()			 		  
		else:
			serialRokitMotor.servo2Increase()

	#show the frame that contains the circled area of color located
#	cv2.imshow("frame", frame)	
	if showFrames > 0:#if the user clicked the "s" key, this becomes 1
		cv2.imshow("res", res)
	

	e2 = cv2.getTickCount()
	time = (e2 - e1)/cv2.getTickFrequency()
	print "milliSeconds" , time*1000
	#the key that is clicked save it as variable key
	key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
        if key == ord("Q"):
                break
	if key == ord("k"):#click k to slow down
		speedDown()
	if key == ord("l"):#click l to speed up
		speedUp() 

        if key == ord("s"):#click l to speed up
                showFrames = 1


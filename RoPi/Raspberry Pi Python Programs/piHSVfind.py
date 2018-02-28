#modify
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

def nothing(x):
    pass

#this is the library I made for RokitCommands over serial
#import serialRokitMotor

h,s,v,r = 100,100,100,100

#for importing a video file
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
        help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
        help="max buffer size")
args = vars(ap.parse_args())


showFrames = 0
lastSeenX = 0
lastSeenY = 0


# Creating a window for later use
cv2.namedWindow('Control Panel')

# Creating track bar
#cv.CreateTrackbar(trackbarName, windowName, value, count, onChange)  None
cv2.createTrackbar('hue', 'Control Panel',11,180,nothing)
cv2.createTrackbar('sat', 'Control Panel',180,255,nothing)
cv2.createTrackbar('val', 'Control Panel',240,255,nothing)
cv2.createTrackbar('range', 'Control Panel',69,127,nothing)
#cv2.createTrackbar('ero', 'Control Panel',8,100,nothing)
#cv2.createTrackbar('dil', 'Control Panel',12,100,nothing)

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#we are tracking the color orange
greenLower =(5, 158, 200)
greenUpper =(30, 255, 255)

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

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	
	e1 = cv2.getTickCount()


	# grab the raw NumPy array representing the image - this array
	# will be 3D, representing the width, height, and # of channels
	image = frame.array

	#convert the image into a numpy array
	img_np = np.array(image)
	#then rename it frame
	frame = img_np

	#flips the frame since the camera is upside down
	frame = cv2.flip(frame,0)
	
	#turn into HSV color space
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask

	#the hue has a range of +-10
	greenLower = (h-10, s-r, v-r)
	greenUpper = (h+10, s+r, v+r) 

	mask = cv2.inRange(hsv, greenLower, greenUpper)
	#find within threshold range
	#mask = cv2.erode(mask, None, iterations=1)#destroy small specs noise
	#mask = cv2.dilate(mask, None, iterations=1)#dilate green blobs
	
	#this "res" frame pieces together 2 the mask frame and the original frame
	
	res = cv2.bitwise_and(frame,frame, mask= mask)

	
	# find contours in the mask
	#cnts is countours
	#cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
	#	cv2.CHAIN_APPROX_SIMPLE)[-2]
	
	#create variable for center
	#center = None
	
	
#Only proceed if at least one contour was found
	#if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
	#	c = max(cnts, key=cv2.contourArea)
	#	((x, y), radius) = cv2.minEnclosingCircle(c)
	#	M = cv2.moments(c)

	#	if int(M["m00"]) > 0:
			#center = (x,y) coordinates on 640,420 pixels
	#		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
	#		x_coordinate = int(M["m10"] / M["m00"])
	#		y_coordinate = int(M["m01"] / M["m00"])		

		
	#	lastSeenX = x_coordinate
	#	lastSeenY = y_coordinate

	#	print " Center ", center," Radius ", radius 

	
 	
 	# get info from track bar and appy to result
	h = cv2.getTrackbarPos('hue','Control Panel')
	s = cv2.getTrackbarPos('sat','Control Panel')
	v = cv2.getTrackbarPos('val','Control Panel')
	r = cv2.getTrackbarPos('range', 'Control Panel')	

	e2 = cv2.getTickCount()
	time = (e2 - e1)/cv2.getTickFrequency()
	print "milliSeconds" , time*1000
	#the key that is clicked save it as variable key
	
	#put the text of the values on the screen to the user can see them
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(res,format(h),(0,20), font, 0.4,(255,255,255),2,cv2.LINE_AA)
	cv2.putText(res,format(s),(60,20), font, 0.4,(255,255,255),2,cv2.LINE_AA)
	cv2.putText(res,format(v),(120,20), font, 0.4,(255,255,255),2,cv2.LINE_AA)
	cv2.putText(res,format(time*1000),(180,20), font, 0.4,(255,255,255),2,cv2.LINE_AA)


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

	cv2.imshow("res", res)

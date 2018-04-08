import os
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import imutils
import RoPi_SerialCom as ropi

resolution_w = 320
resolution_h = 240
error = 40

#Initialize camera
camera = PiCamera()
camera.resolution = (resolution_w,resolution_h)
camera.hflip = True
camera.vflip = True
rawCapture = PiRGBArray(camera)
time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    #Get camera feed
    frame = np.array(frame.array)

    #Filter out all colors except blue
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array([100,100,40])
    upper = np.array([130,255,120])
    blue = cv2.inRange(hsv, lower, upper)

    #Gray and blur
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    #Combine blue and blur into one mask
    mask = cv2.bitwise_and(blue, blur)

    #Find contours
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) [-2]

    #If no contours could be found, do nothing
    if len(cnts) > 0:
        #Find the largest contour
        c = max(cnts, key=cv2.contourArea)
        #If the largest contour is less then 100 pixels in area, do nothing
        if cv2.contourArea(c) > 100:
            #Draw a bounding rectangle
            x, y, w, h = cv2.boundingRect(c)
            #Draw a circle at the center of the rectangle
            cv2.circle(frame, (x+w/2, y+w/2), 7, (255, 255, 255), -1)
            if x+w/2 < (resolution_w/2-error):
                ropi.moveLeft()
            elif x+w/2 < (resolution_w/2+error):
                ropi.moveForwards()
            else:
                ropi.moveRight()
        else:
            ropi.moveStop()
    else:
        ropi.moveStop()

    #Update windows
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", frame)

    #Free up capture stream
    rawCapture.truncate(0)

    #Press 'q' to quit
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

#Stop drone and destroy windows
ropi.moveStop()
cv2.destroyAllWindows()

# import the necessary packages
from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2
import numpy as np
# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-n", "--num-frames", type=int, default=10,
#     help="# of frames to loop over for FPS test")
# ap.add_argument("-d", "--display", type=int, default=1,
#     help="Whether or not frames should be displayed")
# args = vars(ap.parse_args())

print("[INFO] sampling THREADED frames from `picamera` module...")
vs = PiVideoStream().start()
time.sleep(2.0)

# loop over some frames...this time using the threaded stream
while True:
    fps = FPS().start()
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width= 640)
    # check to see if the frame should be displayed to our screen
    #img = cv2.imread('opencv-logo.png',0)
    img = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(img,5)
    #img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1.13,15,param1=45,param2=25,minRadius=14,maxRadius=30)
     
    numOfCoins = None
    aed_1 = 0
    fills_25 = 0
    try:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
            
            # draw the center of the circle
            cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)
            
            if 15 <= i[2] <= 17:
                fills_25 += 1
            elif 18 <= i[2] <= 20:
                aed_1 += 1
            
        #print("Coins",len(circles[0]))
        numOfCoins = len(circles[0])    

    except:
        numOfCoins = 0
        print("No Coins")
        
        
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    frame = cv2.putText(frame, "Coins: " + str(numOfCoins), (50,50), font,1, (255,255,255), 2, cv2.LINE_AA)
    frame = cv2.putText(frame, "0.25 AED: " + str(fills_25), (50,70), font,1, (255,255,5), 2, cv2.LINE_AA)
    frame = cv2.putText(frame, "1 AED: " + str(aed_1), (50,90), font,1, (255,255,5), 2, cv2.LINE_AA)
    frame = cv2.putText(frame, "Total: " + str(aed_1 + (fills_25*0.25)), (50,110), font,1, (0,247,255), 2, cv2.LINE_AA)
    

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF == 27
    
    if key:
        break
    # update the FPS counter
    fps.update()
    fps.stop()
#     print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps())) 



# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()




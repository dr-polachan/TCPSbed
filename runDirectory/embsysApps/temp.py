
import os, sys

lib_path = os.path.abspath(os.path.join(__file__,'..','..'))	
print lib_path
sys.path.append(lib_path)

import time

import cv2
import mss
import numpy

import codec.audiovideo


from gi.repository import Gdk

s = Gdk.Screen.get_default()
width = s.get_width() 
height = s.get_height()

sct = mss.mss()

#monitor = {'top': 0, 'left': 0, 'width': width, 'height': height}
monitor = {'top': 0, 'left': 0, 'width': 640, 'height': 480}

#monitor1 = {'top': 0, 'left': 0, 'width': 1280/2, 'height': 960}
#monitor2 = {'top': , 'left': 0, 'width': width/2, 'height': height/2}

while 'Screen capturing':

        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img = numpy.array(sct.grab(monitor))

#	img = cv2.resize(img,None,fx=.5, fy=.5, interpolation = cv2.INTER_CUBIC)
	#img = cv2.resize(img,(640,480), interpolation = cv2.INTER_CUBIC)

	## encode the message
    	#img = codec.audiovideo.code(img) 
	#print len(img)

	r,g,b,x = cv2.split(img)


	encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),60]
   	result,encimg=cv2.imencode('.jpg',img,encode_param)

	img = encimg

	#img1 = codec.audiovideo.code(r) 
	#img2 = codec.audiovideo.code(g) 
	#img3 = codec.audiovideo.code(b)  

	#img1 = codec.audiovideo.decode(img1)
	#img2 = codec.audiovideo.decode(img2)
	#img3 = codec.audiovideo.decode(img3)
	
	#img = cv2.merge([img1,img2,img3])

	#img = codec.audiovideo.decode(img)
	
        # Display the picture
        cv2.imshow('OpenCV/Numpy normal', img)


        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


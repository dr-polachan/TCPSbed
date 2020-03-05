import re
import cv2
import pickle
import numpy as np

def code (msg):
	try:    	
				
		img = msg
		#r,g,b,x = cv2.split(img)
		r,g,b = cv2.split(img)
		img = cv2.merge([r,g,b])

		#img = cv2.resize(img,(800,600), interpolation = cv2.INTER_CUBIC) # to resize the image
		print "shape",img.shape

		splitCount = 6
		arr_cell = np.array_split(img, splitCount)      

		msg = [None]*splitCount
		arr_obj = [None]*1000 
		index = 0
		for i in range(splitCount):    
			row_number = arr_cell[i].shape[0]	            
			encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),80]
			result,encimg=cv2.imencode('.jpg',arr_cell[i],encode_param) 
			arr_obj[i] = [index, encimg]
			index = index+row_number	
			msg[i] = pickle.dumps(arr_obj[i],protocol=1)

			msg = [ msg[0], msg[1], msg[2], msg[3], msg[4], msg[5] ]

		return(msg)

	except:
		img = msg
		print img.shape		
		print "ISSUE FOUND"			
		msg = [ "NaN", "NaN", "NaN", "NaN" ]
		return (msg)


#frame = np.zeros(frame.shape, dtype=np.uint8)
#frame = np.zeros( (480,640,3), dtype=np.uint8)
frame = np.zeros( (600,1000,3), dtype=np.uint8)
#frame = np.zeros( (720,1280,3), dtype=np.uint8)

def decode (msg):
	global frame

	frameBackup = frame
	
	try:
		splitCount = 6
		for i in range (splitCount):
		    msg_copy = pickle.loads(msg[i])                  
		    cell_index = msg_copy[0]
		    cell = msg_copy[1]
		    cell=cv2.imdecode(cell,1)    
		    ## reconstructing image
		    x = cell_index
		    frame[x:x+cell.shape[0], 0:0+cell.shape[1]] = cell
        
	except: 
		frame = frameBackup

	return(frame)
        



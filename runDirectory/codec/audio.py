import re
#import cv2
import pickle
def code (msg):          
   	msg = pickle.dumps(msg,protocol=1)     
    	return (msg)

def decode (msg):
    	msg = pickle.loads(msg)       
    	return (msg)

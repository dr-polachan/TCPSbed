# same as local.py

import socket
import serial
import cv2
import pyaudio
import numpy as np
import mss
#from gi.repository import Gdk

def init_tx(address_tx,mode_tx): 
    if(mode_tx == "udp"):
        obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
        ret = (obj,address_tx,mode_tx)

    if(mode_tx == "udp4pkts"):
        obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
        ret = (obj,address_tx,mode_tx)

    if(mode_tx == "serial"):
        obj = serial.Serial()
        obj.port = address_tx[0]
        obj.baudrate = address_tx[1]
        obj.open()
        ret = (obj,address_tx,mode_tx)

    if(mode_tx == "microphone"):
    	p1 = pyaudio.PyAudio()
	stream1 = p1.open(format=pyaudio.paInt16,
                channels=2,
                rate=44100,
                output=True,
                frames_per_buffer=1024)
	obj = (p1,stream1)
        ret = (obj,address_tx,mode_tx)

    return(ret)
    
def init_rx(address_rx,mode_rx):
    if(mode_rx == "udp"):
        obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   
        obj.bind(address_rx)
        ret = (obj,address_rx,mode_rx)

    if(mode_rx == "udp4pkts"):
        obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   
        obj.bind(address_rx)
        ret = (obj,address_rx,mode_rx)	

    if(mode_rx == "udp-non-blocking"):
        obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   
        obj.bind(address_rx)
	obj.setblocking(0)
        ret = (obj,address_rx,mode_rx)
    if(mode_rx == "serial"):
        obj = serial.Serial()
        obj.port = address_rx[0]
        obj.baudrate = address_rx[1]
        obj.open()
        ret = (obj,address_rx,mode_rx)

    if(mode_rx == "webcam"):
	obj = cv2.VideoCapture(address_rx[0])	        
        ret = (obj,address_rx,mode_rx)
    
    if(mode_rx == "deskcam"):
	obj = mss.mss()
        ret = (obj,address_rx,mode_rx)

    if(mode_rx == "microphone"):
	p = pyaudio.PyAudio()
    	stream = p.open(format=pyaudio.paInt16,
                channels=2,
                rate=44100,
                input=True,
                frames_per_buffer=1024)
	obj = (p,stream)
        ret = (obj,address_rx,mode_rx)

    return(ret)
    
def send(obj_tx,msg):
    obj = obj_tx[0];
    address_tx = obj_tx[1]
    mode_tx = obj_tx[2]
    
    if(msg == "NULL"):
        return

    if(msg == "NaN"):
	return
    
    if(mode_tx == "udp"):
        obj.sendto(msg, (address_tx))

    if(mode_tx == "udp4pkts"):
	for i in range (6):
		obj.sendto(msg[i], (address_tx))			
    
    if(mode_tx == "serial"):
        #obj.open()
        obj.write(msg+"\n")
        #obj.close()

    if(mode_tx == "microphone"):
	obj[1].write(msg)
    
    return
    
def receive(obj_rx):
    obj = obj_rx[0];
    address_rx = obj_rx[1]
    mode_rx = obj_rx[2]
        
    if(mode_rx == "udp"):
        #obj_rx.settimeout(5.0)
        data, addr = obj.recvfrom(60000) # buffer size is 1024 bytes
	#print data[0]
        #obj_rx.settimeout(None)

    if(mode_rx == "udp4pkts"):

	msg1, addr = obj.recvfrom(60000) # buffer size is 1024 bytes
	msg2, addr = obj.recvfrom(60000) # buffer size is 1024 bytes
	msg3, addr = obj.recvfrom(60000) # buffer size is 1024 bytes
	msg4, addr = obj.recvfrom(60000) # buffer size is 1024 bytes
	msg5, addr = obj.recvfrom(60000) # buffer size is 1024 bytes
	msg6, addr = obj.recvfrom(60000) # buffer size is 1024 bytes
	data = [msg1, msg2, msg3, msg4, msg5, msg6]

    	
    if(mode_rx == "udp-non-blocking"):
        #obj_rx.settimeout(5.0)
	try:
	        data, addr = obj.recvfrom(60000) # buffer size is 1024 bytes
	except:
		data = 'NaN'
        #obj_rx.settimeout(None)

    if(mode_rx == "serial"):
        #obj.open()
        data = obj.readline();
        #obj.close()
        data = data.rstrip('\n')



    if(mode_rx == "webcam"):
	#obj = cv2.VideoCapture(0)
	(ret, frame) = obj.read()
	if(ret == True):	        
		data = frame
	else:
		data = "NaN" 


    if(mode_rx == "deskcam"):
	# get the screen size	
	#s = Gdk.Screen.get_default()
	#width = s.get_width() 
	#height = s.get_height()	
	
	#monitor = {'top': 0, 'left': 0, 'width': width, 'height': height}	
	#monitor = {'top': 0, 'left': 0, 'width': 320, 'height': 240}
	#monitor = {'top': 0, 'left': 0, 'width': 640, 'height': 480}
	#monitor = {'top': 0, 'left': 0, 'width': 800, 'height': 600}

	monitor = {'top': 0, 'left': 0, 'width': 1000, 'height': 600}

        
	# get raw desktop frame
	frame = np.array(obj.grab(monitor))
	data = frame	
	
	
    if(mode_rx == "microphone"):
	data = obj[1].read(1024)

    return(data)

def close(object): 
    mode = object[2]
    if(mode == "microphone"):
	obj_list = object[0] #object[0] is a list
	obj = obj_list[0]
    else:    
    	obj = object[0];
    	obj.close()
    return
    
    
#import socket

# def init():
    # obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
    # return(obj)

# def listen(obj_rx,local_port):
    # obj_rx.bind(('localhost',local_port))
    # return

# def send(obj_tx,msg,address):
    # obj_tx.sendto(msg, address)
    
# def close(obj):
    # obj.close()
    
    # return
        
# def receive(obj_rx):
    # #obj_rx.settimeout(5.0)
    # data, addr = obj_rx.recvfrom(1024) # buffer size is 1024 bytes
    # #obj_rx.settimeout(None)
    # return(data)

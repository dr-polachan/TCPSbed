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
    return(ret)
    
def init_rx(address_rx,mode_rx):
    if(mode_rx == "udp"):
        obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   
        obj.bind(address_rx)
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
    
    return
    
def receive(obj_rx):
    obj = obj_rx[0];
    address_rx = obj_rx[1]
    mode_rx = obj_rx[2]
        
    if(mode_rx == "udp"):
        data, addr = obj.recvfrom(60000) # buffer size is 1024 bytes  	
	
	
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
    

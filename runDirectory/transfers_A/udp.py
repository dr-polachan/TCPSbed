# same as local.py

import socket

def init_tx(address_tx): 
    obj_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
    return(obj_tx)
    
def init_rx(address_rx):
    obj_rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   
    obj_rx.bind(address_rx)
    return(obj_rx)

def send(obj_tx,msg,address_tx):
    obj_tx.sendto(msg, (address_tx))

def close(obj):
    obj.close()
    return
        
def receive(obj_rx):
    obj_rx.settimeout(10)
    try:
        data, addr = obj_rx.recvfrom(1024) # buffer size is 1024 bytes
    except socket.timeout:
    	data = "timeout"
        
    #obj_rx.settimeout(None)
    return(data)

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

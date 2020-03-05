import socket

def init_tx(address_tx):
    # #obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    obj_tx = open(address_tx,'w')
    return(obj_tx)
    
def init_rx(address_rx):    
    obj_rx = open(address_rx,'r')
    return(obj_rx)

def send(obj_tx,msg,address_tx):
    #obj_tx.sendto(msg, (address_tx))
    obj_tx.write(msg+"\n")
    return

def close(obj):
    obj.close()
    
    return
        
def receive(obj_rx):
    msg = obj_rx.readline();
    
    #obj_rx.settimeout(5.0)
    #data, addr = obj_rx.recvfrom(1024) # buffer size is 1024 bytes
    #obj_rx.settimeout(None)
    return(msg)
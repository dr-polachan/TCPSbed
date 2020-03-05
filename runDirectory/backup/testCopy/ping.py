import socket
import re #regular expression

obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

def echo_back(msg,tp):
    ret=0;
    if "ping" in msg:
        testpoint = re.search('tp:(.+?) ', msg).group(1)   
        if(testpoint == tp):
            ip= re.search('ping.+?ip:(.+?):(.+?) ', msg).group(1)
            port = int(re.search('ping.+?ip:(.+?):(.+?) ', msg).group(2))
            address = (ip,port)
            obj.sendto(msg, (address))
            ret=1
        else:    
            ret=0
    
    return(ret)
def close():
    obj.close()
    return
        

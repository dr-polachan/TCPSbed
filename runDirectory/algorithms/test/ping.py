import socket
import re 
execfile("config")

obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

def echo_back(msg,tp):
    ret=0;
    print "debug", msg
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


def echo_back_rev2(msg,tp,(rx_ip,temp)):
    ### Step-0
    ### Check if it is a ping message    
    if "ping" in msg:
	print msg
        ### Step-1
        ### check if cpepip is present (component ping entry point ip)
        ### else, add cpeip
        if(msg.find('cpeip')==-1): 
            # cpeip field does not exist
            header = re.search(r'(.*)(begin(.*))', msg).group(1)
            message = re.search(r'(.*)(begin(.*))', msg).group(2)
            cpeip = rx_ip
            msg = header+"cpeip:"+cpeip+" "+message

	    print "cpeip = -1"
    
        ### Step-2
        ### check for matching test point     
        testpoint = re.search('tp:(.+?) ', msg).group(1)   
        if(testpoint == tp):            
            cpeip = re.search('cpeip:(.*) begin(.*)', msg).group(1)
            if(cpeip == rx_ip):
                ip= re.search('ping.+?ip:(.+?):(.+?) ', msg).group(1)
                port = int(re.search('ping.+?ip:(.+?):(.+?) ', msg).group(2))
                address = (ip,port)
            else:		                
		if(rx_ip == srv_ip):
                    address = (ms_com_ip, ping_link)
                elif(rx_ip == ss_com_ip):
                    address = (srv_ip, ping_link)
            print "address", address
                
	    ### Step-3
   	    ### echo back            
            obj.sendto(msg, (address))
    return(msg)

def transfer(msg,(rx_ip,temp)):
    ### Step-0             
    cpeip = re.search('cpeip:(.*) begin(.*)', msg).group(1)
    if(cpeip == rx_ip):
        ip= re.search('ping.+?ip:(.+?):(.+?) ', msg).group(1)
        port = int(re.search('ping.+?ip:(.+?):(.+?) ', msg).group(2))
        address = (ip,port)
    else:		                
	if(rx_ip == srv_ip):
            address = (ms_com_ip, ping_link)
        elif(rx_ip == ss_com_ip):
            address = (srv_ip, ping_link)
        
    ### Step-3
    ### echo back            
    obj.sendto(msg, (address))

    return(msg)

def close():
    obj.close()
    return



        

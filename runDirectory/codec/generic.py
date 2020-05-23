import re

def code (my_list):
    my_list_str = map(str,my_list)
    msg = " ".join(my_list_str) 
    msg = "begin" + " " + msg + " " + "end"    
    return (msg)
    
def codev2(msg,msg_list):
    msg_list_str = map(str,msg_list)
    temp1 = " ".join(msg_list_str) 
    temp1 = "begin" + " " + temp1 + " " + "end"    
    result = re.sub(r'(begin(.+?)end)', temp1, msg) 
    return(result)

def decode (msg):
    if(re.search('begin (.+?) end', msg)):
    	str = re.search('begin (.+?) end', msg).group(1)
    else:
	str = "NaN"
    myArray = str.split(" ");
    return(myArray)
    


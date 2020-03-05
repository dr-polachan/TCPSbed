import re

def code (my_list):
    my_list_str = map(str,my_list)
    msg = " ".join(my_list_str) #join list items with space
    msg = "begin" + " " + msg + " " + "end"    
    return (msg)
    
def codev2(msg,msg_list):
    #msg is what is received
    #msg_list contains the extracted data
    msg_list_str = map(str,msg_list)
    temp1 = " ".join(msg_list_str) #join list items with space
    temp1 = "begin" + " " + temp1 + " " + "end"    
    #print temp1
    result = re.sub(r'(begin(.+?)end)', temp1, msg) #subst temp1 
    return(result)

def decode (msg):
    #if(re.search('.+?begin (.+?) end', msg)):
    if(re.search('begin (.+?) end', msg)):
    	str = re.search('begin (.+?) end', msg).group(1)
    else:
	str = "NaN"
    myArray = str.split(" ");
    return(myArray)
    
if __name__ == '__main__':
    #list = [22.34,44]
    #print code(list)
    #print 'DONE !!!'
    #myarr = decode("begin 222 233.22 end")
    #print myarr
    #msg = "begin 20 30 20 end"
    msg = "ping seq:NIL ip:10.114.56.165:4025 tp:tp_embsys_entry begin 15 0 10 150 206 end "
    msg_list = [20.00,31.3]
    print codev2(msg,msg_list)
    
#def code1 (msg, data_1,data_2,data_3,data_4,data_5):
#    data_5 = int(data_5)
#    t1 = "begin "+str(data_1)+" "+str(data_2)+" "+str(data_3)+" "+str(data_4)+" "+str(data_5)+" 50 end";
#    
#    result = re.sub(r'(begin(.+?)end)', t1, msg) 
#    return (result)

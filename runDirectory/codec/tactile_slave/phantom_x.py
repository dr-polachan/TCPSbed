### Importing Modules
import re

def code (data_1,data_2,data_3,data_4,data_5):
   #msg = "begin "+str(data_1)+" "+str(data_2)+" "+str(data_3)+" "+str(data_4)+" "+str(data_5)+" end";
    msg = "begin "+ str(data_1)+" "+str(data_2)+" "+str(data_3)+" "+str(data_4)+" "+str(data_5)+" 50 end";
    return (msg)

def code1 (msg, data_1,data_2,data_3,data_4,data_5):
    data_5 = int(data_5)
    t1 = "begin "+str(data_1)+" "+str(data_2)+" "+str(data_3)+" "+str(data_4)+" "+str(data_5)+" 50 end";
    
    result = re.sub(r'(begin(.+?)end)', t1, msg) 
    return (result)
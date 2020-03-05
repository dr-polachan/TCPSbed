
    
import re

def decode (msg):
   #print "debug",msg
   
   str = re.search('(begin(.+?)end)', msg)
   if(str):
    str = str.group(1)
   else: 
    str = "NULL"
   #str = re.search('(begin(.+?)end)', msg).group(1)
   #print "debug",str
   #print str
   #str = msg
   #print str
   return(str)

def decodesrv (msg):
   str = re.search('(begin(.+?)end)', msg)
   if(str):
    str = str.group(1)   
    myArray = str.split(" ");
    vibrator1 = float(myArray[1])
    vibrator2 = float(myArray[2])   
   else:
    vibrator1=200
    vibrator2=200
  
   return (vibrator1,vibrator2)   
   
   
if __name__ == '__main__':
   msg = "ping seq:NIL ip:10.114.56.165:4025 tp:tp_act begin 10 0 10 150 204 end " 
   msg = "send begin 4095 4095 end"
   result = re.search('begin.+?end', msg)
   if result:
    print "sucess"
   else:
    print "fail"
   str = re.search('(begin(.+?)end)', msg).group(1)
   print str
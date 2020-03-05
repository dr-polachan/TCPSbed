### Importing Modules

import re

# cyber-glove format
## input: #<vibrator1>*vibrator2*@
## output: #<x>*<y>*<z>*<pitch>*<pincher>*@

def code_vMtech (msg_list):
   try:
   	vibrator1 = str(msg_list[0])
   	vibrator2 = str(msg_list[1])
   except:
	vibrator1 = "255"
	vibrator2 = "255"
   
   msg = "#"+vibrator1+"*"+vibrator2+"*@"      
   return (msg)

def decode_vMtech (msg):   
   str = re.search('#(.+?)@', msg).group(1)
   myArray = str.split("*");
   x = (myArray[0])
   y = (myArray[1])
   z = (myArray[2])
   pitch = (myArray[3])
   pincher = (myArray[4])
   return (x,y,z,pitch,pincher)

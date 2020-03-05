### Importing Modules

# format:
#"ping seq:1234 tp:tp1 begin 10 0 10 150 200 end"
import re

def decode (msg):
   
   str = re.search('(begin(.+?)end)', msg).group(1)
   myArray = str.split(" ");
   
   x = float(myArray[1])
   y = float(myArray[2])
   z = float(myArray[3])
   
   pitch = float(myArray[4])
   
   pincher = float(myArray[5])   
   return (x,y,z,pitch,pincher)

def code_version_mtech (msg):
   
   str = re.search('(begin(.+?)end)', msg).group(1)
   myArray = str.split(" ");
   #myArray[0] => "begin"
   vibrator1 = (myArray[1])
   vibrator2 = (myArray[2])
   msg = "#"+vibrator1+"*"+vibrator2+"*@"      
   return (msg)

def decode_version_mtech (msg):   
   str = re.search('#(.+?)@', msg).group(1)
   myArray = str.split("*");
   x = (myArray[0])
   y = (myArray[1])
   z = (myArray[2])
   pitch = (myArray[3])
   pincher = (myArray[4])
   return (x,y,z,pitch,pincher)
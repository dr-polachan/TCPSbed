#!/usr/bin/env python

from pynput import mouse  
import os, sys
lib_path = os.path.abspath(os.path.join(__file__,'..','..'))	
print lib_path
sys.path.append(lib_path)
import transfers1.rev1 as transfers
execfile("./src/server_settings.py")

axis_x = 0
axis_y = 0
axis_z = 0
button_left = 0 
button_right = 0 
scroll = 0

obj_tx = [None]

def message_format(axis_x,axis_y,axis_z,button_left,button_right,scroll):
    msg = "begin "  + str(axis_x)
    msg = msg + " " + str(axis_y)
    msg = msg + " " + str(axis_z)
    msg = msg + " " + str(button_left)
    msg = msg + " " + str(button_right)
    msg = msg + " " + str(scroll)
    msg = msg + " end\n"
    return(msg)

def on_move(x, y):
    
    global axis_x
    global axis_y
    global axis_z
    global button_left
    global button_right
    global scroll
    
    global obj_tx

    axis_x = x
    axis_y = y
    
    
    print axis_x,axis_y,axis_z,button_left,button_right,scroll
    
    msg = message_format(axis_x,axis_y,axis_z,button_left,button_right,scroll)
    transfers.send(obj_tx,msg)            
    
def on_click(x, y, button, pressed):
           
    global axis_x
    global axis_y
    global axis_z
    global button_left
    global button_right
    global scroll
    
    
    if((button == button.left) and (pressed == True)):
        button_left = 1
        
    if((button == button.left) and (pressed == False)):
        button_left = 0
    
    if((button == button.right) and (pressed == True)):
        button_right = 1
        
    if((button == button.right) and (pressed == False)):
        button_right = 0

   
    print axis_x,axis_y,axis_z,button_left,button_right,scroll
    
    msg = message_format(axis_x,axis_y,axis_z,button_left,button_right,scroll)
    transfers.send(obj_tx,msg)    
    
def on_scroll(x, y, dx, dy):
    
    global axis_x
    global axis_y
    global axis_z
    global button_left
    global button_right
    global scroll
    
    if(dy < 0):
        scroll = scroll - 1
	if(scroll < 0):
		scroll = 0
    else:
        scroll = scroll + 1
	if(scroll > 25):
		scroll = 25
        
    print axis_x,axis_y,axis_z,button_left,button_right,scroll

    msg = message_format(axis_x,axis_y,axis_z,button_left,button_right,scroll)
    transfers.send(obj_tx,msg)    

if __name__ == '__main__':         
    # defining tx address/mode
    address_tx = (ms_com_ip,kin_link_0)
    mode_tx = "udp"
    
    # initialize 
    obj_tx = transfers.init_tx(address_tx,mode_tx)
        
    # collect events until released
    with mouse.Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll) as listener:
        listener.join()
    
    # exit
    transfers.close(obj_tx)

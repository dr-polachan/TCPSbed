from __future__ import division
from algorithms.kinematics.sub_mouse_controller import controller as controller

def revGeneric (msg_list): 
    msg_list = map(int, msg_list)
    (x,y,temp,btn_left,btn_right,scroll) = msg_list
    
    msg_list = (x,y,scroll,(btn_left,btn_right)) #re-arranging arguments
    (x,y,z,scroll) = controller(msg_list) #returns calibrated [x_out,y_out,z_out,scroll_out]
    
    # scaling
    x = x/10
    y = y/10
    z = z/10

    # rearranging for robot
    robo_x = y
    robo_y = -1*x #check phantom-x i-k implementation
    robo_z = z
    robo_pincher = scroll*4
    
    # bounddary conditions
    if(robo_z < -8):
	robo_z = -8
    if (robo_x < 5):
	robo_x = 5
    if(robo_pincher > 512):
	robo_pincher = 512
    if(robo_pincher < 0):
	robo_pincher = 0

    # initial condition
    robo_x = robo_x
    robo_y = robo_y
    robo_z = robo_z

    ret_list = (robo_x,robo_y,robo_z,0,robo_pincher) #robot-x = y, robot-y = x, robot-pitch=0, robot-pincher=scroll
    
    return (ret_list) 





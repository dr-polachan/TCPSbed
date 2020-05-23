from __future__ import division
from algorithms.kinematics.lib_mouse_controller.sub_mouse_controller import controller as controller

def revGeneric (msg_list): 
    msg_list = map(int, msg_list)
    (x,y,temp,btn_left,btn_right,scroll) = msg_list
    
    msg_list = (x,y,scroll,(btn_left,btn_right)) 
    (x,y,z,scroll) = controller(msg_list) 
    
    ### scaling
    x = x/10
    y = y/10
    z = z/10

    ### rearranging axis for robot
    robo_x = y
    robo_y = -1*x 
    robo_z = z
    robo_pincher = scroll*4
    
    ### boundary conditions
    if(robo_z < -8):
	robo_z = -8
    if (robo_x < 5):
	robo_x = 5
    if(robo_pincher > 512):
	robo_pincher = 512
    if(robo_pincher < 0):
	robo_pincher = 0

    ### initial condition
    robo_x = robo_x
    robo_y = robo_y
    robo_z = robo_z

    ret_list = (robo_x,robo_y,robo_z,0,robo_pincher)
    
    return (ret_list) 





#!/usr/bin/env python

import transfers1.rev1 as transfers
import algorithms.test.ping as ping
from time import sleep
import codec.generic
import codec.cyber_glove
import algorithms.kinematics.mouse_controller
import algorithms.kinematics.hapticGlove

def forward_flow_kinematic():     
    ### defining in/out address/mode
    address_rx = ms_com_fwd_flow_kinematic_entry_addr
    address_tx = ms_com_fwd_flow_kinematic_exit_addr    
    mode_rx = ms_com_fwd_flow_kinematic_entry_mode
    mode_tx = ms_com_fwd_flow_kinematic_exit_mode
    
    ### initialization
    obj_tx = transfers.init_tx(address_tx,mode_tx)
    obj_rx = transfers.init_rx(address_rx,mode_rx)
    
    while (1):
        print "live_mscom_fwd",time.time()

        ### receive message
        msg = transfers.receive(obj_rx) #msg=> (x,y,z,button-left,button-right,scroll-wheel)
        msg = ping.echo_back_rev2(msg,"tpf_ms_com_entry", address_rx)

        ### decode message
	msg_list = codec.generic.decode(msg) #msg_list = (x,y,z,pitch,pincher) 
	print msg_list
	#print msg_list

	### kinematics algorithm

		#msg_list = msg_list # for demonstrating step response
		#msg_list = msg_list # for demonstrating robot actuation delay

		#msg_list = algorithms.kinematics.hapticGlove.rev1(msg_list) # return => (wristX, wristY, wristZ, palmPitch, palmPincher) for phantomX
		
		#print "result: ", msg_list

	#msg_list = algorithms.kinematics.mouse_controller.revGeneric(msg_list) # return: msg-list => (x,y,z,pitch=0,pincher), to use with mouse controller
		#print "debug", msg_list
		#msg_list = algorithms.kinematics.mouse_controller.rev1(msg_list) # msg-list => (x,y,z,pitch=0,pincher) for phantomX
		#msg_list = algorithms.kinematics.mouse_controller.rev_testmode(msg_list) # msg-list => (x,y,z,pitch=0,pincher) for generic use
		
		#print "result", msg_list
		#print "out",msg_list
		#msg_list = codec.cyber_glove.decode_vMtech(msg) #msg_list = (x,y,z,pitch,pincher)        
		#msg_list = codec.generic.decode(msg) #msg_list = (x,y,z,pitch,pincher) 
		#msg_list = algorithms.mouse.calibration(msg_list)
                	
        ### code message        
        msg = codec.generic.codev2(msg,msg_list)

        ### send to tactile slave
	transfers.send(obj_tx,msg); 					
        msg = ping.echo_back_rev2(msg,"tpf_ms_com_exit", address_rx)
    
    transfers.close(obj_tx)
    transfers.close(obj_rx)

    return

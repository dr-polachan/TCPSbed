#!/usr/bin/env python

import algorithms.kinematics.cyber_glove
import algorithms.inverse_kinematics.vrepPhantomX
import codec.tactile_slave.phantom_x
import codec.tactile_master.cyber_glove
import codec.generic
import transfers1.rev1 as transfers
import algorithms.test.ping as ping
import algorithms.compression.kees
import algorithms.kinematics.mouse_controller


def forward_flow_kinematic():     
    ### defining in/out address/mode
    address_rx = server_fwd_flow_kinematic_entry_addr
    address_tx = server_fwd_flow_kinematic_exit_addr    
    mode_rx = server_fwd_flow_kinematic_entry_mode
    mode_tx = server_fwd_flow_kinematic_exit_mode
    
    ### initialization
    obj_tx = transfers.init_tx(address_tx,mode_tx)
    obj_rx = transfers.init_rx(address_rx,mode_rx)
    
    while (1):
    #for myvar in range (2):
        print "live_srv_fwd",time.time()
        
        ### receive message
        msg = transfers.receive(obj_rx)
	print "received:",msg
        ping.echo_back_rev2(msg,"tpf_srv_entry",address_rx)

        ### decode message
        msg_list = codec.generic.decode(msg) #msg_list (return value):(x,y,z, pitch, pincher)
        ping.echo_back_rev2(msg,"tpf_srv_1",address_rx)        	
		
        ### run kinematics algorithm (here)
	msg_list = algorithms.kinematics.mouse_controller.revGeneric(msg_list) # return: msg-list => (x,y,z,pitch=0,pincher), to use with mouse controller
	ping.echo_back_rev2(msg,"tpf_srv_2",address_rx)
        
        ### run inverse kinematics algorithm              
        #msg_list = algorithms.inverse_kinematics.phantom_x.py_fsolve(msg_list) #msg_list (return value):(joint1, joint2, joint3, pitch, pincher,velocity)
        
	msg_list = algorithms.inverse_kinematics.vrepPhantomX.py_fsolve(msg_list) #msg_list (return value):(joint1, joint2, joint3, joint4, gripperPos)
        ping.echo_back_rev2(msg,"tpf_srv_3",address_rx)    

        ### code the message        
        msg = codec.generic.codev2(msg,msg_list)
        ping.echo_back_rev2(msg,"tpf_srv_4",address_rx)
	
        ### send message
        transfers.send(obj_tx,msg)
        ping.echo_back_rev2(msg,"tpf_srv_exit",address_rx)
	#print "send:", msg
    
    transfers.close(obj_tx)
    transfers.close(obj_rx)

    return

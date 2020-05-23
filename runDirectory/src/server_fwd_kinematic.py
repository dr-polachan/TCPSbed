import algorithms.inverse_kinematics.vrepPhantomX
import codec.generic
import transfers.rev1 as transfers
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

        print "live_srv_fwd",time.time()
        
        ### receive message
        msg = transfers.receive(obj_rx)

        ### decode message
        msg_list = codec.generic.decode(msg) #msg_list:(x,y,z, pitch, pincher)
		
        ### run kinematics algorithm (here)
	msg_list = algorithms.kinematics.mouse_controller.revGeneric(msg_list) # msg-list: (x,y,z,pitch=0,pincher)
        
        ### run inverse kinematics algorithm                     
	msg_list = algorithms.inverse_kinematics.vrepPhantomX.py_fsolve(msg_list) #msg_list:(joint1, joint2, joint3, joint4, gripperPos)

        ### code the message        
        msg = codec.generic.codev2(msg,msg_list)
	
        ### send message
        transfers.send(obj_tx,msg)


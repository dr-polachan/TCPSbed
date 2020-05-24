import algorithms.inverse_kinematics.vrep_phantomx
import codec.generic
import transfers.rev1 as transfers
import algorithms.kinematics.mouse_controller


def forward_flow_kinematic():     
    
    ### initialization
    obj_tx = transfers.init_tx(srv_kin_exit_addr,srv_kin_exit_mode)
    obj_rx = transfers.init_rx(srv_kin_entry_addr,srv_kin_entry_mode)
    
    while (1):

        print "live_srv_fwd",time.time()

        ### receive message
        msg = transfers.receive(obj_rx)

        ### decode message
        msg_list = codec.generic.decode(msg) #msg_list:(x,y,z, pitch, pincher)

        ### run kinematics algorithm (here)
        msg_list = algorithms.kinematics.mouse_controller.revGeneric(msg_list) # msg-list: (x,y,z,pitch=0,pincher)

        ### run inverse kinematics algorithm                     
        msg_list = algorithms.inverse_kinematics.vrep_phantomx.py_fsolve(msg_list) #msg_list:(joint1, joint2, joint3, joint4, gripperPos)

        ### code the message        
        msg = codec.generic.code(msg_list)

        ### send message
        transfers.send(obj_tx,msg)


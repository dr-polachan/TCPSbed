#!/usr/bin/env python

import transfers1.rev1 as transfers
import codec.generic
import algorithms.test.ping as ping
import algorithms.hapticSense.flexiForce
import algorithms.hapticFeedback.vibroTactile

### forward flow engine
def backward_flow_haptic():  
    ### defining in/out address/mode
    address_rx = server_bwd_flow_haptic_entry_addr
    address_tx = server_bwd_flow_haptic_exit_addr    
    mode_rx = server_bwd_flow_haptic_entry_mode
    mode_tx = server_bwd_flow_haptic_exit_mode
    
    ### initialization
    obj_tx = transfers.init_tx(address_tx,mode_tx)
    obj_rx = transfers.init_rx(address_rx,mode_rx)
    
    while (1):
    #for myvar in range (2):
        print "live_srv_bwd",time.time()
        ### receive message
        msg = transfers.receive(obj_rx)

	#print msg
        ping.echo_back(msg,"tp_srv_bwd_entry")
        
        ### decode the messasge       
        msg_list = codec.generic.decode(msg) # msg_list = [force-sensor-1-data, force-sensor-2-data]
        ping.echo_back(msg,"tp_srv_bwd_1")
        
	##

	#msg_list = algorithms.hapticSense.flexiForce.rev1(msg_list)         
	#test.ping.echo_back(msg,"tp_srv_bwd_2")

	### for haptic feedback
	#msg_list = algorithms.hapticFeedback.vibroTactile.bypass(msg_list)         
	#test.ping.echo_back(msg,"tp_srv_bwd_3")
        
        ### encode the message
        #msg = codec.generic.code(msg_list)
        msg = codec.generic.codev2(msg,msg_list)
        print msg;
        ping.echo_back(msg,"tp_srv_bwd_4")
        
        ### send the message
        transfers.send(obj_tx,msg)
        test.ping.echo_back(msg,"tp_srv_bwd_exit")
        
    transfers.close(obj_tx)
    transfers.close(obj_rx)
    return



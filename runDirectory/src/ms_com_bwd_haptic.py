import codec.generic
import transfers.rev1 as transfers

def backward_flow_haptic():     

    ### initialization
    obj_tx = transfers.init_tx(ms_com_hap_exit_addr,ms_com_hap_exit_mode)
    obj_rx = transfers.init_rx(ms_com_hap_entry_addr,ms_com_hap_entry_mode)
    
    while (1):
       
        print "live_mscom_bwd_haptic",time.time()
        ### receive message
	msg = transfers.receive(obj_rx)
        
        ### decode the message
        msg_list = codec.generic.decode(msg)
	print "force feedback", msg_list
                   
	### code message        
	msg = codec.generic.code(msg_list)
        
        ### send message
	transfers.send(obj_tx,msg)




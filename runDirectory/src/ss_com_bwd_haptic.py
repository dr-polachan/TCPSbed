import transfers.rev1 as transfers

def backward_flow_haptic():   
    ### defining in/out address/mode
    address_rx = ss_com_bwd_flow_haptic_entry_addr
    address_tx = ss_com_bwd_flow_haptic_exit_addr_A    
    mode_rx = ss_com_bwd_flow_haptic_entry_mode
    mode_tx = ss_com_bwd_flow_haptic_exit_mode
    
    ### initialization
    obj_tx_A = transfers.init_tx(address_tx,mode_tx)
    obj_tx_B = transfers.init_tx(ss_com_bwd_flow_haptic_exit_addr_B,mode_tx)
    obj_rx = transfers.init_rx(address_rx,mode_rx)

        
    while (1):
        print "live_sscom_bwd",time.time()
        
        ### receive message
        msg = transfers.receive(obj_rx)
        
        ### send message
	transfers.send(obj_tx_A,msg); 		
	transfers.send(obj_tx_B,msg); 								




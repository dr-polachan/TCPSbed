import transfers.rev1 as transfers

def backward_flow_haptic():   

    ### initialization
    obj_tx_A = transfers.init_tx(ss_com_hap_exit_addr_A,ss_com_hap_exit_mode)
    obj_tx_B = transfers.init_tx(ss_com_hap_exit_addr_B,ss_com_hap_exit_mode)
    obj_rx = transfers.init_rx(ss_com_hap_entry_addr,ss_com_hap_entry_mode)


    while (1):
        print "live_sscom_bwd",time.time()

        ### receive message
        msg = transfers.receive(obj_rx)

        ### send message
        transfers.send(obj_tx_A,msg); 		
        transfers.send(obj_tx_B,msg); 								




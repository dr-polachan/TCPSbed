import transfers.rev1 as transfers
import codec.generic

def backward_flow_haptic():  

    ### initialization
    obj_tx = transfers.init_tx(srv_hap_exit_addr,srv_hap_exit_mode)
    obj_rx = transfers.init_rx(srv_hap_entry_addr,srv_hap_entry_mode)
    
    while (1):

        print "live_srv_bwd",time.time()

        ### receive message
        msg = transfers.receive(obj_rx)
        print msg
        ### decode the messasge       
        msg_list = codec.generic.decode(msg) # msg_list = [force-sensor-1-data, force-sensor-2-data]
                
        ### encode the message
        msg = codec.generic.code(msg_list)
        
        ### send the message
        transfers.send(obj_tx,msg)



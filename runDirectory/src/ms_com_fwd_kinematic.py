import transfers.rev1 as transfers
from time import sleep
import codec.generic


def forward_flow_kinematic():     

    ### initialization
    obj_tx_A = transfers.init_tx(ms_com_kin_exit_addr_A,ms_com_kin_exit_mode)
    obj_tx_B = transfers.init_tx(ms_com_kin_exit_addr_B,ms_com_kin_exit_mode)
    obj_rx = transfers.init_rx(ms_com_kin_entry_addr,ms_com_kin_entry_mode)
    
    while (1):
        print "live_mscom_fwd",time.time()

        ### receive message
        msg = transfers.receive(obj_rx)

        ### decode message
        msg_list = codec.generic.decode(msg) 
            	
        ### code message        
        msg = codec.generic.code(msg_list)

        ### send to tactile slave
        transfers.send(obj_tx_A,msg)
        transfers.send(obj_tx_B,msg)                   
				
    

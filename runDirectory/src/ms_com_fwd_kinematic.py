import transfers.rev1 as transfers
from time import sleep
import codec.generic
import algorithms.test.ping as ping


def forward_flow_kinematic():     

    ### initialization
    obj_tx_A = transfers.init_tx(ms_com_kin_exit_addr_A,ms_com_kin_exit_mode)
    obj_tx_B = transfers.init_tx(ms_com_kin_exit_addr_B,ms_com_kin_exit_mode)
    obj_rx = transfers.init_rx(ms_com_kin_entry_addr,ms_com_kin_entry_mode)
    obj_codec = codec.v1()
    
    while (1):
        print "live_mscom_fwd",time.time()

        ### receive message
        msg = transfers.receive(obj_rx)

        ### decode message
        #msg_list = codec.generic.decode(msg) 
        msg_list = obj_codec.v1.decode(msg)
            	
        ### code message        
        #msg = codec.generic.codev2(msg,msg_list)
        msg = obj_codec.v1.code(msg_list)

        ### send to tactile slave
        transfers.send(obj_tx_A,msg)
        transfers.send(obj_tx_B,msg)                   
				
        #msg = ping.echo_back_rev2(msg,"tpf_ms_com_entry", ms_com_kin_entry_addr)
        msg = ping.echo_back(msg, "tpf_ms_com_entry")

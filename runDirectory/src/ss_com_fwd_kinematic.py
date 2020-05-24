#!/usr/bin/env python

import transfers.rev1 as transfers
import codec.generic
import time
   
def forward_flow_kinematic():     

    ### initialization
    obj_tx = transfers.init_tx(ss_com_kin_exit_addr,ss_com_kin_exit_mode)
    obj_rx = transfers.init_rx(ss_com_kin_entry_addr,ss_com_kin_entry_mode)
    
    while (1):
		print "live_sscom_fwd",time.time()

		### receive message
		msg = transfers.receive(obj_rx)

		### decode message
		msg_list = codec.generic.decode(msg) 

		### encode message
		msg = codec.generic.code(msg_list)

		### send to tactile slave
		transfers.send(obj_tx,msg)

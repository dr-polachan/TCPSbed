import transfers.rev1 as transfers
import codec.generic as codec
import algorithms.prediction.ss_ei as edge
import time

def forward_flow_kinematic():     

	### initialization
	obj_tx_kinematic = transfers.init_tx(ss_ei_kin_exit_addr, ss_ei_kin_exit_mode) 
	obj_rx_kinematic = transfers.init_rx(ss_ei_kin_entry_addr,ss_ei_kin_entry_mode) 
	obj_rx_haptic = transfers.init_rx(ss_ei_hap_entry_addr,ss_ei_hap_entry_mode) 
	obj_predict = edge.predict()

	while (1):

		print "live_ss-ei",time.time()

		### sampling time
		time.sleep(1e-3)

		### receive message
		msg_kinematic = transfers.receive(obj_rx_kinematic)
		msg_haptic = transfers.receive(obj_rx_haptic)

		### decode message
		msg_kinematic_list = codec.decode(msg_kinematic) 
		msg_haptic_list = codec.decode(msg_haptic) 

		### predict kinematic command
		msg_kinematic_list = obj_predict.run(msg_kinematic_list,msg_haptic_list)

		### encode message
		msg_kinematic = codec.codev2(msg_kinematic,msg_kinematic_list)

		### send message
		transfers.send(obj_tx_kinematic,msg_kinematic)
 
def bypass():     

	### initialization
	obj_rx_kinematic = transfers.init_rx(ss_ei_kin_entry_addr,"udp") 
	obj_tx_kinematic = transfers.init_tx(ss_ei_kin_exit_addr, "udp") 


	while (1):

		print "live_ss-ei (bypass-mode)",time.time()

		### receive message
		msg_kinematic = transfers.receive(obj_rx_kinematic)

		### send message
		transfers.send(obj_tx_kinematic,msg_kinematic)
 

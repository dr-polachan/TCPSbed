import transfers.rev1 as transfers
import codec.generic as codec
import algorithms.prediction.ms_ei as edge
import time

def backward_flow_haptic():     

	### initialization
	obj_rx_haptic = transfers.init_rx(ms_ei_hap_entry_addr,ms_ei_hap_entry_mode) 
	obj_tx_haptic = transfers.init_tx(ms_ei_hap_exit_addr, ms_ei_hap_exit_mode) 
	obj_rx_kinematic = transfers.init_rx(ms_ei_kin_entry_addr,ms_ei_kin_entry_mode) 
	obj_predict = edge.predict()
	
	while (1):

		print "live_ms-ei",time.time()

		### sampling time
		time.sleep(10e-3)

		### receive message
		msg_haptic = transfers.receive(obj_rx_haptic)
		msg_kinematic = transfers.receive(obj_rx_kinematic)

		### decode message
		msg_haptic_list = codec.decode(msg_haptic) 
		msg_kinematic_list = codec.decode(msg_kinematic) 

		### predict haptic command
		msg_haptic_list = obj_predict.run(msg_haptic_list, msg_kinematic_list)

		### encode message
		msg_haptic = codec.code(msg_haptic_list)

		### send message
		transfers.send(obj_tx_haptic,msg_haptic)

def bypass():     

	### initialization
	obj_rx_haptic = transfers.init_rx(ms_ei_hap_entry_addr,"udp") 
	obj_tx_haptic = transfers.init_tx(ms_ei_hap_exit_addr, "udp") 
	
	
	while (1):

		print "live_ms-ei (bypass-mode)",time.time()

		### receive message
		msg_haptic = transfers.receive(obj_rx_haptic)

		### send message
		transfers.send(obj_tx_haptic,msg_haptic)
 

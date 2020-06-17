#!/usr/bin/env python
import transfers_A.udp
import transfers_A.file
import os
import multiprocessing 
from multiprocessing import Process, Queue
import time
import re
import sys
import pandas as pd

### settings
execfile("./src/global_settings.py")

df = pd.read_excel("./src/data-files/da_vinci_suturing_b001.xlsx", header=0)

test_pc_ip = ms_com_ip 
test_pc_udp_port = 7000

## echo count, interval
const_ping_count = 1000 # number of echo commands to send 

## list of echo points
list_tp = ['tpf_ss_com_exit']  

## echo inject and receive address
address_udp_send = (ms_com_ip,kin_link_0)
address_udp_receive = (test_pc_ip, test_pc_udp_port) 

const_echoback_address = test_pc_ip+":"+str(test_pc_udp_port)

address_file_write1 =('./results/qos-analysis/data_received.txt')
address_file_write = ('./results/qos-analysis/data_send.txt')


def send(q):

	address_tx = address_udp_send
	address_tx_file = address_file_write;

	obj_tx = transfers_A.udp.init_tx(address_tx)
	obj_tx_file = transfers_A.file.init_tx(address_tx_file)
    
	global messageToSend

	index_df = 1

	for seq in range(100000,(100000+const_ping_count)):      

		for i in list(list_tp):	    		

			 
			## send command	
			raw_x = df["x"].loc[index_df]
			raw_y = df["y"].loc[index_df]
			raw_z = df["z"].loc[index_df]
			raw_sleep_time = df["time"].loc[index_df]-df["time"].loc[index_df-1]

			msg = "begin"+" "+str(raw_x)+" "+str(raw_y)+" "+str(raw_z)+" "+"0 0 end"
			
			time.sleep(raw_sleep_time) # wait time     	
			
			tp = i
			msgHeader = "ping seq:"+str(seq)+" "+"ip:"+const_echoback_address+" "+"tp:"+tp+" " 	# ping header
			msg = msgHeader + msg		 						# actual-message
			transfers_A.udp.send(obj_tx,msg,address_tx)        
			time1 = '{0:6f}'.format(time.time())
			msg = "time_send:"+time1 + " " + msg       
			transfers_A.file.send(obj_tx_file,msg,address_tx_file)

			index_df = index_df + 1
        
	print "send_completed"

	transfers_A.udp.close(obj_tx)
	transfers_A.file.close(obj_tx_file)

	return
    
def receive(q):
    
	address_rx = ("0.0.0.0", test_pc_udp_port)
	address_tx_file = address_file_write1;

	obj_rx = transfers_A.udp.init_rx(address_rx)
	obj_tx_file = transfers_A.file.init_tx(address_tx_file)

	var_done_counter = 0;
	flag = 0;

	while(1):
		msg = transfers_A.udp.receive(obj_rx)

		if(msg=="timeout"):
			break

		print "<<",msg
		time1 = '{0:6f}'.format(time.time())
		msg = "time_received:"+time1+" "+msg
		transfers_A.file.send(obj_tx_file,msg,address_tx_file)
                  
	print "receive_completed"
   
	transfers_A.udp.close(obj_rx)
	transfers_A.file.close(obj_tx_file)
	q.put("kill")

	return

### multiprocessing
if __name__ == '__main__':
	q = Queue()
	p1 = multiprocessing.Process(target=send,args=(q,))
	p2 = multiprocessing.Process(target=receive,args=(q,))

	p1.start()
	p2.start()
    
	while(1):
            
		if(q.get() == "kill"):
			break

		time.sleep(1)                                        
            
	print "killing multiprocessing ..."

	p1.terminate()
	p2.terminate()

	p1.join()
	p2.join()
	
	print 'DONE !!!'




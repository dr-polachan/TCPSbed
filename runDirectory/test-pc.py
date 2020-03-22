#!/usr/bin/env python

import transfers_A.udp
import transfers_A.file
import multiprocessing 
from multiprocessing import Process, Queue
import time
import re
import sys

### settings
execfile("./src/server_settings.py")
test_pc_ip = "10.0.0.1"
test_pc_udp_port = 6008

## ping count, interval
const_ping_count = 1 # number of ping commands to send 
const_interpkt_delay_ms = 10 #1000; #interpacket delay in milli seconds

## ping test points
#list_tp = ['tpf_ms_com_entry', 'tpf_ms_com_exit']
#list_tp = ['tpf_srv_entry', 'tpf_srv_exit', 'tpf_ss_com_entry','tpf_ss_com_exit']
#list_tp = ['tpf_ms_com_entry', 'tpf_ms_com_exit', 'tpf_srv_entry', 'tpf_srv_exit', 'tpf_ss_com_entry','tpf_ss_com_exit', 'tpf_ss_embsys_entry', 'tpf_ss_embsys_exit']

list_tp = ['tpf_ms_com_entry', 'tpf_ms_com_exit', 'tpf_srv_entry','tpf_srv_exit','tpf_ss_com_entry', 'tpf_ss_com_exit']
#list_tp =['tpf_ss_embsys_entry']
#list_tp =['tpf_srv_entry']
#list_tp = ['tpf_ms_com_entry', 'tpf_ms_com_exit']

## ping inject/receive address
address_udp_send = (ms_com_ip,kin_link_0) # ip-address,port
address_udp_receive = (test_pc_ip, test_pc_udp_port)   # ip-address,port of test_pc

## defining the message
messageToSendInit = "begin 15 0 15 0 0 0 end"
messageToSendCommand = "begin 16 0 15 0 0 0 end"

const_echoback_address = test_pc_ip+":"+str(test_pc_udp_port)

address_file_write1 =('./results/qosAnalysis/data_received.txt')
address_file_write = ('./results/qosAnalysis/data_send.txt')


def send(q):
    # initialization
    address_tx = address_udp_send
    address_tx_file = address_file_write;
    
    obj_tx = transfers.udp.init_tx(address_tx)
    obj_tx_file = transfers.file.init_tx(address_tx_file)
    
    global messageToSend
    for seq in range(100000,(100000+const_ping_count)):        	
        for i in list(list_tp):	    		

	    ## set initial position
      	    time.sleep(const_interpkt_delay_ms/1000.0)           				# inter delay     			
	    msg = messageToSendInit 
            transfers.udp.send(obj_tx,msg,address_tx) 

	    ## send command	
	    msg = messageToSendCommand	
	    time.sleep(const_interpkt_delay_ms/1000.0)           				# inter delay     	
            tp = i
            msgHeader = "ping seq:"+str(seq)+" "+"ip:"+const_echoback_address+" "+"tp:"+tp+" " 	# ping header
	    msg = msgHeader + msg		 						# actual-message
            transfers.udp.send(obj_tx,msg,address_tx)        
            time1 = '{0:6f}'.format(time.time())
            msg = "time_send:"+time1 + " " + msg       
            transfers.file.send(obj_tx_file,msg,address_tx_file)
        
    print "send_completed"
    
    transfers.udp.close(obj_tx)
    transfers.file.close(obj_tx_file)
    return
    
def receive(q):
    # initialization
    
    address_rx = ("0.0.0.0", test_pc_udp_port)
    address_tx_file = address_file_write1;
    
    obj_rx = transfers.udp.init_rx(address_rx)
    obj_tx_file = transfers.file.init_tx(address_tx_file)
    
    var_done_counter = 0;
    flag = 0;
    while(1):
        msg = transfers.udp.receive(obj_rx)

	if(msg=="timeout"):
		break

        print "<<",msg
        time1 = '{0:6f}'.format(time.time())
        msg = "time_received:"+time1+" "+msg
        transfers.file.send(obj_tx_file,msg,address_tx_file)
                  
    print "receive_completed"
   
    transfers.udp.close(obj_rx)
    transfers.file.close(obj_tx_file)
    q.put("kill") #terminate command
    return

### multiprocessing
if __name__ == '__main__':
    	q = Queue()
	p1 = multiprocessing.Process(target=send,args=(q,))
	p2 = multiprocessing.Process(target=receive,args=(q,))

	p1.start()
	p2.start()
    
    	#q.put(0)
    
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


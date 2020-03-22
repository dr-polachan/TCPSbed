#!/usr/bin/env python
import os, sys
import sys
import time
import vrep
import numpy as np

lib_path = os.path.abspath(os.path.join(__file__,'..','..'))	
sys.path.append(lib_path)


import transfers.rev1 as transfers
import codec.generic
import algorithms.test.ping as ping

execfile("./src/server_settings.py")

### Connecting to vRep
vrep.simxFinish(-1)
clientID=vrep.simxStart('127.0.0.1',19996,True,True,5000,5) # Connect to V-REP
if clientID!=-1:
    print ('Connected to remote API server')
else:
    print ('Connection not Established')
    sys.exit('error could not connect')  

### Getting a Handle for the Joint 
errorcode, jointHandle_1 = vrep.simxGetObjectHandle(clientID,'PhantomXPincher_joint1',vrep.simx_opmode_blocking)
errorcode, jointHandle_2 = vrep.simxGetObjectHandle(clientID,'PhantomXPincher_joint2',vrep.simx_opmode_blocking)
errorcode, jointHandle_3 = vrep.simxGetObjectHandle(clientID,'PhantomXPincher_joint3',vrep.simx_opmode_blocking)
errorcode, jointHandle_4 = vrep.simxGetObjectHandle(clientID,'PhantomXPincher_joint4',vrep.simx_opmode_blocking)

### forward flow engine
def vrepControl(): 
    
    dataForce = 0

    ### defining in/out address/mode
    address_rx = (ss_embsys_app_ip, kin_link_3)
    address_tx = (ss_com_ip, hap_link_0)    
    mode_rx = "udp"
    mode_tx = "udp"
    
    ### initialization    
    obj_rx = transfers.init_rx(address_rx,mode_rx)	
    obj_tx = transfers.init_tx(address_tx,mode_tx)

    
    while (1):
        print "vrepControl",time.time()
        
        ### receive message
        msg = transfers.receive(obj_rx) 
        ping.echo_back(msg,"tpf_ss_embsys_entry") #ss_embsys tp's               
        
   	### decode message
	msg_list = codec.generic.decode(msg) 
	print msg_list
	
	### moving actuators
	msg_list = map(int, msg_list)
	print "received", msg_list

	jointAngle1 = msg_list[0]
	jointAngle2 = msg_list[1]
	jointAngle3 = msg_list[2]
	jointAngle4 = msg_list[3]
	gripperPosition = msg_list[4] #0-100, Full Close=0, Full Open = 100

	errorcode = vrep.simxSetJointTargetPosition(clientID,jointHandle_1, jointAngle1*3.14/180, vrep.simx_opmode_streaming)
	errorcode = vrep.simxSetJointTargetPosition(clientID,jointHandle_2, jointAngle2*3.14/180, vrep.simx_opmode_streaming)
	errorcode = vrep.simxSetJointTargetPosition(clientID,jointHandle_3, jointAngle3*3.14/180, vrep.simx_opmode_streaming)
	errorcode = vrep.simxSetJointTargetPosition(clientID,jointHandle_4, jointAngle4*3.14/180, vrep.simx_opmode_streaming)
	errorcode = vrep.simxSetIntegerSignal(clientID,'PhantomXPincher_gripperClose',gripperPosition,vrep.simx_opmode_oneshot)
	
	### reading haptic data
	[errorcode, dataForce] = vrep.simxGetJointForce(clientID,jointHandle_4,vrep.simx_opmode_streaming)
	dataForce = -1*dataForce

	### Restricting pressure between 0 and 100
	if(dataForce < 0):
		dataForce = 0
	if(dataForce > 100):
		dataForce = 100

	dataForce = int(100*dataForce)
	

        print "force", dataForce

	### coding haptic data
	msg_list = [dataForce]
        msg = codec.generic.codev2(msg,msg_list)
	        
        ### send the message
    	transfers.send(obj_tx,msg)
        ping.echo_back(msg,"tpf_ss_embsys_exit")
	          
    transfers.close(obj_tx)
    transfers.close(obj_rx)

    return

if __name__ == '__main__':
    vrepControl()

import time
import lib_vrep.vrep as vrep
import os, sys
import numpy as np
lib_path = os.path.abspath(os.path.join(__file__,'..','..'))	
sys.path.append(lib_path)
import transfers.rev1 as transfers
import codec.generic

execfile("./src/global_settings.py")

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

### initialization
obj_file = open('./results/edge-experiments/data.txt', 'w')
string = "time"+","+"data"+"\n"
obj_file.write(string) 

def vrepControl(): 

	### defining in/out address/mode
	address_rx = (ss_embsys_app_ip, kin_link_4)
	address_tx = (ss_com_ip, hap_link_0)    
	mode_rx = "udp"
	mode_tx = "udp"

	### initialization    
	obj_rx = transfers.init_rx(address_rx,mode_rx)	
	obj_tx = transfers.init_tx(address_tx,mode_tx)

	count = 0
	while (1):
		count = count + 1
		print "vrep-control",time.time()

		### receive message
		msg = transfers.receive(obj_rx) 

		### decode message
		msg_list = codec.generic.decode(msg) 

		### moving actuators
		try:
			msg_list = map(float, msg_list)
		except:
			continue

		jointAngle1 = msg_list[0]
		jointAngle2 = msg_list[1]
		jointAngle3 = msg_list[2]
		jointAngle4 = msg_list[3]
		gripperPosition = int(msg_list[4]) #Full Close=0, Full Open = 100

		errorcode = vrep.simxSetJointTargetPosition(clientID,jointHandle_1, jointAngle1*3.14/180, vrep.simx_opmode_streaming)
		errorcode = vrep.simxSetJointTargetPosition(clientID,jointHandle_2, jointAngle2*3.14/180, vrep.simx_opmode_streaming)
		errorcode = vrep.simxSetJointTargetPosition(clientID,jointHandle_3, jointAngle3*3.14/180, vrep.simx_opmode_streaming)
		errorcode = vrep.simxSetJointTargetPosition(clientID,jointHandle_4, jointAngle4*3.14/180, vrep.simx_opmode_streaming)
		errorcode = vrep.simxSetIntegerSignal(clientID,'PhantomXPincher_gripperClose',gripperPosition,vrep.simx_opmode_oneshot)

		[errorcode, gripperPosRead] = vrep.simxGetIntegerSignal(clientID,'PhantomXPincher_gripperClose',vrep.simx_opmode_oneshot)

		### store and save gripper position
		string = str('{0:6f}'.format(time.time()))+","+str(gripperPosRead)+"\n"
		obj_file.write(string) #time,gripper-position

		if(count > 25):
			print "closing applciation"
			obj_file.close()
			break

		### reading haptic data
		[errorcode, dataForce] = vrep.simxGetJointForce(clientID,jointHandle_4,vrep.simx_opmode_streaming)
		dataForce = int(np.clip(-100*dataForce,0,100))

		### coding haptic data
		msg_list = [dataForce]
		msg = codec.generic.code(msg_list)

		### send the message
		transfers.send(obj_tx,msg)

if __name__ == '__main__':
    vrepControl()

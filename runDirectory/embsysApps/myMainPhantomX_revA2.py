# -*- coding: utf-8 -*-
"""
Created on Mon May 16 16:33:35 2016

@author: kpol
"""

import vrep
import sys
import time

vrep.simxFinish(-1)
clientID=vrep.simxStart('127.0.0.1',19996,True,True,5000,5) # Connect to V-REP
if clientID!=-1:
    print ('Connected to remote API server')
else:
    print ('Connection not Established')
    sys.exit('error could not connect')  

# Getting a Handle for the Joint 
errorcode, jointHandle_1 = vrep.simxGetObjectHandle(clientID,'PhantomXPincher_joint1',vrep.simx_opmode_blocking)
errorcode, jointHandle_2 = vrep.simxGetObjectHandle(clientID,'PhantomXPincher_joint2',vrep.simx_opmode_blocking)
errorcode, jointHandle_3 = vrep.simxGetObjectHandle(clientID,'PhantomXPincher_joint3',vrep.simx_opmode_blocking)
errorcode, jointHandle_4 = vrep.simxGetObjectHandle(clientID,'PhantomXPincher_joint4',vrep.simx_opmode_blocking)

#errorcode, jointHandle_5 = vrep.simxGetObjectHandle(clientID,'PhantomXPincher_gripperCenter_joint',vrep.simx_opmode_blocking)
#errorcode, jointHandle_6 = vrep.simxGetObjectHandle(clientID,'PhantomXPincher_gripperClose_joint',vrep.simx_opmode_blocking)

# moving the objects
## initial position

jointAngle1 = 20
jointAngle2 = 10
jointAngle3 = 10
jointAngle4 = 10
gripperPosition = 25 #0-100, Full Close=0, Full Open = 100


errorcode = vrep.simxSetJointTargetPosition(clientID,jointHandle_1, jointAngle1*3.14/180, vrep.simx_opmode_streaming)
errorcode = vrep.simxSetJointTargetPosition(clientID,jointHandle_2, jointAngle2*3.14/180, vrep.simx_opmode_streaming)
errorcode = vrep.simxSetJointTargetPosition(clientID,jointHandle_3, jointAngle3*3.14/180, vrep.simx_opmode_streaming)
errorcode = vrep.simxSetJointTargetPosition(clientID,jointHandle_4, jointAngle4*3.14/180, vrep.simx_opmode_streaming)
#errorcode = vrep.simxSetJointTargetPosition(clientID,jointHandle_5, jointAngle5, vrep.simx_opmode_streaming)
#errorcode = vrep.simxSetJointTargetPosition(clientID,jointHandle_6, jointAngle6, vrep.simx_opmode_streaming)
errorcode = vrep.simxSetIntegerSignal(clientID,'PhantomXPincher_gripperClose',gripperPosition,vrep.simx_opmode_oneshot)





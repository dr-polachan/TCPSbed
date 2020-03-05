### Importing Modules
from __future__ import division
import numpy as np
from numpy import linalg as LA
import math

from algorithms.kinematics.hapticGloveLib.imu import classIMU as classIMU

obj1 = classIMU()
obj1.magnetometerCalibrationParameterSet([205,-50,116,-10,40,-205]) #[mxMax, mxMin, myMax, myMin, mzMax, mzMin]

obj2 = classIMU()
obj2.magnetometerCalibrationParameterSet([200,-50,110,-100,40,-130]) #[mxMax, mxMin, myMax, myMin, mzMax, mzMin]

global msgListPrevious
msgListPrevious = [1188, 3365, 14192, -52, 45, -89, -16, 188, -90, 1188, 3365, 14192, -52, 45, -89, -16, 188, -90]

def rev1 (msgList): 
    global msgListPrevious

    ## Step-1: Retreiving data from glove
    try:	
	msgList = map(int, msgList)
	msgListPrevious = msgList
    except: 
	msgList = msgListPrevious

    ## Step-2 finding DCM myDCM_utog, orientation of user frame axis w.r.t global frame axis
    myDCM_utog = obj1.computeDCM_utog(msgList[0:9])	
     
    myDCM_ctog_1 = obj1.computeDCM_ctog(msgList[0:9])
    myDCM_ctog_2 = obj2.computeDCM_ctog(msgList[9:])
    myDCM_ctog_2 = myDCM_ctog_1.copy()
 
    myUpperArm_chipframe_pos = [10,0,0]  #in chip frame axes w.r.t shoulder joint as (0,0,0)
    myLowerArm_chipframe_pos = [10,0,0]  #in chip frame axes w.r.t elbow joint as (0,0,0)

    myUpperArm_globalframe_pos = np.matmul(myDCM_ctog_1, myUpperArm_chipframe_pos)
    myLowerArm_globalframe_pos = np.matmul(myDCM_ctog_2, myLowerArm_chipframe_pos)

    myWristPosition = np.add(myUpperArm_globalframe_pos,myLowerArm_globalframe_pos)

    myWristPosition_userframe = np.matmul(myDCM_utog.transpose(), myWristPosition)
    myWristPosition_userframe = np.round(myWristPosition_userframe, 3)

	
    [wristX, wristY, wristZ] = 	myWristPosition_userframe
    palmPitch = 0
    palmPincher = 0
    result = [wristX, wristY, wristZ, palmPitch, palmPincher]
		          			    
    return (result) 

def bypass (msg_list):

    return (msg_list)



    
   

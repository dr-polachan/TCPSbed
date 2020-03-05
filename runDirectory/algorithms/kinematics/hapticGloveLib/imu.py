### Importing Modules

from __future__ import division

import numpy as np

from numpy import linalg as LA
import math



## class for imu dcm computation
class classIMU:
    def __init__(self):
	self.mxmax = 205.0
	self.mxmin = -50.0
	self.mymax = 116.0
	self.mymin = -10.0
	self.mzmax = 40.0
	self.mzmin = -205.0

	self.dcm = np.identity(3)
	self.dcm_utog = np.identity(3)

	self.fScaleA = 0.02
	self.fScaleG = 0.96
	self.fScaleM = 0.02

	self.flagFirstIterationDone = 0

	self.deltat = 10e-3

	self.counterUtoGCompute = 0

    def magnetometerCalibrationParameterSet(self, parameters):
	
	[mxMax, mxMin, myMax, myMin, mzMax, mzMin] = parameters

	self.mxmax = mxMax
	self.mxmin = mxMin
	self.mymax = myMax
	self.mymin = myMin
	self.mzmax = mzMax
	self.mzmin = mzMin	

    	return ()

    def magnetometerCalibration(self, mag):
        
	[magX, magY, magZ] = np.array(mag)

	mxmax = self.mxmax
	mxmin = self.mxmin
	mxavg = (mxmax + mxmin)/2
	mymax = self.mymax
	mymin = self.mymin
	myavg = (mymax + mymin)/2
	mzmax = self.mzmax
	mzmin = self.mzmin
	mzavg = (mzmax + mzmin)/2

	mxhic = magX - mxavg
	myhic = magY - myavg
	mzhic = magZ - mzavg

	mxdif = mxmax - mxmin
	mydif = mymax - mymin
	mzdif = mzmax - mzmin

	mdifavg = (mxdif + mydif + mzdif)/3

	mxscale = mdifavg/mxdif
	myscale = mdifavg/mydif
	mzscale = mdifavg/mzdif

	mxfin = mxhic*mxscale
	myfin = myhic*myscale
	mzfin = mzhic*mzscale

	magCalibX = mxfin
	magCalibY = myfin
	magCalibZ = mzfin

	## calibrating axis
	magOut = [magCalibY, magCalibX, magCalibZ*-1]

        return ( magOut )
    
    def accelerometerCalibration(self, acc):

	[aX, aY, aZ] = np.array(acc)

	#[aCalibX, aCalibY, aCalibZ] = [aX*-1, aY*-1,aZ*-1]
	#[aCalibX, aCalibY, aCalibZ] = [aX, aY, -aZ]
	[aCalibX, aCalibY, aCalibZ] = [aX, aY, aZ]
        
        return ( [aCalibX, aCalibY, aCalibZ] )

    def gyroscopeCalibration(self, gyro):
	
	gyro = np.array(gyro)
        gyro = gyro.astype(np.float)

	gyroCalib = 1.3323124e-4*gyro	

	[gCalibX, gCalibY, gCalibZ] = gyroCalib
        
	return ( [gCalibX, gCalibY, gCalibZ] )

    def findDCMrevKPOL(self, msgList):
 	
	myReadingAccelerometer = msgList[0:3]
	myReadingMagnetometer = msgList[3:6]
	myReadingGyro = msgList[6:9]
	
	myDCM = self.dcm
   
	### init values
	myAngleScale_A = self.fScaleA
	myAngleScale_G = self.fScaleG
	myAngleScale_M = self.fScaleM

	myDeltaT = self.deltat

	### computing DCM
	I = myReadingMagnetometer
	K = myReadingAccelerometer

	#print "my", I

	J = np.cross(K, I) # J=KxI
	I = np.cross(J, K) # orthogonalise vector I wrt K&J to null the measurement error

	#normalizing the I,J, K vectors
	I = I/LA.norm(I, axis=0) 
	K = K/LA.norm(K, axis=0)
	J = J/LA.norm(J, axis=0)

	if(self.flagFirstIterationDone == 0):
		self.flagFirstIterationDone = 0
		myDCM[0][:] = I  #magnetometer
		myDCM[1][:] = J  #J=KxI
		myDCM[2][:] = K  #accelerometer


	elif (self.flagFirstIterationDone == 1):

		print "my",I
		dtheta_A = np.cross(myDCM[2][:], K) #angle with which K is moving
		dtheta_M = np.cross(myDCM[0][:], I) #angle with which I is moving

		dtheta_G = np.array([myReadingGyro[0]*myDeltaT, myReadingGyro[1]*myDeltaT, myReadingGyro[2]*myDeltaT])

		# adding the scaled dtheta's
		dtheta = np.add(dtheta_M*myAngleScale_M,dtheta_A*myAngleScale_A)
		dtheta = np.add(dtheta, dtheta_G*myAngleScale_G)

		print "Angles",dtheta_A, dtheta_M, dtheta_G
		print "Angle" ,dtheta

		dI = np.cross(dtheta,myDCM[0][:])
		#print "dI",dI
		I = np.add(myDCM[0][:],dI) #ps:magnitude of I now is not 1
		#print "I",I

		dK = np.cross(dtheta,myDCM[2][:])
		K = np.add(myDCM[2][:],dK)
		#print "K",K

		J = np.cross(K, I) # J=KxI
		
		#method-2 (see mtech report)
		I1 = np.cross(J,K)
		Error = I1-I #I+Error = I1
		Error = Error*0.5
		I = np.add(I,Error)
		K = np.add(K,Error)

		#normalizing the I,J, K vectors
		I = I/LA.norm(I, axis=0) 
		K = K/LA.norm(K, axis=0)
		J = J/LA.norm(J, axis=0)

		myDCM[0][:] = I  
		myDCM[1][:] = J  
		myDCM[2][:] = K  

	self.dcm = myDCM
	return ()


    def findDCM(self, msgList):
	
	accel=np.zeros(3)
 	gyro=np.zeros(3)
	mag=np.zeros(3) 

	I=mag
	J=gyro
	K=accel

	accel = msgList[0:3]
	mag = msgList[3:6]
	gyro = msgList[6:9]

	dcm = self.dcm

	if (self.flagFirstIterationDone == 0):

		self.flagFirstIterationDone = 0 

		for i in range(len(accel)):
			I[i] = mag[i]
			K[i] = accel[i] 

		#crossproduct of I and K to get J
		J = np.cross(K, I) 

		#orthogonalise vector I wrt K&J
		I = np.cross(J, K)

		#normalizing the I,K vectors
		try:
			I = I/LA.norm(I, axis=0) 
			K = K/LA.norm(K, axis=0)
			J = J/LA.norm(J, axis=0)
		

			self.dcm[0]=I
			self.dcm[1]=J
			self.dcm[2]=K

		except:
			self.dcm = self.dcm

	if (self.flagFirstIterationDone == 1):

		#print"code is entering flag 1 of dcmcompute function"
		for i in range(len(accel)):
			I[i] = mag[i]
			K[i] = accel[i] 

		#crossproduct of I and K to get J
		J = np.cross(K, I) 

		#orthogonalise vector I wrt K&J
		I = np.cross(J, K)

		#normalizing the I,K vectors
		I = I/LA.norm(I, axis=0) 
		J = J/LA.norm(J, axis=0)
		K = K/LA.norm(K, axis=0)

		#compute the rotn and scale as inferred from accel
		temp = np.cross(dcm[2][:], K)
		delta = temp*self.fScaleA

		#print "deltaA", self.dcm[2]

		#compute the rotn and scale as inferred from gyro
		temp[0] = gyro[0]*self.deltat*self.fScaleG
		temp[1] = gyro[1]*self.deltat*self.fScaleG
		temp[2] = gyro[2]*self.deltat*self.fScaleG


		delta = np.add(delta, temp)

		#compute the rotn and scale as inferred from magneto
		temp = np.cross(dcm[0][:], I)
		temp = temp*self.fScaleM

		delta = np.add(delta, temp)

		#rotating the I vector from the DCM matrix by th escaled direction
		I = np.cross(delta, dcm[0])
		dcm[0] = np.add(dcm[0], I)

		#rotating the K vector from the DCM matrix by the escalated direction
		K = np.cross(delta, dcm[2])
		dcm[2] = np.add(dcm[2], K)

		#calculte orthogonality error
		fError = np.dot(dcm[0], dcm[2])/(-2)
		I = np.add(dcm[0],dcm[2]*fError)
		K = np.add(dcm[2],dcm[0]*fError)

		#calculating new I and K vectors afer incorporating the errors
		dcm[0] = I
		dcm[2] = K

		#normalising the derived vectors
		dcm[0] = dcm[0]/LA.norm(dcm[0], axis=0) 
		dcm[2] = dcm[2]/LA.norm(dcm[2], axis=0)

		#computing the J vector
		dcm[1] = np.cross(dcm[2], dcm[0])

	self.dcm = dcm
	
	return()

    def computeDCM_ctog(self, msgList):

	## accelerometer calibration
	msgList[0:3] = self.accelerometerCalibration(msgList[0:3])	

	## magnetometer calibration        
	msgList[3:6] = self.magnetometerCalibration(msgList[3:6])	

	## gyro calibration
	msgList[6:9] = self.gyroscopeCalibration(msgList[6:9])

	## finding the DCM
	self.findDCM(msgList) # this updates self.dcm
	#self.findDCMrevKPOL(msgList)

	## return value
	ret = self.dcm
	ret = np.round(ret,3)

        return (ret)


    def computeDCM_utog(self, msgList):

	if(self.counterUtoGCompute < 100):

		self.counterUtoGCompute += 1
		
		print "counter:", self.counterUtoGCompute
	
		## accelerometer calibration
		msgList[0:3] = self.accelerometerCalibration(msgList[0:3])	

		## magnetometer calibration        
		msgList[3:6] = self.magnetometerCalibration(msgList[3:6])	

		## gyro calibration
		msgList[6:9] = self.gyroscopeCalibration(msgList[6:9])

		## finding the DCM
		self.findDCM(msgList) # this updates self.dcm
		#self.findDCMrevKPOL(msgList)

		## copy the dcm to dcm_utog
		self.dcm_utog = self.dcm.copy()

		## return value
		ret = self.dcm_utog
		ret = np.round(ret,3)

	else:
		ret = self.dcm_utog
		ret = np.round(ret,3)

	return (ret)


    
   

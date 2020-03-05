import random

class eISlaveSide:
    def __init__(self):
	self.msgKinematicPrevious = "NaN"
	self.msgHapticPrevious = "NaN"
	self.msgKinematic = "NaN"
	self.msgHaptic = "NaN"
	self.sequenceNo = random.randint(100000,200000)
	self.dupPktCount = 0
	self.dupPktThreshold = 3
	
    def read(self, parameters): # parameters = [queueKinematic,queueHaptic,queueAudio,queueVideo]
	[queueKinematic,queueHaptic,queueAudio,queueVideo] = parameters

	##1 Outward Flow [Haptic]
	try: 
		## reading data
		self.msgHaptic = queueHaptic.get(False)

		## appending sequence number 
		self.msgHaptic = "seq:"+str(self.sequenceNo)+" "+self.msgHaptic
		self.sequenceNo += 1
		self.dupPktCount = 0

	except:
		## restoring from old sample
		self.msgHaptic = self.msgHapticPrevious
	
	##2 Inward Flow [Kinematic flow]	
	try: 
		## reading data
		self.msgKinematic = queueKinematic.get(False)

	except:
		## restoring from old sample
		self.msgKinematic = self.msgKinematic	

	return(self.msgKinematic, self.msgHaptic)

    def edgeIntelligenceRev1(self): 
	
	##1 edgeIntelligence for haptic flow
	self.dupPktCount += 1	
	if(self.dupPktCount <= self.dupPktThreshold):
		self.msgHapticPrevious = self.msgHaptic		

	else:
		self.msgHaptic = "NaN"

	##2 edgeIntelligence for kinematic flow
	if(self.msgKinematic == self.msgKinematicPrevious):
		self.msgKinematic = "NaN"
	else:
		self.msgKinematicPrevious = self.msgKinematic
		
	return(self.msgKinematic, self.msgHaptic)


class eIMasterSide:
    def __init__(self):
	self.msgKinematicPrevious = "NaN"
	self.msgHapticPrevious = "NaN"
	self.msgKinematic = "NaN"
	self.msgHaptic = "NaN"
	self.sequenceNo = random.randint(100000,200000)
	self.sequenceNoPrevious = self.sequenceNo
	self.dupPktCount = 0
	self.dupPktThreshold = 3

    def read(self, parameters): # parameters = [queueKinematic,queueHaptic,queueAudio,queueVideo]
	[queueKinematic,queueHaptic,queueAudio,queueVideo] = parameters

	##1 Outward Flow [kinematic]
	try: 
		## reading data		
		self.msgKinematic = queueKinematic.get(False)

		## appending sequence number 
		self.msgKinematic = "seq:"+str(self.sequenceNo)+" "+self.msgKinematic
		self.sequenceNo += 1
		self.dupPktCount = 0

	except:
		## restoring from old sample
		self.msgKinematic = self.msgKinematicPrevious
	
	##2 Inward Flow [haptic flow]	
	try: 
		## reading data
		self.msgHaptic = queueHaptic.get(False)

	except:
		## restoring from old sample
		self.msgHaptic = self.msgHapticPrevious	

	return(self.msgKinematic, self.msgHaptic)

    def edgeIntelligenceRev1(self): 
	
	##1 edgeIntelligence for kinematic flow
	self.dupPktCount += 1	
	if(self.dupPktCount <= self.dupPktThreshold):
		self.msgKinematicPrevious = self.msgKinematic		

	else:
		self.msgKinematic = "NaN"

	##2 edgeIntelligence for haptic flow
	if(self.msgHaptic == self.msgHapticPrevious):
		self.msgHaptic = "NaN"
	else:
		self.msgHapticPrevious = self.msgHaptic
		
	return(self.msgKinematic, self.msgHaptic)

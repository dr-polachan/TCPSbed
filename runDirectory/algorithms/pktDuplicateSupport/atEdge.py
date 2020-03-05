import random
import transfers1.rev1 as transfers
from time import sleep

class pktDuplicateClass:
    def __init__(self):
	
	self.VarDupPktThreshold = 0
	self.VarDupPktInterval = 0
	self.sequenceNo = random.randint(100000,200000)

	self.msgPrevious = "NaN"

    def send(self, obj_tx, msg):
	msg = "seq:"+str(self.sequenceNo)+" "+ msg
	self.sequenceNo += 1		

	for i in range(self.VarDupPktThreshold):	
		transfers.send(obj_tx,msg);
		sleep(self.VarDupPktInterval)
	
	return

    def receive(self, obj_rx):
	while(1):
	
		msg = transfers.receive(obj_rx)
		if (msg != self.msgPrevious):
			self.msgPrevious = msg
			return(msg)

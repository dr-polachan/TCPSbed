from __future__ import division
import numpy as np
import time

class predict:

	def __init__(self):

		self.msg_kinematic_list_old = ["NaN"] 
		self.time_old = 0
		self.slope_n = 0

	def run(self, msg_kinematic_list, msg_haptic_list): 

		if(msg_kinematic_list != ["NaN"]):
			self.msg_kinematic_list_old = msg_kinematic_list
		else:
			msg_kinematic_list = self.msg_kinematic_list_old	

		return (msg_kinematic_list) 
	
	def linear(self, msg_kinematic_list):

		msg = msg_kinematic_list

		if(msg_kinematic_list == ["NaN"]):
			# we need to predict the message

			if(self.msg_kinematic_list_old != ["NaN"]):
				msg_kinematic_list = self.msg_kinematic_list_old + self.slope_n*(time.time()-self.time_old)
			else:
				msg_kinematic_list = self.msg_kinematic_list_old

		else:

			self.msg_kinematic_list_old = msg_kinematic_list
			self.time_old = time.time()

			if(self.msg_kinematic_list_old != ["NaN"]):
				dt = 100e-3

				# figure out wave velocity
				msg_kinematic_list = map(float,msg_kinematic_list)
				self.msg_kinematic_list_old = map(float,self.msg_kinematic_list_old)
				self.slope_n = np.array(msg_kinematic_list) - np.array(self.msg_kinematic_list_old)
				self.slope_n = self.slope_n/dt

				# figure out wave accelearation
				#self.slope_n_minus_1 = np.array(self.msg_kinematic_list_old) - np.array(self.msg_kinematic_list_old_old)
				#self.slope_n_minus_1 = self.slope_n_minus_1/dt

		return(msg_kinematic_list)
	




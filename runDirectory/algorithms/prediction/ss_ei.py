from __future__ import division


class predict:

	def __init__(self):

		self.msg_kinematic_list_old = ["NaN"] 

	def run(self, msg_kinematic_list, msg_haptic_list): 

		if(msg_kinematic_list != ["NaN"]):
			self.msg_kinematic_list_old = msg_kinematic_list
		else:
			msg_kinematic_list = self.msg_kinematic_list_old	

		return (msg_kinematic_list) 





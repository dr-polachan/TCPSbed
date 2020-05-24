from __future__ import division


class predict:

	def __init__(self):

		self.msg_haptic_list_old = ["NaN"] 

	def run(self, msg_haptic_list, msg_kinematic_list): 

		if(msg_haptic_list != ["NaN"]):
			self.msg_haptic_list_old = msg_haptic_list
		else:
			msg_haptic_list = self.msg_haptic_list_old	

		return (msg_haptic_list)





from __future__ import division


class predict:

  def __init__(self):
    
    self.msg_list_old = ["NaN"] 

  def run(self,msg_list, haptic_list): 
    
    if(msg_list != ["NaN"]):
	self.msg_list_old = msg_list
    else:
	msg_list = self.msg_list_old	
    
    return (msg_list) 





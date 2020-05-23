import multiprocessing 
import time
import sys

execfile("./src/ms_com_settings.py")
execfile("./src/ms_com_fwd_kinematic.py")
execfile("./src/ms_com_bwd_haptic.py")

if __name__ == '__main__':

    	f1 = multiprocessing.Process(target=forward_flow_kinematic)
    	b1 = multiprocessing.Process(target=backward_flow_haptic)

	if(en_kinematic_link):	
		f1.start()    
	if(en_haptic_link):
    		b1.start()
	

	

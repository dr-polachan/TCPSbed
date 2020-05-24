import multiprocessing 
import time
import sys

execfile("./src/ms_ei_settings.py")
execfile("./src/ms_ei_bwd_haptic.py")

if __name__ == '__main__':

    	f1 = multiprocessing.Process(target=backward_flow_haptic) 	
	if(en_haptic_link):	
		f1.start()    




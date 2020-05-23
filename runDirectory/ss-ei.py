import multiprocessing 
import time
import sys

execfile("./src/ss_ei_settings.py")
execfile("./src/ss_ei_fwd_kinematic.py")

if __name__ == '__main__':

    	f1 = multiprocessing.Process(target=forward_flow_kinematic) 	
	if(en_kinematic_link):	
		f1.start()    




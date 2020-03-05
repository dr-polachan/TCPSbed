#!/usr/bin/env python

import multiprocessing 
import time
import sys

# load files
execfile("./src/server_settings.py")
execfile("./src/server_fwd_kinematic.py")
execfile("./src/server_bwd_haptic.py")
execfile("./src/server_bwd_video.py")
execfile("./src/server_bwd_audio.py")
execfile("./src/server_bwd_ping.py")

### multiprocessing
if __name__ == '__main__':
	# fwd channel
    	f1 = multiprocessing.Process(target=forward_flow_kinematic)
	# backward channel
    	b1 = multiprocessing.Process(target=backward_flow_haptic)    
	b2 = multiprocessing.Process(target=backward_flow_video)
	b3 = multiprocessing.Process(target=backward_flow_audio)
	b4 = multiprocessing.Process(target=backward_flow_ping)

	if(en_kinematic_link):	
		f1.start()    
	if(en_haptic_link):
    		b1.start()
	if(en_video_link):
		b2.start()
	if(en_audio_link):
		b3.start()
	b4.start()

	while(1):
		time.sleep(10)
    
	f1.terminate()
    	b1.terminate()
        b2.terminate()
	b3.terminate()
	b4.terminate()

	f1.join()
    	b1.join()
       	b2.join()
	b3.join()
	b4.join()
    
	print 'DONE !!!'

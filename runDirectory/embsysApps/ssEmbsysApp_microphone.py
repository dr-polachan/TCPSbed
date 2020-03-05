#!/usr/bin/env python


import os, sys
lib_path = os.path.abspath(os.path.join(__file__,'..','..'))	
sys.path.append(lib_path)

import codec.generic
#import codec.audiovideo
import codec.audio

import transfers1.rev1 as transfers

#import test.ping
import time
import pyaudio

execfile("server_settings.py")


### forward flow engine
def audio_input():    
    ### defining in/out address/mode
    address_rx = ("NaN", "NaN")
    address_tx = (ss_embsys_app_ip, audio_link_0)    
    mode_rx = "microphone"
    mode_tx = "udp"
    
    ### initialization
    obj_tx = transfers.init_tx(address_tx,mode_tx)
    obj_rx = transfers.init_rx(address_rx,mode_rx)
    
    while (1):
    #for myvar in range (2):
        print "live_embsys_app_microphone_bwd_audio",time.time()
	
	## receiving data from microphone
	msg = transfers.receive(obj_rx)           

    	## encode the message
    	msg = codec.audio.code(msg)
                
	## send the message
    	transfers.send(obj_tx,msg)
	          
    transfers.close(obj_tx)
    transfers.close(obj_rx)
    return


if __name__ == '__main__':
    audio_input()

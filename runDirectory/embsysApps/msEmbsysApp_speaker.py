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
def audio_output():    
    ### defining in/out address/mode
    address_rx = (ms_embsys_app_ip,audio_link_3) #0.0.0.0 works for linux and windows    
    mode_rx = "udp"
    
    ### initialization    
    obj_rx = transfers.init_rx(address_rx,mode_rx) 
    obj_tx = transfers.init_tx(("NaN","NaN"),"microphone")

    #p1 = pyaudio.PyAudio()
    #stream1 = p1.open(format=pyaudio.paInt16,
    #            channels=2,
    #            rate=44100,
    #            output=True,
    #            frames_per_buffer=1024)
    
    while (1):
    #for myvar in range (2):        
        print "live_embsys_audio",time.time()
        
        ### receive message
        msg = transfers.receive(obj_rx)        

        ### decode
        msg = codec.audio.decode(msg)        
        
        ### stream to speaker
	transfers.send(obj_tx,msg)        
	#stream1.write(msg)
        
    transfers.close(obj_rx)
    transfers.close(obj_tx)
    #stream1.close()
    #p1.terminate()
    return

if __name__ == '__main__':
    audio_output()

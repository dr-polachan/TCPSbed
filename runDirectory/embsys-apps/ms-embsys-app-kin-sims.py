import os, sys
import numpy as np
import time
import math
lib_path = os.path.abspath(os.path.join(__file__,'..','..'))	
sys.path.append(lib_path)
import transfers.rev1 as transfers
import codec.generic

execfile("./src/global_settings.py")    

if __name__ == '__main__':         

    ### defining in/out address/mode
    address_tx = (ms_com_ip,kin_link_0)
    mode_tx = "udp"

    ### initialization
    obj_tx = transfers.init_tx(address_tx,mode_tx)

    ### initial time
    t_init = time.time()

    while(1):
        print "kin-sims",time.time()

        ### sampling time
        time.sleep(50e-3)

        ### generating kinematic sample
        amp = 30
        freq = 1
        time_now = time.time()-t_init
        arg = 2*math.pi*freq*time_now
        pincher = amp*np.sin(arg)
        msg_list = [16,0,12,0,int(50+pincher)] #(x,y,z,pitch,pincher)
        
        ### encode message
        msg = codec.generic.code(msg_list)

        ### send message
        transfers.send(obj_tx,msg)
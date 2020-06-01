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
        msg_list = [16,0,12,0,int(100)] #(x,y,z,pitch,pincher)
        msg = codec.generic.code(msg_list)
        transfers.send(obj_tx,msg)
        time.sleep(100e-3)
        msg_list = [16,0,12,0,int(0)] #(x,y,z,pitch,pincher)
        msg = codec.generic.code(msg_list)
        transfers.send(obj_tx,msg)
        time.sleep(100e-3)

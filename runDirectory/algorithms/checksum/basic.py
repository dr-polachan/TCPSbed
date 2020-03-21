### Importing Modules
from __future__ import division

import numpy as np

def rev1 (msg_list):	
    msg_list = map(float, msg_list)

    try:
    	checksum = int(np.sum(msg_list))
    except:
	checksum = 0
    checksum = checksum+1234
    msg_list = msg_list + [checksum,]

    return (msg_list)



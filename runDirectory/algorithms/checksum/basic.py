### Importing Modules
from __future__ import division

import numpy as np

### define checksum (incorporated in PhantomX-controller board)
def rev1 (msg_list):	
    #print "debug111",msg_list
    msg_list = map(float, msg_list)

    try:
    	checksum = int(np.sum(msg_list))
    except:
	checksum = 0
    #print "xyz", checksum
    checksum = checksum+1234
    msg_list = msg_list + [checksum,]
    #print "result", msg_list

    return (msg_list)



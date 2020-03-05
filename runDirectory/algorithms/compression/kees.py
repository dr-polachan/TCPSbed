import kees_lib.kees_lib
    
def encode(msg_list):

    x = float(msg_list[0])
    y = float(msg_list[1])
    z = float(msg_list[2])
    pitch = float(msg_list[3])
    pincher = int(msg_list[4])
    velocity = int(msg_list[5])
    
    msg_list = (x,y,z,pitch,pincher,velocity)
    #print msg_list
    msg_list = kees_lib.kees_lib.encode(msg_list)
          
    return(msg_list)

def decode(msg_list):    
    
    msg_list = kees_lib.kees_lib.decode(msg_list)
                                        
    return(msg_list)

if __name__ == '__main__':
     #sender-receiver in sync
    for i in range(5):
        msg = (10.0, -0.0, 10.0, 0.0, 0.0)
        msg_list = encode(msg)
        print "encode_result",msg_list        
        msg_list = decode(msg_list)                
        print "decode_result",msg_list        

    print ""
    # sender side
    for i in range(5):
        msg = (10.0, -0.0, 10.0, 0.0, 0.0)
        #msg_list = algorithms.compression.kees.encode(msg)
        msg_list = encode(msg)
        print "encode_result",msg_list
        
    print ""
    # receiver side    
    for i in range(5):
        msg = ['10000', '10.0']
        msg_list = decode(msg)
        print "decode_result",msg_list

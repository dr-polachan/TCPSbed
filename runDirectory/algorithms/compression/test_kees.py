import kees_1 #at the sender side

import kees_2   #at the receiver side  

if __name__ == '__main__':
     #sender-receiver in sync
#    for i in range(5):
#        msg = (10.0, -0.0, 10.0, 0.0, 0.0)
#        msg_list = kees_1.encode(msg)
#        print "encode_result",msg_list        
#        msg_list = kees_1.decode(msg_list)                
#        print "decode_result",msg_list        
#
#    print ""
    # sender side
    msg = (10.0, -0.0, 10.0, 0.0, 0.0)
    print "original message", msg
    print ""
    
    for i in range(5):

        #msg_list = algorithms.compression.kees.encode(msg)
        msg_list = kees_1.encode(msg)
        print "encode_result",msg_list
        
    print ""
    # receiver side    
    for i in range(5):
        msg = ['10000', '10.0']
        msg_list = kees_2.decode(msg)
        print "decode_result",msg_list
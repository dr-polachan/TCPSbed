from kees import kees

k_transmit = kees();
k_receive = kees();

k_transmit = kees();
k_receive = kees();

k_transmit.initializeEstimation([0,0,0,0,0,0])
k_receive.initializeEstimation([0,0,0,0,0,0])

def encode(source):
    packet =  k_transmit.prediction_encode(source)
    return(packet)

def decode(packet):
    k_receive.prediction_decode(packet)
    return(k_receive.estimateList)

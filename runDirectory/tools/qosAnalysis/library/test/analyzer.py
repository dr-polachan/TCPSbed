from __future__ import division #float result for division
from numpy import genfromtxt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import math
import pandas as pd

from scipy.stats import norm

def analyze(file_send_data,file_read_data,tp):
    # replace ":" with space
    data_received = np.array([])
    time_received = np.array([])
    with open(file_send_data, 'r') as content_file:
        str = content_file.read()
    str = str.replace(":"," " " ")

    with open("ds.txt", "w") as text_file:
        text_file.write(str)

    with open(file_read_data, 'r') as content_file:
        str = content_file.read()
    str = str.replace(":"," " " ")

    with open("dr.txt", "w") as text_file:
        text_file.write(str)

#    print "...."

    # retreive data (sequence#) and time
    data = genfromtxt(file_send_data)
    data_send = data[:,1]
    time_send = data[:,0]
#    try:
#        data = genfromtxt(file_read_data)
#    except IOError:
#    	data = np.array(([0,0],[0,0]))        
    data = genfromtxt(file_read_data)
    if len(data)==0:
        d = { tp : pd.Series(["NaN","NaN", "NaN", "NaN", "NaN", "NaN", "NaN", "NaN", "NaN", "NaN", "NaN", "NaN", "100"], 
	index=['median latency(ms)', 'avg latency(ms)', 'max latency(ms)', 'min latency(ms)', 'std latency(ms)', 'avg sender interpacket delay(ms)', 'max sender interpacket delay(ms)', 'min sender interpacket delay(ms)', 'std interpacket delay(ms)', 'duplicate packets(%)', 'data send(count)', 'data received(count)', 'packet loss(%)'])}
        df = pd.DataFrame(d)
	return(df)
    
    data_received = data[:,1]
    time_received = data[:,0]

#    print data.ndim
#    print data_received
    # offset correction of time
    temp = time_send - time_send[0];
    temp_ms = temp*1000;
    time_send_corrected = temp_ms #fix to 6 digits

    temp = time_received - time_send[0];
    temp_ms = temp*1000;
    time_received_corrected = temp_ms #fix to 6 digits

    # receiver performance analysis
    latency_ms = np.zeros(data_received.size)
    for i_received in range(data_received.size):

        i_send = np.where(data_send == data_received[i_received])[0][0]
        latency = time_received_corrected[i_received] - time_send_corrected[i_send];
        
        latency_ms[i_received] = latency;
        i_received;
        
    rttby2_ms = latency_ms*0.5;
#    print rttby2_ms
    average_latency_ms = np.mean(rttby2_ms)
    maximum_latency_ms = np.amax(rttby2_ms)
    minimum_latency_ms = np.amin(rttby2_ms)
    sigma_latency_ms = np.std(rttby2_ms)
    
    median_latency_ms = np.median(rttby2_ms)
    
#    print "\nlatency results (ms)>>"
#    print "avg:",average_latency_ms
#    print "max:",maximum_latency_ms
#    print "min:",minimum_latency_ms
#    print "std:",sigma_latency_ms
#    d = {'abc' : pd.Series([average_latency_ms, maximum_latency_ms, minimum_latency_ms, sigma_latency_ms], 
#	index=['avg latency', 'max latency', 'min latency', 'std latency'])}
#    df = pd.DataFrame(d)
#    print df
    # sender performance analysis
    time_send_diff = np.diff(time_send_corrected);
    average_interpacket_delay_ms = np.mean(time_send_diff)
    maximum_interpacket_delay_ms = np.amax(time_send_diff)
    minimum_interpacket_delay_ms = np.amin(time_send_diff)
    sigma_interpacket_delay_ms = np.std(time_send_diff)

#    print "\nsender inter-packet delay (ms)>>"
#    print "avg:",average_interpacket_delay_ms
#    print "max:",maximum_interpacket_delay_ms
#    print "min:",minimum_interpacket_delay_ms
#    print "std:",sigma_interpacket_delay_ms

    # lost/duplicate packets
    row1 = np.unique(data_received).size;
    row2 = data_received.size;
    row3 = data_send.size;
    duplicate_packets_received = row2-row1
    packet_loss = 100-100*((row2-duplicate_packets_received)/row3)
#    print "\nlost/duplicate packets>>"
#    print "duplicate packets:",duplicate_packets_received
#    print "data send:", data_send.size
#    print "data received:",data_received.size
#    print "packet loss(%):",packet_loss
    d = { tp : pd.Series([median_latency_ms, average_latency_ms, maximum_latency_ms, minimum_latency_ms, sigma_latency_ms, average_interpacket_delay_ms, maximum_interpacket_delay_ms, minimum_interpacket_delay_ms, sigma_interpacket_delay_ms, duplicate_packets_received, data_send.size, data_received.size, packet_loss], 
	index=['median latency(ms)','avg latency(ms)', 'max latency(ms)', 'min latency(ms)', 'std latency(ms)', 'avg sender interpacket delay(ms)', 'max sender interpacket delay(ms)', 'min sender interpacket delay(ms)', 'std interpacket delay(ms)', 'duplicate packets(%)', 'data send(count)', 'data received(count)', 'packet loss(%)'])}
    df = pd.DataFrame(d)

    #e = np.random.normal(size=100)  
    #temp = {'latencies(rtt/2)':rttby2_ms}
    #df_raw = pd.Dataframe(temp) #rttby2_ms)


    #np.histogram(rttby2_ms)
    #plt.hist(rttby2_ms,bins=10)
    
    data = rttby2_ms
    #binwidth = .2
    #plt.hist(data, bins=np.arange(min(data), max(data) + binwidth, binwidth))  
    
    #plt.axis([0, 10, 0, 3000])  #first two for x-axis limit, next two for y-axis
    #plt.xlabel("latency (ms)")
    #plt.ylabel('counts (out of 10,000)')
    #plt.show()
    
    # best fit of data
    #(mu, sigma) = norm.fit(data)
#    print "mu:",mu,"sigma:",sigma
    df_data = pd.DataFrame({tp:data.tolist()})
    return(df,df_data)#,df_rawlatencies)
if __name__ == '__main__':
    x = np.linspace(-50,50,1000)
    plt.xlabel("latency (ms)")
    #plt.ylabel('Probability')
    plt.ylabel('Counts')    
    #plt.title('distribution of latency(ms) across test points')
    plt.title('distribution of latency(ms) for tp_embsys_exit')
    
#    file_send_data = './results_srv_entry/data_send.txt'
#    file_read_data = './results_srv_entry/data_received.txt'
#    (mu,sigma) = analyze(file_send_data,file_read_data)
#    mu = round(mu,2)
#    #label_str='srv_entry/1:'+str(mu)
#    plt.plot(x,mlab.normpdf(x,mu,sigma),label='srv_entry @'+str(mu)+"ms")
#    plt.annotate("1", xy=((mu,0)), xytext=(mu,0),
#            arrowprops=dict(facecolor='red', shrink=0.05),
#            )
#    
#        
#    file_send_data = './results_srv_exit/data_send.txt'
#    file_read_data = './results_srv_exit/data_received.txt'
#    (mu,sigma) = analyze(file_send_data,file_read_data)
#    mu_srv_exit = mu
#    mu = round(mu,2)
#    plt.plot(x,mlab.normpdf(x,mu,sigma),label='srv_exit  @'+str(mu)+"ms")
#    plt.annotate("2", xy=((mu,0)), xytext=(mu,0),
#            arrowprops=dict(facecolor='red', shrink=0.05),
#            )
#
#    file_send_data = './results_embsys_entry/data_send.txt'
#    file_read_data = './results_embsys_entry/data_received.txt'
#    (mu,sigma) = analyze(file_send_data,file_read_data)
#    mu = round(mu,2)
#
#    plt.plot(x,mlab.normpdf(x,mu,sigma),label='embsys_entry  @'+str(mu)+"ms")
#    plt.annotate("3", xy=((mu,0)), xytext=(mu,0),
#            arrowprops=dict(facecolor='red', shrink=0.05),
#            )
#  
#    file_send_data = './results_embsys_1/data_send.txt'
#    file_read_data = './results_embsys_1/data_received.txt'
#    (mu,sigma) = analyze(file_send_data,file_read_data)
#    mu=round(mu,2)
#    plt.plot(x,mlab.normpdf(x,mu,sigma),label='embsys_1  @'+str(mu)+"ms")
#    plt.annotate("4", xy=((mu,0)), xytext=(mu,0),
#            arrowprops=dict(facecolor='red', shrink=0.05),
#            )
#  
#    file_send_data = './results_embsys_2/data_send.txt'
#    file_read_data = './results_embsys_2/data_received.txt'
#    (mu,sigma) = analyze(file_send_data,file_read_data)
#    mu = round(mu,2)
#    plt.plot(x,mlab.normpdf(x,mu,sigma),label='embsys_2  @'+str(mu)+"ms")
#    plt.annotate("5", xy=((mu,0)), xytext=(mu,0),
#            arrowprops=dict(facecolor='red', shrink=0.05),
#            )
 
    file_send_data = 'sendfilefinlib.txt'
    file_read_data = 'receivefilefinlib.txt'
#    tp='ab'
    (mu,sigma,df) = analyze(file_send_data,file_read_data,tp)
#    mu = round(mu,2)
#    plt.plot(x,mlab.normpdf(x,mu,sigma),label='embsys_exit  @'+str(mu)+"ms")
#    plt.annotate("6", xy=((mu,0)), xytext=(mu,0),
#            arrowprops=dict(facecolor='red', shrink=0.05),
#            )

    #plt.ylim([0,1])
    plt.xlim([0,10])
    plt.show()
    plt.legend()
    
   


    

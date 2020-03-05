import pandas as pd 
import numpy as np
import custom_library.test.reformatfiles as reformatfiles
import custom_library.test.analyzer as analyzer
import matplotlib.pyplot as plt
import os

### user settings
list_pp=["tpf_ms_com_entry","tpf_ms_com_exit","tpf_srv_entry","tpf_srv_exit","tpf_ss_com_entry","tpf_ss_com_exit","tpf_ss_embsys_entry","tpf_ss_embsys_exit"] #ping point list

#list_pp=["tpf_ss_embsys_entry","tpf_ss_embsys_exit"] #ping point list

### initialization
array_obj_stat = np.zeros(len(list_pp), dtype=object)
array_obj_data = np.zeros(len(list_pp), dtype=object)
### analyzis
for i in range(len(list_pp)):
  ## reformat data_received/data_send.txt & save as dr/ds.txt
  reformatfiles.reformatfiles("../../results/data_received.txt","dr1.txt",list_pp[i])   
  reformatfiles.reformatfiles("../../results/data_send.txt","ds1.txt",list_pp[i]) 
  ## analyzer the results
  (obj_stat,obj_data) = analyzer.analyze("ds1.txt","dr1.txt",list_pp[i])
  array_obj_stat[i]=obj_stat #statistics of send/received data
  array_obj_data[i]=obj_data #raw rtt/2 data
  

## creating a single data frame for multiple ping-points
df_stat = pd.concat(array_obj_stat, axis=1) 
df_data = pd.concat(array_obj_data, axis=1) 


###printing the dataframe
print df_stat

### indexing
#df.iloc[:,[1,2]]

### converting to latex table
#print df.to_latex()

### saving as xlsx file
#writer = pd.ExcelWriter('output.xlsx')
#df_stat.to_excel(writer,'statistics')
#df_data.to_excel(writer,'raw rtt_by_2')
#writer.save()

### plots ----------
### latency bar plot
df_stat.loc["avg latency(ms)",:].plot(kind='bar', rot=10, alpha=0.5)
plt.ylabel("latency (ms)")
#df_stat.loc["median latency(ms)",:].plot(kind='bar',legend="True",rot=10, alpha=0.5)

## jitter bar plot
#df_var = pd.DataFrame()
#df_var = (df_data.describe().loc["75%"] - df_data.describe().loc["25%"]).copy()
#df_var.plot(kind='bar',legend="True",rot=10, alpha=0.5)

### latency box plot
#readme - https://matplotlib.org/devdocs/api/_as_gen/matplotlib.pyplot.boxplot.html
#df_data.plot(kind='box',legend='True',rot=10, sym='', notch='True')

#df_data.plot(kind='box',legend='True',rot=10, sym='', notch='True', bootstrap=10000)
#df_data.plot(kind='box',legend='True',rot=10, sym='', meanline='True', showmeans='True', notch='True')

### latency histogram plots
#df_data.iloc[:,[0,2,4,6]].plot(kind='hist', stacked=True, alpha=0.5, bins=300)
#plt.axis([0, 11.5, 0, 260])  #first two for x-axis limit, next two for y-axis
#plt.xlabel("latency (ms)")
#plt.ylabel('frequency (out of 10,000)')

plt.show()
    
## remove temperory files
os.remove("ds.txt")
os.remove("dr.txt")

print "\nDONE !!!"

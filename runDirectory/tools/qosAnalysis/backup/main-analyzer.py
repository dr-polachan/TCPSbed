import pandas as pd 
import numpy as np
import custom_library.test.reformatfiles as reformatfiles
import custom_library.test.analyzer as analyzer
import matplotlib.pyplot as plt
import os

### user settings
list_pp=["tpf_srv_entry","tpf_srv_exit","tpf_ss_com_entry","tpf_ss_com_exit","tpf_embsys_entry","tpf_embsys_exit"] #ping point list
#ping_points = ["tp_embsys_exit","tp_embsys_entry"]

### initialization
array_obj_stat = np.zeros(len(list_pp), dtype=object)
array_obj_data = np.zeros(len(list_pp), dtype=object)
### analyzis
for i in range(len(list_pp)):
  ## reformat data_received/data_send.txt & save as dr/ds.txt
  reformatfiles.reformatfiles("data_received.txt","dr.txt",list_pp[i])   
  reformatfiles.reformatfiles("data_send.txt","ds.txt",list_pp[i]) 
  ## analyzer the results
  (obj_stat,obj_data) = analyzer.analyze("ds.txt","dr.txt",list_pp[i])
  array_obj_stat[i]=obj_stat #statistics of send/received data
  array_obj_data[i]=obj_data #raw rtt/2 data
  

## creating a single data frame for multiple ping-points
df_stat = pd.concat(array_obj_stat, axis=1) 
df_data = pd.concat(array_obj_data, axis=1) 


###printing the dataframe
#print df_stat

### indexing
#df.iloc[:,[1,2]]

### converting to latex table
#print df.to_latex()

### saving as xlsx file
#writer = pd.ExcelWriter('output.xlsx')
#df_stat.to_excel(writer,'statistics')
#df_data.to_excel(writer,'raw rtt_by_2')
#writer.save()

### plots
#df1.loc["avg latency(ms)",:].plot(kind='bar',legend="True",rot=10, alpha=0.5)
#df=df.rename(columns = {'tp_embsys_exit':'tpf_ss_embsys_exit'}) #rename coloumn names

### histogram plots
#df_data.plot(kind='hist', stacked=True, alpha=0.5, bins=300)
#plt.axis([0, 10, 0, 7000])  #first two for x-axis limit, next two for y-axis
#plt.xlabel("latency (ms)")
#plt.ylabel('frequency (out of 10,000)')
#plt.show()
    
## remove temperory files
os.remove("ds.txt")
os.remove("dr.txt")

print "\nDONE !!!"

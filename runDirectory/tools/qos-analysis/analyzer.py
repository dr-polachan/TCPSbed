import pandas as pd ## previous version used u'0.20.1'
import numpy as np
import library.test.reformatfiles as reformatfiles
import library.test.analyzer as analyzer
import matplotlib.pyplot as plt
import os
import scipy
import scikits.bootstrap as bootstrap

plt.close('all')

### read list of echo-points to parse
execfile("settings")
list_pp = list_tp

### initialization
array_obj_stat = np.zeros(len(list_pp), dtype=object)
array_obj_data = np.zeros(len(list_pp), dtype=object)

### analyzis
for i in range(len(list_pp)):
  ## reformat data_received/data_send.txt & save as dr/ds.txt
  reformatfiles.reformatfiles("../../results/qos-analysis/data_received.txt","./results/dr1.txt",list_pp[i])   
  reformatfiles.reformatfiles("../../results/qos-analysis/data_send.txt","./results/ds1.txt",list_pp[i]) 
  ## analyzer the results
  (obj_stat,obj_data) = analyzer.analyze("./results/ds1.txt","./results/dr1.txt",list_pp[i])
  array_obj_stat[i]=obj_stat #statistics of send/received data
  array_obj_data[i]=obj_data #raw rtt/2 data
  
### creating a single data frame for multiple echo points
df_stat = pd.concat(array_obj_stat, axis=1) 
df_data = pd.concat(array_obj_data, axis=1) 

### printing statistics
print df_stat

### replacing NaN with previous values
df_data = df_data.fillna(method='ffill').copy()

### finding 95% confidence interval for the means
errorPercentage = []   
for i in range (len(df_data.columns)):
    CIs = bootstrap.ci(data=df_data.iloc[:,i], statfunction=scipy.mean)  
    a1 = CIs[1] -df_data.iloc[:,i].mean()
    a2 = -(CIs[0]-df_data.iloc[:,i].mean())
    percentage = 100*(CIs[1]-CIs[0])/df_data.iloc[:,i].mean()
    errorPercentage.append(percentage)
df_stat.loc["errorPercentageInMean"] = errorPercentage


### latency bar plot
plt.figure("latency plots")
error = df_stat.loc["errorPercentageInMean"]*df_stat.loc["avg latency(ms)",:]/100.0
df_stat.loc["avg latency(ms)",:].plot(kind='bar',rot=10, alpha=0.8, yerr=np.transpose(error))
plt.ylabel("average latency (ms)",fontsize=12)

### latency histogram plots
plt.figure("latency histogram")
dfx = df_data.iloc[:,0].copy()
dfx.hist(bins = 200, xlabelsize =12, ylabelsize=12 ) 
plt.xlabel("latency (ms)", fontsize=12)
plt.ylabel('frequency (out of '+str(len(dfx))+')',fontsize=12)
plt.legend(fontsize=12) 
  
### remove temperory files
os.remove("ds.txt")
os.remove("dr.txt")

plt.show()

print "\nDONE !!!"

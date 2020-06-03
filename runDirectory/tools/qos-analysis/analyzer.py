import pandas as pd ## previous version used u'0.20.1'
import numpy as np
import library.test.reformatfiles as reformatfiles
import library.test.analyzer as analyzer
import matplotlib.pyplot as plt
import os

import scipy
import scikits.bootstrap as bootstrap

plt.close('all')

### user settings
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

### replacing NaN with previous values
df_data = df_data.fillna(method='ffill').copy()

### finding 95% confidence interval for the means
errorPercentage = []   
for i in range (len(df_data.columns)):
    CIs = bootstrap.ci(data=df_data.iloc[:,i], statfunction=scipy.mean)  
    #print max error
    a1 = CIs[1] -df_data.iloc[:,i].mean()
    a2 = -(CIs[0]-df_data.iloc[:,i].mean())
    percentage = 100*(CIs[1]-CIs[0])/df_data.iloc[:,i].mean()
    #print "\n Error % on calculated mean (for 95% confidence interval) =", round(percentage,2),"%"
    errorPercentage.append(percentage)
#print "errorPercentage", errorPercentage
df_stat.loc["errorPercentageInMean"] = errorPercentage
#<<<

### plots ----------
### latency bar plot
plt.figure("Figure 1")
#df_stat.loc["avg latency(ms)",:].plot(kind='bar',rot=10, alpha=0.5)
#df_stat.loc["median latency(ms)",:].plot(kind='bar',rot=10, alpha=0.5)
#error = [0.005, 0.004, 0.004, 0.007, 0.009, 0.009, 0.069, 0.021]
#error = [18.19]
error = df_stat.loc["errorPercentageInMean"]*df_stat.loc["avg latency(ms)",:]/100.0
df_stat.loc["avg latency(ms)",:].plot(kind='bar',rot=10, alpha=0.8, yerr=np.transpose(error))
##df_stat.loc["avg latency(ms)",:].plot(kind='bar',rot=10, alpha=0.5, yerr=2*df_stat.loc["std latency(ms)",:])
#df_stat.loc["avg latency(ms)",:].plot(kind='bar',rot=20, alpha=0.5,fontsize=12)
##df_stat.loc["avg latency(ms)",:].plot.barh()
plt.ylabel("average latency (ms)",fontsize=12)
#plt.title("average latency (ms)",fontsize=12)
##df_stat.loc["median latency(ms)",:].plot(kind='bar',legend="True",rot=10, alpha=0.5)


## Ratio plots
#dfx_latency = pd.DataFrame()
#dfx_variance = pd.DataFrame()
#
#dfx_latency = df_withVideo.loc["avg latency(ms)",:]/df_withoutVideo.loc["avg latency(ms)",:]
#dfx_variance = df_withVideo.loc["std latency(ms)",:]/df_withoutVideo.loc["std latency(ms)",:]
#plt.subplot(2,1,1)
#dfx_latency.plot(kind='bar',rot=10, alpha=0.7)
#plt.ylabel("ratio of mean latency")
#plt.ylim((0,1.5))
#plt.subplot(2,1,2)
#dfx_variance.plot(kind='bar',rot=10, alpha=0.7)
#plt.ylabel("ratio of std-deviation")

# Side by side bar plot (for latency comparison with and wihtout video)
#dfLatency = pd.DataFrame()
#dfLatency["withoutVideo"] = df_withoutVideo.loc["avg latency(ms)",:]
#dfLatency["withVideo"] = df_withVideo.loc["avg latency(ms)",:]
#dfLatency.plot(kind='bar',rot=20, alpha=0.7, fontsize=12)
#plt.ylabel("average latency (ms)",fontsize=12)
#plt.legend(fontsize=12) # using a size in points


#dfJitter = pd.DataFrame()
#dfJitter["withoutVideo"] = df_withoutVideo.loc["std latency(ms)",:]
#dfJitter["withVideo"] = df_withVideo.loc["std latency(ms)",:]
#dfJitter.plot(kind='bar',rot=20, alpha=0.7,fontsize=12)
#plt.ylabel("std-deviation in latency (ms)",fontsize=12)
#plt.legend(fontsize=12) # using a size in points

#dfLatency = pd.DataFrame()
#dfLatency["withoutVideo"] = df_withoutVideo.loc["avg latency(ms)",:]
#dfLatency["withVideo"] = df_withVideo.loc["avg latency(ms)",:]
#dfLatency["difference"] = dfLatency["withoutVideo"] - dfLatency["withVideo"]
#dfLatency["difference"].plot(kind='bar',rot=10, alpha=0.7)
#plt.ylabel("average latency (ms)",fontsize=12)

### link latency bar plot
#link_0 = df_stat.loc["avg latency(ms)",:][2]-df_stat.loc["avg latency(ms)",:][1]
#link_1 = df_stat.loc["avg latency(ms)",:][4]-df_stat.loc["avg latency(ms)",:][3]
#link_2 = df_stat.loc["avg latency(ms)",:][6]-df_stat.loc["avg latency(ms)",:][5]
#
#df_link = pd.DataFrame()
#df_link["link 0: ms_com - srv"]=[link_0]
#df_link["link 1: srv - ss_com"]=[link_1]
#df_link["link 2: ss_com - ss_embsys"]=[link_2]
#df_link.plot(kind='bar',rot=10, alpha=0.5)
#plt.ylabel("average latency (ms)")
#plt.xlabel("links")

## jitter "bar" plot
#df_var = pd.DataFrame()
#df_var = (df_data.describe().loc["75%"] - df_data.describe().loc["25%"]).copy()
#df_var.plot(kind='bar',legend="True",rot=10, alpha=0.5)

### latency box plot
#plt.figure("latency box plot")
#dfx = df_data.copy()
#mask = (dfx > dfx.quantile(.05)) & (dfx <= dfx.quantile(.95))
#dfx = dfx[mask].copy()
#df_data = dfx.copy()
#readme - https://matplotlib.org/devdocs/api/_as_gen/matplotlib.pyplot.boxplot.html
#df_data.plot(kind='box',legend='True',rot=10, sym='', notch='True')
#df_data.plot(kind='box',legend='True',rot=10, sym='', notch='True', bootstrap=10000)
#df_data.plot(kind='box',legend='True',rot=10, sym='', meanline='True', showmeans='True', notch='True')
#plt.ylabel('latency statistics',fontsize=12)
#plt.title('latecy box plot',fontsize=12)

### latency histogram plots
plt.figure("latency histogram")
dfx = df_data.iloc[:,0].copy()
#dfx = df_data.iloc[:,[0,2,4,6]].copy()
mask = (dfx > dfx.quantile(.05)) & (dfx <= dfx.quantile(.95))
dfx[mask].hist(bins = 100, xlabelsize =12, ylabelsize=12 ) #stacked=True, alpha=0.5, bins=50)
plt.xlabel("latency (ms)", fontsize=12)
plt.ylabel('frequency (out of '+str(len(dfx))+')',fontsize=12)
plt.legend(fontsize=12) # using a size in points
  
## remove temperory files
os.remove("ds.txt")
os.remove("dr.txt")

plt.show()

print "\nDONE !!!"

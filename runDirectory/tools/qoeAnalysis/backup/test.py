#import matlab.engine
#if( eng == False ):
#    eng = matlab.engine.start_matlab()

import custom_library.test.StepInfov4_deepak as myStepInfo
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
#import numpy as np

import scipy
import scikits.bootstrap as bootstrap
#http://www.randalolson.com/2012/08/06/statistical-analysis-made-easy-in-python/

matplotlib.rcParams.update({'font.size': 12})

plt.close('all')

goodnessCount = 0
m = 100 #number of step response curves

varRiseTime = []
varOvershoot = []
overshoot = []
for i in range(m):
    print "iteration", i
    ## reading the file
    df = pd.read_csv("../../results/StepAnalysis/data"+str(i)+".txt", header=None)
    df1 = pd.DataFrame()
    
    ## extracting only the step curve        
    for i in range(15,len(df)): 
        if ((df.iloc[i,1]) < 90):
            k=i
            break
    
    ## saving to dataframe, scaling
    df1["time"] = df.iloc[:,0].copy()
    df1["time"] = df1["time"] - df1["time"].iloc[0]
#    df1["data"] = (df.iloc[k:,1].copy() - 80)*5 #scaling the step response graph
    df1["data"] = df.iloc[:,1].copy()    
    
    ## passing to matlab stepinfo
    y = df1["data"].tolist()
    t = df1["time"].tolist()	
    
    #change only here -start
#    y = matlab.double(y)
#    t = matlab.double(t)    
#    t = eng.stepinfo(y,t,100)
#    t = myStepInfo.myStepInfo(df1)
#    print df1["time"]
#    print df1["data"]
#    print "this must be printed",df1
    t = myStepInfo.myStepInfo(df1)
    t = t.iloc[0,:]
#    print t
#    print "the overshoot is",t["overshoot"]
#    overshoot = t["overshoot"].tolist()
#    risetime = t["rise times"].tolist()
#    print "list overshoot is",overshoot
    #print "overshoot 0 is",overshoot[0]
    # -change in end.
    
    ## printing the results
    if (t["overshoot"] < 20):
        goodnessCount += 1
        varRiseTime.append(round(1000*t["rise times"],5))
    varOvershoot.append(round(t["overshoot"],5))
    
    #print overshoot, round(1000*t["RiseTime"],3),"ms"
    
    ##for plotting step curves in an overlap fashion
    #plt.plot(df1["time"], df1["data"])


df_data  = pd.DataFrame(varRiseTime)
df_overshoot = pd.DataFrame(varOvershoot)

#print "the data dataframe is",df_data
#print "the overshoot dataframe is",df_overshoot

### finding 95% confidence interval for the means
for i in range (1):
    CIs = bootstrap.ci(data=df_data.iloc[:,i], statfunction=scipy.mean)  
    #print max error
    a1 = CIs[1] -df_data.iloc[:,i].mean()
    a2 = -(CIs[0]-df_data.iloc[:,i].mean())
    ErrorPercentage = 100*(CIs[1]-CIs[0])/df_data.iloc[:,i].mean()
    ErrorPercentage = round(ErrorPercentage,2)
    #if(a1 > a2):
    #    print round(a1,3)
    #else:
    #    print round(a2,3)

## Summarizing results
print "-------"
print "Summary::"
#print "Goodness percentage =", round(100*(goodnessCount/(m*1.0)),2),"%"
print "Average Rise Time =", round(df_data.iloc[:,i].mean(),3), "with Error% =", ErrorPercentage,"%"
print "tcpsCQM =", round((1.5/round(df_data.iloc[:,i].mean(),3)),2), "@ p=", round(100*(goodnessCount/(m*1.0)),2),"%"
print "tcpsCQM (in log10) =", round(np.log10(1.5/round(df_data.iloc[:,i].mean(),3)),2), "@ p=", round(100*(goodnessCount/(m*1.0)),2),"%"
print "-------"

### for plotting overshoot histogram
#ax1 = df_overshoot.plot(kind='bar')

### for plotting overlapped step response curves
#plt.xlabel('Time (in seconds)', fontsize = '12')
#plt.ylabel('Haptic Data (units)', fontsize = '12')
#plt.show()

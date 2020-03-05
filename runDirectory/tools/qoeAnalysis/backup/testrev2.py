#import matlab.engine
#try:
#    if( eng == False ):
#        eng = matlab.engine.start_matlab()
#except:
#        eng = matlab.engine.start_matlab()
from libStepInfo.custom import myStepInfo as myStepInfo
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
import numpy as np

import scipy
import scikits.bootstrap as bootstrap
#http://www.randalolson.com/2012/08/06/statistical-analysis-made-easy-in-python/

matplotlib.rcParams.update({'font.size': 12})

plt.close('all')

goodnessCount = 0


varRiseTime = []
varOvershoot = []
varBooleanGoodness = []

SampleCounts = 500

m = 100 #number of step response curves
Index = 0

mStart = SampleCounts*(Index)
#print "what is this",mStart
for i in range(mStart, mStart+m):
#for i in range(46, 48):
#for i in range(m):
    print "iteration", i
    ## reading the file
    df = pd.read_csv("../../results/StepAnalysis/data"+str(i)+".txt", header=None)
    df1 = pd.DataFrame()
    
    
    ## extracting only the step curve        
    for i in range(15,len(df)): 
        if ((df.iloc[i,1]) < 90):
            k=i
            break
    print "the value of k is",k
    ## saving to dataframe, scaling
    df1["time"] = df.iloc[:,0].copy()
    #df1["time"] = df.iloc[k:]
    df1["time"] = df1["time"] - df1["time"].iloc[0]
    df1["data"] = (df.iloc[:,1].copy() - 80)*5 #scaling the step response graph
    #df1["data"] = df.iloc[:,1].copy()
    #df1["data"] = df.iloc[k:]    
    ## passing to matlab stepinfo
    y = df1["data"].tolist()
    t = df1["time"].tolist()
    
    print "the time taken in is", df1["time"]

    #change only here -start----------------------
#    y = matlab.double(y)
#    t = matlab.double(t)    
#    t = eng.stepinfo(y,t,100)
#    print "this must be printed",df1
    t = myStepInfo(df1)
    t = t.iloc[0,:]
    print "overshoot",t["overshoot"]
    print "settling time",t["settling-time"]
    print "latency",t["latency"]
    print "mean square error",t["mean-square-error"]
    # -change in end ------------------------------
    
    ## printing the results
    if (t["overshoot"] < 20):
        goodnessCount += 1
        varRiseTime.append(round(1000*t["rise times"],5))
        varBooleanGoodness.append(1)
    else:
        varBooleanGoodness.append(0)    
        
    varOvershoot.append(round(t["overshoot"],5))
    
    print t["overshoot"], round(1000*t["rise times"],3),"ms", varBooleanGoodness[-1], goodnessCount
    
    ##for plotting step curves in an overlap fashion
    plt.plot(df1["time"], df1["data"])

df_data  = pd.DataFrame(varRiseTime)
df_dataGoodness = pd.DataFrame(varBooleanGoodness)
df_overshoot = pd.DataFrame(varOvershoot)

### finding rise time mean and its 95% confidence interval

i=0
CIs = bootstrap.ci(data=df_data.iloc[:,i], statfunction=scipy.mean)  
#print max error
a1 = CIs[1] -df_data.iloc[:,i].mean()
a2 = -(CIs[0]-df_data.iloc[:,i].mean())
ErrorPercentageRiseTime = 100*(CIs[1]-CIs[0])/df_data.iloc[:,i].mean()
ErrorPercentageRiseTime = round(ErrorPercentageRiseTime,2)



### finding mean goodness percentage and its 95% confidence interval

i=0
CIs = bootstrap.ci(data=df_dataGoodness.iloc[:,i], statfunction=scipy.mean)  
#print max error
a1 = CIs[1] -df_dataGoodness.iloc[:,i].mean()
a2 = -(CIs[0]-df_dataGoodness.iloc[:,i].mean())
ErrorPercentageGoodness = 100*(CIs[1]-CIs[0])/df_dataGoodness.iloc[:,i].mean()
ErrorPercentageGoodness = round(ErrorPercentageGoodness,2)

### finding 

    #if(a1 > a2):
    #    print round(a1,3)
    #else:
    #    print round(a2,3)

## Summarizing results

print "-------"
print "Summary::"
#print "Goodness percentage =", round(100*(goodnessCount/(m*1.0)),2),"%"
print "Average Rise Time =", round(df_data.iloc[:,i].mean(),3), "with Error% = +/-", ErrorPercentageRiseTime/2,"%"
print "Goodness Percentage =", round(100*df_dataGoodness.iloc[:,i].mean(),3), "% with Error% = +/-", ErrorPercentageGoodness/2,"%"
print "tcpsCQM =", round((1.5/round(df_data.iloc[:,i].mean(),3)),2), "@ p=", round(100*(goodnessCount/(m*1.0)),2),"%"
print "tcpsCQM (in log10) =", round(np.log10(1.5/round(df_data.iloc[:,i].mean(),3)),2), "dB @ p=", round(100*(goodnessCount/(m*1.0)),2),"%"
print "-------"





### for plotting overshoot histogram
#ax1 = df_overshoot.plot(kind='bar')

## for plotting overlapped step response curves
plt.xlabel('Time (in seconds)', fontsize = '12')
plt.ylabel('Haptic Data (units)', fontsize = '12')
plt.show()

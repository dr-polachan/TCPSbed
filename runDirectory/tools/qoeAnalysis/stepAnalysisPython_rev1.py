#import matlab.engine
#try:
#    if( eng == False ):
#        eng = matlab.engine.start_matlab()
#except:
 #       eng = matlab.engine.start_matlab()
from libStepInfo.custom import myStepInfo as myStepInfo
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
import numpy as np
import sys
import scipy
import scikits.bootstrap as bootstrap
#http://www.randalolson.com/2012/08/06/statistical-analysis-made-easy-in-python/

matplotlib.rcParams.update({'font.size': 12})

plt.close('all')

goodnessCount = 0


varRiseTime = []
varOvershoot = []
varBooleanGoodness = []



m = 30 #number of step response curves
Index = 0

SampleCounts = 500
mStart = SampleCounts*(Index)

for i in range(mStart, mStart+m):
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
    df1["time"] = df.iloc[:,0].copy() ### this line is different when using matlab step info code
    df1["time"] = df1["time"] - df1["time"].iloc[0]
    df1["data"] = (df.iloc[:,1].copy() - 80)*5 #scaling the step response graph
    
    ## passing to matlab stepinfo
    y = df1["data"].tolist()
    t = df1["time"].tolist()
    
    ## section-A -start [this section is different when using matlab step info
    t = myStepInfo(df1)
    t = t.iloc[0,:]
    ## section-A -end
    
    ## printing the results
    if (t["Overshoot"] < 20):
        goodnessCount += 1
        varRiseTime.append(round(1000*t["RiseTime"],5))
        varBooleanGoodness.append(1)
    else:
        varBooleanGoodness.append(0)    
        
    varOvershoot.append(round(t["Overshoot"],5))
    
    print t["Overshoot"], round(1000*t["RiseTime"],3),"ms", varBooleanGoodness[-1], goodnessCount
    
    ##for plotting step curves in an overlap fashion
    plt.plot(df1["time"], df1["data"])

df_data  = pd.DataFrame(varRiseTime)
df_dataGoodness = pd.DataFrame(varBooleanGoodness)
df_overshoot = pd.DataFrame(varOvershoot)

## >> Added on June 14th
if(len(df_data)==0):
    print "\nmyWarning: No good step respnose curves identified, check the results"
    sys.exit()
## <<
    
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
print "tcpsCQM =", round((1.5/round(df_data.iloc[:,i].mean(),3)),4), "@ p=", round(100*(goodnessCount/(m*1.0)),2),"%"
tcpsCQM = round(np.log10(1.5/round(df_data.iloc[:,i].mean(),3)),4)
print "tcpsCQM (in log10) =", tcpsCQM, "dB @ p=", round(100*(goodnessCount/(m*1.0)),3),"%"
ShkMax = 1*pow(10,tcpsCQM)
print "Shk(max) =", round(ShkMax,5), "m/s" 
print "-------"


## for plotting overlapped step response curves
plt.xlabel('Time (in seconds)', fontsize = '12')
plt.ylabel('Haptic Data (units)', fontsize = '12')
plt.show()

from pandas import ExcelFile
import pandas as pd
import matplotlib.pyplot as plt
import custom_library.test.StepInfov4_deepak as myStepInfo


df = pd.read_csv("../../results/StepAnalysis/data(0.9).txt", header=None)

print df

df1 = pd.DataFrame()

df1["time (in seconds)"] = df.iloc[:,0] 
df1["time (in seconds)"] = df1["time (in seconds)"] - df1["time (in seconds)"][0]
df1["pressure profile"] = df.iloc[:,1] 

print "df1", df1


df1["time"] = df1["time (in seconds)"] 
df1["data"] = df1["pressure profile"]

result = myStepInfo.myStepInfo(df1)

print result

ax = df1.plot(x='time (in seconds)', y='pressure profile',style='-*')




plt.show()



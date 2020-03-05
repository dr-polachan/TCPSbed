from pandas import ExcelFile
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("../../results/StepAnalysis/data.txt", header=None)

print df

df1 = pd.DataFrame()

df1["time (in seconds)"] = df.iloc[:,0] 
df1["time (in seconds)"] = df1["time (in seconds)"] - df1["time (in seconds)"][0]
df1["pressure profile"] = df.iloc[:,1] 

print "df1", df1

ax = df1.plot(x='time (in seconds)', y='pressure profile',style='-*')

plt.show()



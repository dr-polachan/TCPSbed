from pandas import ExcelFile
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('Data.txt', header=None)

print df

df1 = pd.DataFrame()

df1["time (in seconds)"] = df.iloc[:,0] #df.iloc[:,0+3*i].dropna().copy()
df1["time (in seconds)"] = df1["time (in seconds)"] - df1["time (in seconds)"][0]
df1["pressure profile"] = df.iloc[:,1] #df.iloc[:,1+3*i].dropna().copy()

print "df1", df1

ax = df1.plot(x='time (in seconds)', y='pressure profile',style='-*')

plt.show()

#df2 = pd.DataFrame()
#df2["time"] = df.iloc[:,5].dropna().copy()
#df2["pressure_added_delay_of_30ms"] = df.iloc[:,6].dropna().copy()

#df2.plot(x='time', y='pressure_added_delay_of_30ms', ax=ax)

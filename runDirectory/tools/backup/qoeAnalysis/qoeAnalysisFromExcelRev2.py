from pandas import ExcelFile
import pandas as pd
import matplotlib.pyplot as plt
## inputs
plt.close('all')

myExcel = "data.xlsx"
#myWorksheet = "impulse-haptic-only"
myWorksheet = "objective-controller"

## read & convert to excel
obj = ExcelFile(myExcel) #reading excel file
df = obj.parse(myWorksheet,header=None) #reading the worksheet in the excel file

#df = pd.read_excel(open(myExcel,'rb'), sheetname = myWorksheet, header=None)

df1 = pd.DataFrame()

i=5 #nth data set n=[0, ...]
df1["time (in seconds)"] = df.iloc[:,0+3*i].dropna().copy()
df1["time (in seconds)"] = df1["time (in seconds)"] - df1["time (in seconds)"][0]
df1["pressure profile"] = df.iloc[:,1+3*i].dropna().copy()

ax = df1.plot(x='time (in seconds)', y='pressure profile',style='-*')

#df2 = pd.DataFrame()
#df2["time"] = df.iloc[:,5].dropna().copy()
#df2["pressure_added_delay_of_30ms"] = df.iloc[:,6].dropna().copy()

#df2.plot(x='time', y='pressure_added_delay_of_30ms', ax=ax)

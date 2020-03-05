from pandas import ExcelFile

import csv
## inputs
myExcel = "settings.xlsx"
myWorksheet = "generated-file"

## read & convert to excel
obj = ExcelFile(myExcel) #reading excel file
df = obj.parse(myWorksheet) #reading the worksheet in the excel file

## Executing the content 
for i in range (0, len(df)):
    line = df.iloc[i,0]    
    exec(str(line))
#print "DONE"



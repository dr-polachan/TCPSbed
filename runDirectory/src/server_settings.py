from pandas import ExcelFile

## loading the excel file contents and executing it.

load_from_excel = 0
if(load_from_excel == 1):
	## inputs
	myExcel = "settings.xlsx"
	myWorksheet = "config"

	## read & convert to excel
	obj = ExcelFile(myExcel) #reading excel file
	df = obj.parse(myWorksheet) #reading the worksheet in the excel file

	## writing the read value from excel to file: generated-file
	f = open('config', 'w')

	for i in range (0, len(df)):
	    line = df.iloc[i,0]    
	    f.write(line+"\n")  
	    #print "debug",line

	f.close() 

## executing the configuration file "generated-file"
execfile('config')

print "configurations-loaded-sucessfully"

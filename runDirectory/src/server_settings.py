from pandas import ExcelFile

load_from_excel = 0
if(load_from_excel == 1):
	myExcel = "settings.xlsx"
	myWorksheet = "config"

	obj = ExcelFile(myExcel) 
	df = obj.parse(myWorksheet) 

	f = open('config', 'w')
	for i in range (0, len(df)):
	    line = df.iloc[i,0]    
	    f.write(line+"\n")  
	f.close() 

execfile('config')

print "configurations-loaded-sucessfully"

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

#*time = np.array([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9])
#data = np.array([1,1,1,1,1,0.6,0,0.8,1.11,0.95,1,1,1,0.7,0.2,1.2,0.95,1,1,1])

#time = np.array([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2])
#data = np.array([1,1,1,1,1,0.6,0.1,0.8,1,1,1,1,1])

#time = np.array([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5])
#data = np.array([1,1,1,1,1,0.6,0.1,0.8,1,1,1,1,1,1,1,1,1,1,0.6,0.1,0.8,1,1,1,1,1])

#time = np.array([0,0.0153098106,0.0311799049,0.0465300083,0.0619599819,0.0776298046,0.0929498672,0.108579874,0.1238698959,0.1389698982,0.1546800137,0.1702299118,0.1857500076,0.2014598846,0.2166700363,0.2322700024,0.2479200363,0.263299942,0.2786698341,0.2941799164,0.3095300198,0.3249900341])
#data = np.array([1,1,1,0,0.75,0.875,0.9375,0.96875,0.984375,0.9921875,0.99609375,0.998046875,0.9990234375,0.9995117188,0.9997558594,0.9998779297,0.9999389648,0.9999694824,0.9999847412,0.9999923706,0.9999961853,0.9999980927])

#time = np.array([0,0.0159699917,0.0311601162,0.0467000008,0.0621399879,0.0778000355,0.0933401585,0.108700037,0.1242501736,0.1396400928,0.1550199986,0.1704201698,0.1854500771,0.2015800476,0.2170500755,0.2327301502,0.2480800152,0.2633500099,0.2787899971,0.2942202091,0.3095300198])
#data = np.array([1,1,1,0,0,0.75,1,1.125,1.125,1.0625,1,0.96875,.76875,0.984375,1,1.0078125,1.0078125,1.00390625,1,0.998046875,0.998046875])

#df2 = pd.read_csv("data2.txt", header=None)

#print df2

#time = np.array(df2.iloc[:,0])
#time = time - time[0]
#data = np.array(df2.iloc[:,1])
#data = data/100.0
#print data
#print time.shape
#print time

#print data.shape
#print data

#1.0625

#plt.plot(time,data,'-*')
#plt.show()

def func(x, a, b, c):
	return(a*x*x + b*x + c)

def myStepInfo(dfInput):
    
    myRiseFallThreshold = (81-80)*5  # 20 percent
    flagFallDetected = 0
    rise_time = 0
    n = 1
    x = 2
    zero_overshoot_flag = 0
    settle_found_counter = 0
#   
    myFallIndex = []
    myRiseIndex = []
    myLatency = []
    myOvershoot = []
    myOvershootIndex = []
    myRisePoints = []
    myFallPoints = []
    myRiseTime = []
    myRisePointPredicted = []
    mySettleTime = []
    mySettleIndex = []
    myMeanSquareError = []
    
    
    
    time = dfInput["time"]
    data = dfInput["data"]
    #data = (data - 80)*5
    dfInput["data"] = data
#    print "the time here is",time
    
    ## Step-1: Detecting fall point index
    for i in range(2, len(time)):
         #print "what is this",data[i-2] 
         if(data[i-1] < myRiseFallThreshold):
            if (data[i-2] > data[i-1]) and (data[i-1] <= data[i]):
                if(flagFallDetected == 0):
                    myFallIndex.append(i-1)      
		    #print "i find fall point here", myFallIndex      
                    myFallPoints.append(round(time[i-1],3))        
                    flagFallDetected = 1
                    
            if(flagFallDetected == 1):
                if(data[i] > myRiseFallThreshold):
                    myRisePoints.append(round(time[i-1],3))
                    myRiseIndex.append(i-1)  
                    flagFallDetected = 0
#    print "the fall points are",myFallPoints
#    print "the Rise points are",myRisePoints    
    ## Step-2: Detecting latency
#    for i in range(len(myFallIndex)):
#        latency = time[myRiseIndex[i]] - time[myFallIndex[i]]
#        latency = round(latency,2)
#        myLatency.append(latency)
    
    ## Step-3: Detecting overshoot
    if (len(myFallIndex)>1):						# for multiple fall points
#	    print "I start from here"
	    for i in range(len(myFallIndex)-1):
        	overshoot = dfInput["data"].loc[myFallIndex[i]: myFallIndex[i+1]].max()
#		print "whats happening here?!?!", overshoot
#        	overshoot = round((overshoot-100)*100,2)
		overshoot = overshoot - 100
#		print "the current overshoot is",overshoot
        	myOvershoot.append(overshoot)
        
        	temp = dfInput["data"].loc[myFallIndex[i]: myFallIndex[i+1]].idxmax()
#		print "the overshoot index is",temp
        	myOvershootIndex.append(temp)
#    	    print "my overshoot finally contains",myOvershoot
    	    if(len(myFallIndex)>1):
        	i=i+1
        	overshoot = dfInput["data"].loc[myFallIndex[i]:].max()
#        	overshoot = round((overshoot-100)*100,2)
		overshoot = overshoot - 100
		if (overshoot<=0):
			overshoot = 0						#--------------------------
#			myOvershootIndex[i-1] = "NaN"
        	myOvershoot.append(overshoot)
        
        	temp =  dfInput["data"].loc[myFallIndex[i]:].idxmax()
#        print "data",temp
        	myOvershootIndex.append(temp)
#    print "here are the overshoot values",myOvershoot
    if (len(myFallIndex)==1):						# for single fall point
#	    print "i am finding overshoot for single fal point"
#	    print "I start from there"
	    for i in range(len(myFallIndex)):
        	overshoot = dfInput["data"].loc[myFallIndex[i]: len(time)].max()
#		print "whats happening here?!?!", overshoot
#        	overshoot = round((overshoot-100)*100,2)
		overshoot = overshoot - 100
#		print "this is simplew math this must happen", overshoot
#		print "the overshoot at single fall point is", overshoot
		if (overshoot<=0):
#			print "knock knock"
			overshoot = 0						#--------------------------
#			myOvershootIndex[i] = "NaN"
#		print "the current overshoot is",overshoot
        	myOvershoot.append(overshoot)
        
        	temp = dfInput["data"].loc[myFallIndex[i]: len(time)].idxmax()
#		print "the overshoot index is",temp
        	myOvershootIndex.append(temp)
#    	    print "my overshoot finally contains",myOvershoot
    	    if(len(myFallIndex)>1):
        	i=i+1
        	overshoot = df["data"].loc[myFallIndex[i]:].max()
        	overshoot = overshoot-100
        	myOvershoot.append(overshoot)
        	temp =  df["data"].loc[myFallIndex[i]:].idxmax()
#        print "data",temp
        	myOvershootIndex.append(temp)
 #   print "here are the overshoot values",myOvershoot 	        




    ## Step-4: Finding Rise Time
#    print "myOvershoot contains this before finding rise time",myOvershoot    
    for i in range(len(myRiseIndex)):

    
	if (len(myOvershootIndex)>0):
	        dfTemp = dfInput.loc[myRiseIndex[i]:myOvershootIndex[i]].copy()
#		print "the values to curve fit are",dfTemp

#	print"whats this",dfTemp
	if (myOvershoot[i] == 0):
	        dfTemp = dfInput.loc[myRiseIndex[i]:myRiseIndex[i]+2].copy()      ####################################please check this part (can change upper limit to len(time) instead of myRiseIndex[i]+3 but it is redusing accuracy
#		print "the values to curve fit are",dfTemp

#	print dfTemp

        dfTemp =  dfTemp.reset_index()

        dfTemp = (dfTemp - dfTemp.loc[0]).copy()

#	print "the values to curve fit are",dfTemp
        

        # setting the the thresholds for finding rise time

#        max_data = max(dfTemp["data"])
        max_data = max(dfTemp["data"]) - myOvershoot[i]
	min_data = min(dfTemp["data"])

	#print "the max is",max_data
	
	y1 = 0.1*(max_data - min_data)

	y2 = 0.9*(max_data - min_data)

#        y1 = 7.04 #- data[myRiseIndex[i]]

#        y2 = 28.16 #- data[myRiseIndex[i]]

        

        # finding second order equation
	popt, pcov = curve_fit(func, dfTemp["data"], dfTemp["time"],bounds=(0, [200.0, 200.0, 200.0]))
#	popt, pcov = curve_fit(func, dfTemp["data"], dfTemp["time"],bounds=0)

#        coefficients = np.polyfit(dfTemp["data"],dfTemp["time"],2) # (x,y)

        equation = np.poly1d(popt)

        

#        print "y1", equation(y1)
#	print "y2", equation(y2)

#        print "the fall times are------------------------------",myFallPoints
#	print "the rise times are------------------------------",myRisePoints
#	print "the current rise time is",myRisePoints[i]
	latency = myRisePoints[i] - myFallPoints[i] + equation(y1)
#	print "the latency is",latency
	myLatency.append(latency)
	

        # computing rise time

        rise_time = equation(y2) - equation(y1)      
#	print "the rise time is", rise_time
        rise_time = round(rise_time,4)

        myRiseTime.append(rise_time)

        

        # computing predicted rise index

        myRisePointPredicted.append(equation(y1)+time[myRiseIndex[i]])
#    print "the rise time is",myRiseTime
#    print "the predicted rise point is",myRisePointPredicted
        

    

       

	# computing settling time
    for i in range(len(myRiseIndex)):
#	print "what is the overshoot index here",myOvershootIndex[i]
#	print "the current overshoot index is",myOvershootIndex[i]	
#	print "the next fallIndex is",myFallIndex[i+1]
#	print "the value of i here is",i
	if (myOvershoot[i]==0):
#		print "i should be here"
		strt_index = myRiseIndex[i]
#		print "shouldnt i roll from here??"
#		print strt_index
		zero_overshoot_flag = 1
	else:
		strt_index = myRiseIndex[i]			##myOvershootIndex[i]
#		print "I roll from there onwards"
#		print "strt_index",strt_index
	if (i+1 == len(myRiseIndex)):
#		print "I roll here"
		dfSettlingPoints = dfInput.loc[strt_index:len(time)].copy()    
#		print "the settling points are",dfSettlingPoints
		
	else:
		dfSettlingPoints = dfInput.loc[strt_index:myFallIndex[i+1]].copy()
#	print "wahts this now....",dfSettlingPoints["data"]
	check_list = dfSettlingPoints["data"]
#	print "this's gotta be that",check_list
	dfMovingWindows = dfSettlingPoints.iloc[1:]
#	print "these are the initial parts of the window",dfMovingWindows
#	dfMovingWindows = dfSettlingPoints	
	unique_index = pd.Index(dfInput["time"])
	for n in range(len(dfSettlingPoints)):
#		print "the max of the moving window is",df["data"].loc[dfMovingWindows["data"].max()]

#		print "hello"
		
#		print "the moving windows are",dfMovingWindows 
#		print "the top element of the moving window is",dfMovingWindows["data"].iloc[0]		
#		print "the top element's timestamp of the moving window is",dfMovingWindows["time"].iloc[0]		
#		print "debug" 		
#		print "this should be the max of the moving data",dfMovingWindows["data"].max()
		if (zero_overshoot_flag == 1):
#			print "am i entering here?"
			if (dfMovingWindows["data"].min()>=(90- 80)*5):
#				print "hi from 0 overshoot settling points"
				time_at_settle = dfMovingWindows["time"].iloc[0]
				index_at_settle = unique_index.get_loc(time_at_settle)
				mySettleIndex.append(index_at_settle + 1)
				zero_overshoot_flag = 0
				settle_found_counter = 1
	#			print "the index of settling time",index_at_settle
	#			print "done...sortta :P",dfMovingWindows["time"].iloc[0]
				break
			dfMovingWindows = dfMovingWindows.iloc[1:]
			
#		print df["data"].iloc[dfMovingWindows["data"].max()]
		else:
#			print "it did not enter the previous block"
#			print "checking the following if condition",dfMovingWindows["data"].max(),dfMovingWindows["data"].min()
			if (dfMovingWindows["data"].max()<=(110- 80)*5 and dfMovingWindows["data"].min()>=(90- 80)*5 ):
				#print "hi from non zero overshoot settling points"
				time_at_settle = dfMovingWindows["time"].iloc[0]
				index_at_settle = unique_index.get_loc(time_at_settle)
				mySettleIndex.append(index_at_settle + 1)
				settle_found_counter = 1
	#			print "the index of settling time",index_at_settle
#				print "done...sortta :P",dfMovingWindows["time"].iloc[0]
				break
			dfMovingWindows = dfMovingWindows.iloc[1:]

	if(settle_found_counter == 1):
		cur_stl_time = time_at_settle - dfInput["time"].loc[strt_index] 
	#	print"the current settle time finally is",cur_stl_time
		mySettleTime.append(cur_stl_time)
	if(settle_found_counter == 0):
		cur_stl_time = 1000000	
		mySettleTime.append(cur_stl_time)
		mySettleIndex.append(1000000)
	


    ### Step - mean square error
    if(settle_found_counter == 1):
	    for i in range(len(myRisePoints)):
		dfErrorPoints = dfInput.loc[mySettleIndex[i]:mySettleIndex[i]+x]    
	#	print"the error points are",dfErrorPoints
	#	print "the mean is",dfErrorPoints["data"].mean()
		dfChangeFromMean = dfErrorPoints["data"].subtract(100)
	#	print "this is the resulting dataframe",dfChangeFromMean
		dfMeanSquareError = dfChangeFromMean.pow(2)
	#	print "the mean square error till the given point is",dfMeanSquareError
	#	print "the cumulative mean sqr error is",dfMeanSquareError.sum()
		dfMeanSquareError = dfMeanSquareError.sum()/len(dfMeanSquareError)
		myMeanSquareError.append(dfMeanSquareError)
    if(settle_found_counter == 0):
	    for i in range(len(myRisePoints)):
		myMeanSquareError.append(1000000)

    ### Step scaling overshoots 
#    for i in range(len(myOvershoot)):
#	    print "this is the oershoot before changing in the library",myOvershoot[i]
#	    myOvershoot[i] = ((myOvershoot[i] + 100 - 80)*5 - 100)

    ### Step - Loading Results
    dfResult = pd.DataFrame()    
    
    dfResult["overshootIndex"] = myOvershootIndex
    dfResult["fall-index"] = myFallIndex
    dfResult["rise-index"] = myRiseIndex
    dfResult["fall-points"] = myFallPoints
    dfResult["rise-points"] = myRisePoints
    #print "are ruslts being loaded?"
    dfResult["rise-points-predicted"] = myRisePointPredicted
    dfResult["RiseTime"] = myRiseTime
    dfResult["Overshoot"] = myOvershoot
    dfResult["latency"] = myLatency
    dfResult["settling-time"] = mySettleTime
    dfResult["settling-index"] = mySettleIndex
    dfResult["mean-square-error"] = myMeanSquareError
    return(dfResult)


################################################## uncomment for testing purposes only ########################################## 
#df = pd.DataFrame()
#df["time"] = time
#df["data"] = data

#result = myStepInfo(df)
#print result

#plt.plot(time,data,'-*')
#plt.show()


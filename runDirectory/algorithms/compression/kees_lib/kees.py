class kees:
    estimateList = [] # this attribute stores the estimation
    threshold = 1 # this variable defines the packet size in number of sensor values
    
    # this list is a string of floats with the initial values of the various flows
    def initializeEstimation(k, newEstimateList):
        k.estimateList = newEstimateList

    def prediction_decode(k, msgList):
            receiveList = msgList[:] # create a copy of the list
            selected = receiveList[0]
            
            receiveList.pop(0)
            receiveList = map(float, receiveList)

            """ calculate number of channels by looking at length of selected string"""
            count = len(selected)

            """ update the estimation """
            for i in xrange(0, count):
                    if selected[i] == '1':
                            k.estimateList[i] = receiveList[0]
                            receiveList.pop(0) # pop used value

            

    def prediction_encode(k, msgList):
            sourceList = map(float, msgList[:]) # transfer string to float and make a copy

            """ calculate number of channels """
            count = len(sourceList)

            """ calculate priority """
            score = [0]*count
            for i in xrange(0,count):
                    score[i] = abs(sourceList[i] - k.estimateList[i])

            """ select sensors """
            selected = list('0'*count)
            for i in xrange(0,k.threshold):
                    maxScore = -1
                    index = 0
                    for j in xrange(0,count):
                            if score[j]>maxScore:
                                    index = j
                                    maxScore = score[j]
                    selected[index] = '1'
                    score[index] = -1


            """ construct new packet """
            newPacket = []
            newPacket.append("".join(selected))
            for i in xrange(0,count):
                    if selected[i]=='1':
                            newPacket.append(str(sourceList[i]))

            """ update transmitted estimation"""
            for i in xrange(0,count):
                    if selected[i]=='1':
                            k.estimateList[i] = sourceList[i]

            return newPacket 


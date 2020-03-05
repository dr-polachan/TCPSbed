import time
import cv2
import mss
import numpy as np
import pickle
from time import sleep

encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),80]

with mss.mss() as sct:

    # Part of the screen to capture
    monitor = {'top': 0, 'left': 0, 'width': 640, 'height': 480}
    img = np.array(sct.grab(monitor))

    r,g,b,x = cv2.split(img)

    img = cv2.merge([r,g,b])

    frame = img

    arr_obj = [None]*1000 

    mat_image_original = np.zeros(frame.shape, dtype=np.uint8)

    mat_image_estimated = np.zeros(frame.shape, dtype=np.uint8)

    while 'Screen capturing':

        last1_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img = np.array(sct.grab(monitor))
        r,g,b,x = cv2.split(img)
        img = cv2.merge([r,g,b])
        frame = img
    
        mat_image_original = frame

        splitCount = 4
        arr_cell = np.array_split(mat_image_original, splitCount)
      
        index = 0
        
        msg = [None]*splitCount

        for i in range(len(arr_cell)):    

            row_number = arr_cell[i].shape[0]
            
            result,encimg=cv2.imencode('.jpg',arr_cell[i],encode_param) 
            arr_obj[i] = [index, encimg]
            index = index+row_number

            msg[i] = pickle.dumps(arr_obj[i],protocol=1)
            print "size in KB", round(len(msg)/1000.0,0)
            #print "size", len(msg)

        # emulating transverse delay of 5ms
        sleep(5e-3) 

        last_time = time.time()
        
        for i in range (len(arr_cell)):
        ### at receiving side      
            msg_copy = pickle.loads(msg[i])
                  
            cell_index = msg_copy[0]
            cell = msg_copy[1]
            cell=cv2.imdecode(cell,1)    
        ## reconstructing image
            x = cell_index
            mat_image_estimated[x:x+cell.shape[0], 0:0+cell.shape[1]] = cell
        print "time=",round((time.time()-last_time),4)
        
        # Display the picture
        frame = mat_image_estimated

        cv2.imshow('OpenCV/Numpy normal', frame)

        print('fps: {0}'.format(1 / (time.time()-last1_time)))

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break




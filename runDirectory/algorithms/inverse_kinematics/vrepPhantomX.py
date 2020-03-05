### Importing Modules
from __future__ import division
import math
from scipy.optimize import fsolve
import time

solution_listOld = [0, 3, 106, -19, 0] #initial condition
flagConstrainViolation = 0
flagCoverageViolation = 0
   
def py_fsolve(msg_list):

    global solution_listOld
    global flagConstrainViolation
    global flagCoverageViolation

    x = float(msg_list[0])
    y = float(msg_list[1])
    z = float(msg_list[2])
    pitch = float(msg_list[3])
    pincher = int(msg_list[4])
    
    ### robotic arm length
    l1=5; 
    l2=15;
    l3=15;
   	 
    ### checking for out of coverage, see mtech paper
    if ((z-l1)**2 + x**2 + y**2 > (l2+l3)**2):
	flagCoverageViolation = 1		       
    else:	     	
	flagCoverageViolation = 0	   
       
    ### i-kinematics    
    def equations(p):
        x1, x2, x3 = p

        eq1 = l1+15*math.cos(x2)+15*math.cos(x2+x3) - z
        eq2 = (15*math.sin(x2)+15*math.sin(x2+x3))*math.cos(x1) - x
        eq3 = (15*math.sin(x2)+15*math.sin(x2+x3))*math.sin(x1) - y
               
        f=[eq1, eq2, eq3]    
        
        return (f)

    ## solution finder	
    #result = fsolve(equations,(1,1,1))
    result = fsolve(equations,(1,1,1),xtol=.01)
    #[jointAngle1, jointAngle2, jointAngle3, jointAngle4, gripperPos] = solution_listOld
    #x1 = jointAngle1*3.14/180	
    #x2 = jointAngle1*3.14/180
    #x3 = jointAngle1*3.14/180
    #result = fsolve(equations,(x1,x2,x3))	

    # converting to degrees
    x1 = result[0]*180/3.14
    x2 = result[1]*180/3.14
    x3 = result[2]*180/3.14
        
    theta1 = x1;
    theta2 = x2;
    theta3 = x3;
	
    theta4 = 90-(theta2+theta3) # to keep pitch always horizontal to base
	    
    jointAngle1 = (int)(theta1);  # base rotation
    jointAngle2 = (int)(theta2);  
    jointAngle3 = (int)(theta3); 
    jointAngle4 = (int)(theta4);  # pitch joint

    gripperPos = (int) (pincher); # gripper pos to be between 0 (full-close) and 100 (full-open)
    gripperPos = (int) (gripperPos) #if 0=> Full Close, 100=>Full Open

    ## check for joint constraints
    if(flagCoverageViolation == 1):
	print "out of coverage"
	[jointAngle1, jointAngle2, jointAngle3, jointAngle4, gripperPos] = solution_listOld
    if(jointAngle4 < -90 or jointAngle4 > 90):
	flagConstrainViolation = 1
	print "out of contraint j4", jointAngle4
	[jointAngle1, jointAngle2, jointAngle3, jointAngle4, gripperPos] = solution_listOld
    if(jointAngle3 < -135 or jointAngle3 > 135):
	flagConstrainViolation = 1
	print "out of contraint j3", jointAngle3
	[jointAngle1, jointAngle2, jointAngle3, jointAngle4, gripperPos] = solution_listOld	
    if(jointAngle2 < -135 or jointAngle2 > 135):
	flagConstrainViolation = 1
	print "out of contraint j2", jointAngle2
	[jointAngle1, jointAngle2, jointAngle3, jointAngle4, gripperPos] = solution_listOld	
    if(jointAngle1 < -170 or jointAngle1 > 170):
	flagConstrainViolation = 1
	print "out of contraint j1", jointAngle1
	[jointAngle1, jointAngle2, jointAngle3, jointAngle4, gripperPos] = solution_listOld	
    else:
	flagConstrainViolation = 0	
	
    ## backup
    if(flagConstrainViolation == 0 and flagCoverageViolation == 0):
	solution_listOld = [jointAngle1, jointAngle2, jointAngle3, jointAngle4, gripperPos]	
    
    return(jointAngle1,jointAngle2,jointAngle3,jointAngle4,gripperPos) 

#if __name__ == '__main__':
#    print py_fsolve([10,0,15,2,3])
#    print py_fsolve([34,-2,1,2,3])

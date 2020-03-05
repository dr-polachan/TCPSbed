### Importing Modules
from __future__ import division
import math
from scipy.optimize import fsolve
import time


### Defines kinematics algorithm of robots in use
def absolute_method (x,y,z):
    ### Inputs
    X=x;
    Y=y;
    Z=z;
    
    ### Constants
    l1=5;
    l2=15;
    l3=15;
    
    #pinch = 1 # -1.5 to +1.5
    #pitch = 1 # 
    	 
    ### Checking for out of coverage
    if ((Z-l1)**2 + X**2 + Y**2 > (l2+l3)**2):
        a = (l2+l3)**2 - 1 - l1**2
        b = 2*Z*l1
        c = -(X**2 + Y**2 + Z**2)
        k = -b + sqrt(b**2-4*a*c)
        k = k/(2*a)
        k = k.evalf()
    else:
        k=1
        
    X = X/k;
    Y = Y/k;
    Z = Z/k;
            
    #print "K value is : ",k
    ### Angle Computation
    Z1=Z-l1
    check_2=X**2+Y**2+Z1**2
    U=(float(X**2+Y**2+Z1**2+l2**2-l3**2)/float(2*l2))
    V=math.sqrt(X**2+Y**2)
    
    tmp4=float(4*Z1**2*U**2)-float((4*(V**2+Z1**2)*(U**2-V**2)))
    
    if tmp4>=0: #not required check it
        tmp=math.sqrt(tmp4)
        tmp2=((float(2*Z1*U)+float(tmp))/float(2*(V**2+Z1**2)))
        
        tmp3=float((Z1-float((l2*tmp2)))/float(l3))
    
        if X==0:
            theta1=90
            if Y<0:
                theta1=180
            if Y==0:
                theta1=0
        else:
            theta1=math.atan(float(Y)/float(X))*180/3.14
            
        
        theta2=math.acos(tmp2)*180/3.14
        
        theta3=float(math.acos(tmp3)*180/3.14)+float(-1*theta2)
    
        
        x1 = theta1;
        x2 = theta2;
        x3 = theta3;
    
        print x1,x2,x3 # in degrees
    
    ### Dynamixel Steps Computation
    dynafactor = 3.41;#  ie, 1024/300
    pitch_factor = 60;   #   90/1.5
    theta1 = x1;
    theta2 = x2;
    theta3 = x3;
    
    data_1 = (int)(512+(theta1*dynafactor));  #base rotation
    data_2=(int)(512+(theta2*dynafactor)); 
    data_3=(int)(512+((90-theta3)*dynafactor));    # correction for the third motor
    #data_4=(int)(512+(dynafactor*pitch_factor*pitch)); #pitch, palm movement
    #data_5=(int)(512*pinch); #pincher movement
    data_4 = 512;
    data_5 = 512;
       

    #print msg #,"\n"
    
    return(data_1,data_2,data_3,data_4,data_5)



    
def py_fsolve(msg_list):

    x = float(msg_list[0])
    y = float(msg_list[1])
    z = float(msg_list[2])
    pitch = float(msg_list[3])
    pincher = int(msg_list[4])
    
    ### constants robotic arm length
    l1=0; #l=5
    l2=15;
    l3=15;
   	 
    ### checking for out of coverage, see mtech paper
    if ((z-l1)**2 + x**2 + y**2 > (l2+l3)**2):
        #print "hello"
        margin = 5 # 1
        #a = (l2+l3)**2 - margin**2 - l1**2
        a = (l2+l3-margin)**2 - l1**2
        b = 2*z*l1
        c = -(x**2 + y**2 + z**2)
        k = (-b + math.sqrt(b**2-4*a*c))/(2*a)
        
    else:
        k=1
    

    x = x/k;
    y = y/k;
    z = z/k;
    
    #print "debug", k, int(x), int(y), int(z)
    #print "debug", int(x), int(y), int(z),pincher
    ### i-kinematics
    
    def equations(p):
        x1, x2, x3 = p
        #x1 = p
        
        #x=10
        #y=0
        #z=10

        eq1 = l1+15*math.cos(x2)+15*math.cos(x2+x3) - z
        eq2 = (15*math.sin(x2)+15*math.sin(x2+x3))*math.cos(x1) - x
        eq3 = (15*math.sin(x2)+15*math.sin(x2+x3))*math.sin(x1) - y
        
        #f = cos(x1)-0.5    
        
        f=[eq1, eq2, eq3]    
        
        return (f)

    result = fsolve(equations,(1,1,1))
    x1 = result[0]*180/3.14
    x2 = result[1]*180/3.14
    x3 = result[2]*180/3.14
    
    #print x1,x2,x3 # in degrees
    
     ### Dynamixel Steps Computation
    dynafactor = 3.41;#  ie, 1024/300
    pitch_factor = 60;   #   90/1.5
    theta1 = x1;
    theta2 = x2;
    theta3 = x3;
    
    data_1 = (int)(512+(theta1*dynafactor));  #base rotation
    data_2=(int)(512+(theta2*dynafactor)); 
    data_3=(int)(512+((90-theta3)*dynafactor));    # correction for the third motor
    #data_4=(int)(512+(dynafactor*pitch_factor*pitch)); #pitch, palm movement
    #data_5=(int)(512*pinch); #pincher movement
    
    #to keep pitch always horizontal to base
    theta4 = 90-(theta2+theta3)
    data_4 = (int)(512+(theta4*dynafactor));  #base rotation
    data_5 = (int) (pincher);    
    #data_4 = 512;
    #data_5 = 512;
       
    #print msg #,"\n"
    velocity = 50
    #checksum = (data_1 + data_2 + data_3 + data_4 + data_5+ velocity)+1234
    #checksum = (int) (checksum)
    #return(data_1,data_2,data_3,data_4,data_5,velocity,checksum)
    return(data_1,data_2,data_3,data_4,data_5,velocity)


def py_fsolveRev1(msg_list):

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
    

    ### Dynamixel Steps Computation
    dynafactor = 3.41;#  ie, 1024/300
    pitch_factor = 60;   #   90/1.5
    theta1 = jointAngle1;
    theta2 = jointAngle2;
    theta3 = jointAngle3;
    
    data_1 = (int)(512+(theta1*dynafactor)); #base rotation
    data_2=(int)(512+(theta2*dynafactor)); 
    data_3=(int)(512+((90-theta3)*dynafactor)); # correction for the third motor, due to bug in motor connection
    
    #to keep pitch always horizontal to base
    theta4 = 90-(theta2+theta3)
    data_4 = (int)(512+(theta4*dynafactor));  #base rotation
    data_5 = (int) (pincher);    
      
    velocity = 50

    return(data_1,data_2,data_3,data_4,data_5,velocity)

    #return(jointAngle1,jointAngle2,jointAngle3,jointAngle4,gripperPos) 

#if __name__ == '__main__':
#    print py_fsolve([10,0,15,2,3])
#    print py_fsolve([34,-2,1,2,3])

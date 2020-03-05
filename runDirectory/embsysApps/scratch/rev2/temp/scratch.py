import numpy as np
import math
#dcmc1 = np.array([[0.5,0.866],[-0.866,0.5]])



theta = 45
dcmc1 = np.array([	[math.cos(np.radians(theta)), math.cos(np.radians(270+theta))],
			[math.cos(np.radians(90+theta)),math.cos(np.radians(theta))]	])

theta = 55
dcmc2 = np.array([	[math.cos(np.radians(theta)), math.cos(np.radians(270+theta))],
			[math.cos(np.radians(90+theta)),math.cos(np.radians(theta))]	])

dcmc1 = np.round(dcmc1,2)
dcmc2 = np.round(dcmc2,2)

#c = np.array([0, 10]) # point in c1 frame

c2 = np.array([10, 0]) # coordinate in c2 frame

print "dcmc1 is",dcmc1
print "dcmc2 is",dcmc2

#print "global coordinate of point in C1 frame", np.matmul(dcmc1.transpose(),c)

cg = np.matmul(dcmc2.transpose(),c2)
print "point in C2 frame transpoed to global frame", cg

c1 = np.matmul(dcmc1,cg)
print "point in global frame tranposed to c1 frame", c1



#d = np.matmul(dcmc2.transpose(),c)
#print "the intermediate value is",d
#print "the final value is",np.matmul(dcmc1,d)


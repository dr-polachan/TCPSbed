import numpy as np

for i in range(10):
	obj_file = open('data%s.txt' %i, 'w')
	obj_file.write('%s' %i)
	obj_file.close()


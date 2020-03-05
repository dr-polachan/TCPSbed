import os
execfile('generated-file')

os.system("sudo "+vrep_path+" -s "+"vrep/"+vrep_scene)



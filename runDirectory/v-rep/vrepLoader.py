import os
execfile('config')

os.system("sudo "+vrep_path+" -s "+"v-rep/"+vrep_scene)
#os.system("sudo "+vrep_path+" -h -s "+"v-rep/"+vrep_scene) #headless mode



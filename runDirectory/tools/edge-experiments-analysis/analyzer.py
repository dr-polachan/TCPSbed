import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

plt.close('all')

data_file = "../../results/edge-experiments/data.txt"
df = pd.read_csv(data_file)
df["time"]= df["time"]-df["time"][0]

print df.head()
print df.tail()

plt.step(df["time"], df["data"], where='post', linestyle='--', marker='o')
plt.xlabel('time (in seconds)',fontsize=14)
plt.ylabel('gripper-position (0-100)',fontsize=14)
plt.tick_params(labelsize=14)

plt.xlim(0,1)
plt.show()

print "DONE !!!"

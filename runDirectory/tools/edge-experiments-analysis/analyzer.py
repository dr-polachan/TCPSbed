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

df.plot(x='time',y='data')

plt.show()

print "DONE !!!"
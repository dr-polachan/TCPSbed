from scipy import signal
import numpy as np
import matplotlib as plt

a = np.array([[0, 1], [0, 0]])
b = np.array([[0], [1]])
c = np.array([[1, 0]])
d = np.array([[0]])

sys = signal.StateSpace(a, b, c, d)

np.linalg.eig(a)


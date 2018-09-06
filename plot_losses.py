import numpy as np
import matplotlib.pyplot as plt

losses = np.loadtxt('./losses.txt')
plt.plot(losses)
plt.show()
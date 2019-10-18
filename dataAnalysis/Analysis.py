import matplotlib.pyplot as plt
import numpy as np

with open('nodeDataQueue.txt', 'r') as f:
    data = f.readlines()
    raw = np.zeros((15, 3600))
    count = 0
    for val in data:
        raw[count%15][int(count/15)] = float(val)
        count += 1
    
    plt.plot(range(0, 3600), raw[3])
    plt.show()

with open('processSize.txt', 'r') as f:
    pass
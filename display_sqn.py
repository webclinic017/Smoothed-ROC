import matplotlib
import numpy as np

for index, x in np.ndenumerate(dset):
    if x == 1:
        ax.scatter(*index, c = 'red')
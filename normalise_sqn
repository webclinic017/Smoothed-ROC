import numpy as np
sqn = np.load('sqn_1m.npy')
min_val = np.amin(sqn)
sqn = sqn - min_val
max_val = np.amax(sqn)
sqn = sqn / max_val
np.save('sqn_1m_normed.npy', sqn)

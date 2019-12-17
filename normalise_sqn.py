import numpy as np

pair = 'ZILUSDT'
sqn = np.load(f'{pair}_sqn_1m.npy')
min_val = np.amin(sqn)
sqn = sqn - min_val
max_val = np.amax(sqn)
sqn = sqn / max_val
np.save(f'{pair}_sqn_1m_normed.npy', sqn)

import numpy as np

pair = 'BTCUSDT'
sqn = np.load(f'{pair}_sqn_1m.npy')

# find index of result with highest score
sqn_non-zero = sqn.nonzero()
ind_max = np.unravel_index(np.argmax(sqn, axis=None), sqn.shape)
print('Best Settings: {}'.format(ind_max))
print('SQN Score: {:.1f}'.format(sqn[ind_max]))



min_val = np.amin(sqn)
sqn = sqn - min_val
max_val = np.amax(sqn)
sqn = sqn / max_val
np.save(f'{pair}_sqn_1m_normed.npy', sqn)

import numpy as np

pair = 'BNBUSDT'
sqn = np.load(f'results\{pair}_sqn_1m.npy')

# find index of result with highest score
max = np.amax(sqn[sqn != 0])
ind_max = np.argwhere(sqn == max)
print('Best Settings: {}'.format(ind_max*10))
print('SQN Score: {:.1f}'.format(max))



min_val = np.amin(sqn)
sqn = sqn - min_val
max_val = np.amax(sqn)
sqn = sqn / max_val
np.save(f'{pair}_sqn_1m_normed.npy', sqn)

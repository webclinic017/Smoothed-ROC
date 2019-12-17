import numpy as np

def stats(trading_pair):
    a = np.load(f'\results\{trading_pair}_sqn_1m.npy')

    max = np.amax(a[a != 0])
    ind_max = np.argwhere(a == max)

    print(f'Best SQN score: {max:.1f}, settings: {ind_max}')

import numpy as np

def stats(trading_pair):
    a = np.load(f'results\{trading_pair}_sqn_1m.npy')

    max = np.amax(a[a != 0])
    ind_max = np.argwhere(a == max)
    avg = np.mean(a[a != 0])

    print(f'Best SQN score: {max:.1f}, settings: {ind_max}.\nMean SQN score for all settings: {avg:.2f}')
    # if using avg sqn score to compare different strategies or trading pairs, remember that they must all be from the same date range

stats('ZILUSDT')
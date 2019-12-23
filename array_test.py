import numpy as np
from strategies import SmoothedRocStops

def stats(trading_pair):
    a = np.load(f'results\{trading_pair}_sqn_1m.npy')

    max = np.amax(a[a != 0])
    ind_max = np.argwhere(a == max)
    avg = np.mean(a[a != 0])

    print(f'Best SQN score: {max:.1f}, settings: {ind_max*10}.\nMean SQN score for all settings: {avg:.2f}')
    # if using avg sqn score to compare different strategies or trading pairs, remember that they must all be from the same date range

stats('ZILUSDT')

# TODO it might be worth writing a short txt file with each opt run to record param settings, so i know what settings produced each backtest
# TODO or it might even be a better idea to create folders based on param settings so that every results array produced by an opt run automatically goes into a folder with other comparable results arrays

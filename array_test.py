import numpy as np
import math
from pathlib import Path

# TODO Try ang get this working with more intelligent inputs than the strings it is currently using

def stats_sig(s_n, range_str, a, b, rq, date_range, trading_pair):
    data_source = Path(f'Z:/results/{s_n}/{range_str}/sl{a}-{b}\{rq}/{date_range}/sqn/{trading_pair}_1m.npy')
    arr = np.load(data_source)

    max = np.amax(arr)
    ind_max = np.argwhere(arr == max)
    avg = np.mean(arr)

    range_lst = range_str.split(',')
    range_x = range_lst[0].split('-')
    range_x[0], range_x[1] = int(range_x[0]), int(range_x[1])
    x_step = math.ceil((range_x[1] - range_x[0]) / len(arr))
    range_y = range_lst[1].split('-')
    range_y[0], range_y[1] = int(range_y[0]), int(range_y[1])
    y_step = math.ceil((range_y[1] - range_y[0]) / len(arr))
    range_z = range_lst[2].split('-')
    range_z[0], range_z[1] = int(range_z[0]), int(range_z[1])
    z_step = math.ceil((range_z[1] - range_z[0]) / len(arr))

    print(f'Best SQN score: {max:.1f}, settings: {(ind_max[0][0] * x_step) + range_x[0]}, {(ind_max[0][1] * y_step) + range_y[0]}, {(ind_max[0][2] * z_step) + range_z[0]}.\nMean SQN score for all settings: {avg:.2f}')
    print(f'Array shape: {arr.shape}') ### if using avg sqn score to compare different strategies or trading pairs, remember that they must all be from the same date range

def stats_sl(s_n, range_str, x, y, z, rq, date_range, trading_pair):
    data_source = Path(f'Z:/results/{s_n}/{range_str}/{x}-{y}-{z}\{rq}/{date_range}/sqn/{trading_pair}_1m.npy')
    arr = np.load(data_source)

    max = np.amax(arr)
    ind_max = np.argwhere(arr == max)
    avg = np.mean(arr)

    range_lst = range_str.split(',')
    range_a = range_lst[0].split('-')
    range_a[0], range_a[1] = int(range_a[0]), int(range_a[1])
    a_step = math.ceil((range_a[1] - range_a[0]) / len(arr))
    range_b = range_lst[1].split('-')
    range_b[0], range_b[1] = int(range_b[0]), int(range_b[1])
    b_step = math.ceil((range_b[1] - range_b[0]) / len(arr))


    print(f'Best SQN score: {max:.1f}, settings: {(ind_max[0][0] * a_step) + range_a[0]}, {(ind_max[0][1] * b_step) + range_b[0]}.\nMean SQN score for all settings: {avg:.2f}')
    print(f'Array shape: {arr.shape}') ### if using avg sqn score to compare different strategies or trading pairs, remember that they must all be from the same date range

# stats_sig('smoothed-roc-stops', '10-100,10-50,10-100', '50', '50', '20', '2020-01-01_2020-01-30', 'BNBUSDT')

stats_sl('smoothed-roc-stops', '1-100,1-100', '251', '76', '301', '2', '2020-01-01_2020-01-30', 'BNBUSDT')

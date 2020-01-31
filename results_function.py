import os
import numpy as np

def array_func_sl():

    '''function to load/create a numpy array of appropriate size and populate it with results from the strategy object,
    then save the array with a procedurally generated filename'''

    ## initialise or load an array for stats
    if not os.path.exists(f'results_{s_n}\{trading_pair}_{x}-{y}-{z}_sqn_1m.npy'): # for optimising stoploss params
        sqn_array = np.zeros((2, 2))
    else:
        sqn_array = np.load(f'results_{s_n}\{trading_pair}_{x}-{y}-{z}_sqn_1m.npy')# for optimising stoploss params

    for run in opt_runs:
        for strategy in run:
            perc_sell = strategy.params.stop_sell_perc
            perc_buy = strategy.params.stop_buy_perc
            sqn_result = strategy.analyzers.sqn.get_analysis()
            # .get_analysis() returns a dict so use dictionary .get method to retrieve sqn score
            sqn_value = sqn_result.get('sqn')
            print(f'SQN Value:{sqn_value}')
            # store all sqn scores from backtests in a numpy array
            sqn_array[perc_sell][perc_buy] = sqn_value
            ta_analysis = strategy.analyzers.ta.get_analysis()
            print(ta_analysis)

    # find index of result with highest score
    # max = np.amax(sqn_array[sqn_array != 0])  # if all values are below zero, this will ignore the zeros
    # ind_max = np.argwhere(sqn_array == max)

    ### save the array for future recall
    if not os.path.isdir(f'results_{s_n}'):  # checks that the relevant folder exists
        os.mkdir(f'results_{s_n}')  # creates the folder if it doesn't
    # np.save(f'results_{s_n}\{trading_pair}_{x}-{y}-{z}_sqn_1m.npy', sqn_array)    # for optimising stoploss params
    np.save(f'results_{s_n}\{trading_pair}_{a}-{b}_sqn_1m.npy', sqn_array)  # for optimising sroc params

    # print('Best Settings: {}'.format(ind_max * 10))
    # print('SQN Score: {:.1f}'.format(max))


def array_func_sroc(opt_runs, s_n, trading_pair, rq, a, b, roc, sroc, lb, ta_res, sqn_res):

    '''function to load/create a numpy array of appropriate size and populate it with results from the strategy object,
        then save the array with a procedurally generated filename'''

    range_x = roc[1] - roc[0]
    range_y = sroc[1] - sroc[0]
    range_z = lb[1] - lb[0]

    ### initialise an array for sqn stats
    sqn_array = np.zeros((rq, rq, rq))

    for run in opt_runs:
        for strategy in run:
            period1 = int(strategy.params.roc_period * rq/range_x)
            period2 = int(strategy.params.sroc_period * rq/range_y)
            period3 = int(strategy.params.lookback * rq/range_z)
            sqn_result = strategy.analyzers.sqn.get_analysis()
            ### .get_analysis() returns a dict so use dictionary .get method to retrieve sqn score
            sqn_value = sqn_result.get('sqn')
            # print(f'SQN Value:{sqn_value}')
            ### store all sqn scores from backtests in a numpy array
            sqn_array[period1][period2][period3] = sqn_value


    ### save the array for future recall
    if not os.path.isdir(f'results_{s_n}'):  # checks that the relevant folder exists
        os.mkdir(f'results_{s_n}')  # creates the folder if it doesn't

    np.save(f'results_{s_n}\{trading_pair}_{a}-{b}_sqn_1m.npy', sqn_array)  # for optimising sroc params

    ### find index of result with highest score
    max = np.amax(sqn_array[sqn_array != 0])  # if all values are below zero, this will ignore the zeros
    ind_max = np.argwhere(sqn_array == max)

    print('Best Settings: {}'.format(ind_max * 10))
    print('SQN Score: {:.1f}'.format(max))

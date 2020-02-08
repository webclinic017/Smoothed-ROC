import os
import numpy as np
from pathlib import Path
import math

def array_func_sroc(opt_runs, s_n, trading_pair, rq, a, b, roc, sroc, lb, pnl_res, sqn_res, start, end):

    '''function to create a numpy array of appropriate size and populate it with results from the strategy object,
        then save the array with a procedurally generated path and filename'''

    range_x = roc[1] - roc[0]
    range_y = sroc[1] - sroc[0]
    range_z = lb[1] - lb[0]
    range_str = f'{roc[0]}-{roc[1]},{sroc[0]}-{sroc[1]},{lb[0]}-{lb[1]}'

    x_step = math.ceil(range_x / rq)
    y_step = math.ceil(range_y / rq)
    z_step = math.ceil(range_z / rq)

    start_date = str(start)
    end_date = str(end)
    date_range = f'{start_date[:10]}_{end_date[:10]}'

    if sqn_res:
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
        if not os.path.isdir(Path(f'Z:/results')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results'))  # creates the folder if it doesn't
        if not os.path.isdir(Path(f'Z:/results/{s_n}')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results/{s_n}'))  # creates the folder if it doesn't
        if not os.path.isdir(Path(f'Z:/results/{s_n}/{range_str}')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results/{s_n}/{range_str}'))  # creates the folder if it doesn't
        if not os.path.isdir(Path(f'Z:/results/{s_n}/{range_str}/sl{a}-{b}')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results/{s_n}/{range_str}/sl{a}-{b}'))  # creates the folder if it doesn't
        if not os.path.isdir(Path(f'Z:/results/{s_n}/{range_str}/sl{a}-{b}/{rq}')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results/{s_n}/{range_str}/sl{a}-{b}/{rq}'))  # creates the folder if it doesn't
        if not os.path.isdir(Path(f'Z:/results/{s_n}/{range_str}/sl{a}-{b}/{rq}/{date_range}')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results/{s_n}/{range_str}/sl{a}-{b}/{rq}/{date_range}'))  # creates the folder if it doesn't
        if not os.path.isdir(Path(f'Z:/results/{s_n}/{range_str}/sl{a}-{b}/{rq}/{date_range}/sqn')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results/{s_n}/{range_str}/sl{a}-{b}/{rq}/{date_range}/sqn'))  # creates the folder if it doesn't

        np.save(Path(f'Z:/results/{s_n}/{range_str}/sl{a}-{b}/{rq}/{date_range}/sqn/{trading_pair}_1m.npy'), sqn_array)  # for optimising sroc params

        ### find index of result with highest score
        max = np.amax(sqn_array)
        ind_max = np.argwhere(sqn_array == max)
        avg = np.mean(sqn_array)

        print(f'Best SQN score: {max:.1f}, settings: {(ind_max[0][0] * x_step) + roc[0]}, {(ind_max[0][1] * y_step) + sroc[0]}, {(ind_max[0][2] * z_step) + lb[0]}.\nMean SQN score for all settings: {avg:.2f}')

    if pnl_res:
        ### initialise an array for ta stats
        pnl_array = np.zeros((rq, rq, rq))

        for run in opt_runs:
            for strategy in run:
                period1 = int(strategy.params.roc_period * rq / range_x)
                period2 = int(strategy.params.sroc_period * rq / range_y)
                period3 = int(strategy.params.lookback * rq / range_z)
                pnl_value = strategy.analyzers.ta.get_analysis()['pnl']['net']['average']
                ### store all pnl scores from backtests in a numpy array
                pnl_array[period1][period2][period3] = pnl_value

        ### save the array for future recall
        if not os.path.isdir(Path(f'Z:/results')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results'))  # creates the folder if it doesn't
        if not os.path.isdir(Path(f'Z:/results/{s_n}')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results/{s_n}'))  # creates the folder if it doesn't
        if not os.path.isdir(Path(f'Z:/results/{s_n}/{range_str}')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results/{s_n}/{range_str}'))  # creates the folder if it doesn't
        if not os.path.isdir(Path(f'Z:/results/{s_n}/{range_str}/sl{a}-{b}')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results/{s_n}/{range_str}/sl{a}-{b}'))  # creates the folder if it doesn't
        if not os.path.isdir(Path(f'Z:/results/{s_n}/{range_str}/sl{a}-{b}/{rq}')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results/{s_n}/{range_str}/sl{a}-{b}/{rq}'))  # creates the folder if it doesn't
        if not os.path.isdir(Path(f'Z:/results/{s_n}/{range_str}/sl{a}-{b}/{rq}/{date_range}')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results/{s_n}/{range_str}/sl{a}-{b}/{rq}/{date_range}'))  # creates the folder if it doesn't
        if not os.path.isdir(Path(f'Z:/results/{s_n}/{range_str}/sl{a}-{b}/{rq}/{date_range}/pnl')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results/{s_n}/{range_str}/sl{a}-{b}/{rq}/{date_range}/pnl'))  # creates the folder if it doesn't

        np.save(Path(f'Z:/results/{s_n}/{range_str}/sl{a}-{b}/{rq}/{date_range}/pnl/{trading_pair}_1m.npy'), pnl_array)  # for optimising sroc params

        ### find index of result with highest score
        max = np.amax(pnl_array)
        ind_max = np.argwhere(pnl_array == max)
        avg = np.mean(pnl_array)

        print(f'Best PnL score: {max:.1f}, settings: {(ind_max[0][0] * x_step) + roc[0]}, {(ind_max[0][1] * y_step) + sroc[0]}, {(ind_max[0][2] * z_step) + lb[0]}.\nMean PnL score for all settings: {avg:.2f}')

# TODO get array_func_sl working the same way as array_func_roc

def array_func_sl(opt_runs, s_n, trading_pair, rq, x, y, z, ss, sb, pnl_res, sqn_res, start, end):

    '''function to create a numpy array of appropriate size and populate it with results from the strategy object,
        then save the array with a procedurally generated path and filename'''

    range_a = ss[1] - ss[0]
    range_b = sb[1] - sb[0]
    range_str = f'{ss[0]}-{ss[1]},{sb[0]}-{sb[1]}'

    a_step = math.ceil(range_a / rq)
    b_step = math.ceil(range_b / rq)

    start_date = str(start)
    end_date = str(end)
    date_range = f'{start_date[:10]}_{end_date[:10]}'

    if sqn_res:
        ### initialise an array for sqn stats
        sqn_array = np.zeros((rq, rq))

        for run in opt_runs:
            for strategy in run:
                period1 = int(strategy.params.stop_sell_perc * rq/range_a)
                period2 = int(strategy.params.stop_buy_perc * rq/range_b)
                sqn_result = strategy.analyzers.sqn.get_analysis()
                ### .get_analysis() returns a dict so use dictionary .get method to retrieve sqn score
                sqn_value = sqn_result.get('sqn')
                # print(f'SQN Value:{sqn_value}')
                ### store all sqn scores from backtests in a numpy array
                sqn_array[period1][period2] = sqn_value


        ### save the array for future recall
        if not os.path.isdir(Path(f'Z:/results')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results'))  # creates the folder if it doesn't
        if not os.path.isdir(Path(f'Z:/results/{s_n}')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results/{s_n}'))  # creates the folder if it doesn't
        if not os.path.isdir(Path(f'Z:/results/{s_n}/{range_str}')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results/{s_n}/{range_str}'))  # creates the folder if it doesn't
        if not os.path.isdir(Path(f'Z:/results/{s_n}/{range_str}/{x}-{y}-{z}')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results/{s_n}/{range_str}/{x}-{y}-{z}'))  # creates the folder if it doesn't
        if not os.path.isdir(Path(f'Z:/results/{s_n}/{range_str}/{x}-{y}-{z}/{rq}')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results/{s_n}/{range_str}/{x}-{y}-{z}/{rq}'))  # creates the folder if it doesn't
        if not os.path.isdir(Path(f'Z:/results/{s_n}/{range_str}/{x}-{y}-{z}/{rq}/{date_range}')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results/{s_n}/{range_str}/{x}-{y}-{z}/{rq}/{date_range}'))  # creates the folder if it doesn't
        if not os.path.isdir(Path(f'Z:/results/{s_n}/{range_str}/{x}-{y}-{z}/{rq}/{date_range}/sqn')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results/{s_n}/{range_str}/{x}-{y}-{z}/{rq}/{date_range}/sqn'))  # creates the folder if it doesn't

        np.save(Path(f'Z:/results/{s_n}/{range_str}/{x}-{y}-{z}/{rq}/{date_range}/sqn/{trading_pair}_1m.npy'), sqn_array)  # for optimising sroc params

        ### find index of result with highest score
        max = np.amax(sqn_array)
        ind_max = np.argwhere(sqn_array == max)
        avg = np.mean(sqn_array)

        print(f'Best SQN score: {max:.1f}, settings: {(ind_max[0][0] * a_step) + ss[0]}, {(ind_max[0][1] * b_step) + sb[0]}.\nMean SQN score for all settings: {avg:.2f}')

    if pnl_res:
        ### initialise an array for ta stats
        pnl_array = np.zeros((rq, rq))

        for run in opt_runs:
            for strategy in run:
                period1 = int(strategy.params.stop_sell_perc * rq / range_a)
                period2 = int(strategy.params.stop_buy_perc * rq / range_b)
                pnl_value = strategy.analyzers.ta.get_analysis()['pnl']['net']['average']
                ### store all pnl scores from backtests in a numpy array
                pnl_array[period1][period2] = pnl_value

        ### save the array for future recall
        if not os.path.isdir(Path(f'Z:/results')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results'))  # creates the folder if it doesn't
        if not os.path.isdir(Path(f'Z:/results/{s_n}')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results/{s_n}'))  # creates the folder if it doesn't
        if not os.path.isdir(Path(f'Z:/results/{s_n}/{range_str}')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results/{s_n}/{range_str}'))  # creates the folder if it doesn't
        if not os.path.isdir(Path(f'Z:/results/{s_n}/{range_str}/{x}-{y}-{z}')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results/{s_n}/{range_str}/{x}-{y}-{z}'))  # creates the folder if it doesn't
        if not os.path.isdir(Path(f'Z:/results/{s_n}/{range_str}/{x}-{y}-{z}/{rq}')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results/{s_n}/{range_str}/{x}-{y}-{z}/{rq}'))  # creates the folder if it doesn't
        if not os.path.isdir(Path(f'Z:/results/{s_n}/{range_str}/{x}-{y}-{z}/{rq}/{date_range}')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results/{s_n}/{range_str}/{x}-{y}-{z}/{rq}/{date_range}'))  # creates the folder if it doesn't
        if not os.path.isdir(Path(f'Z:/results/{s_n}/{range_str}/{x}-{y}-{z}/{rq}/{date_range}/pnl')):  # checks that the relevant folder exists
            os.mkdir(Path(f'Z:/results/{s_n}/{range_str}/{x}-{y}-{z}/{rq}/{date_range}/pnl'))  # creates the folder if it doesn't

        np.save(Path(f'Z:/results/{s_n}/{range_str}/{x}-{y}-{z}/{rq}/{date_range}/pnl/{trading_pair}_1m.npy'), pnl_array)  # for optimising sroc params

        ### find index of result with highest score
        max = np.amax(pnl_array)
        ind_max = np.argwhere(pnl_array == max)
        avg = np.mean(pnl_array)

        print(f'Best PnL score: {max:.1f}, settings: {(ind_max[0][0] * a_step) + ss[0]}, {(ind_max[0][1] * b_step) + sb[0]}.\nMean PnL score for all settings: {avg:.2f}')


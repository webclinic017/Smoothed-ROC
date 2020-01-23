import backtrader as bt
import backtrader.feeds as btfeeds
import os
import datetime
import time
import numpy as np
from sizers import PercentSizer
from strategies import SmoothedRocStops

if __name__ == '__main__':

    t_start = time.perf_counter()
    startcash = 1000
    trading_pair = 'BNBUSDT'
    strategy_name = SmoothedRocStops
    counter = {'counter' : 0}


    cerebro = bt.Cerebro(stdstats=False,optreturn=True,optdatas=True,exactbars=True)
    cerebro.optstrategy(SmoothedRocStops,
                        roc_period=range(10, 1000, 50),    # for optimising sroc params
                        sroc_period=range(10, 500, 25),    # for optimising sroc params
                        lookback=range(10, 1000, 50),      # for optimising sroc params
                        # stop_sell_perc=range(1, 3),         # for optimising stoploss params
                        # stop_buy_perc=range(1, 3),          # for optimising stoploss params
                        start=t_start)
    cerebro.optstrategy(SmoothedRocStops, start=t_start)

    datapath = os.path.abspath(os.getcwd() + f'\Data\{trading_pair}-1m-data.csv')

    # Create a data feed
    data = btfeeds.GenericCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2019, 1, 1),
        todate=datetime.datetime(2019,1,2),
        dtformat=('%Y-%m-%d %H:%M:%S'),
        datetime=0,
        high=2,
        low=3,
        open=1,
        close=4,
        volume=5,
        openinterest=-1,
        timeframe=bt.TimeFrame.Minutes,
        compression=1
    )

    cerebro.adddata(data)

    cerebro.broker.setcash(startcash)

    cerebro.addsizer(PercentSizer)

    # cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='ta')
    # TODO work out what tradeanalyzer does and if it would be useful for stats
    # cerebro.addanalyzer(bt.analyzers.SQN, _name='sqn')

    cerebro.broker.setcommission(commission=0.0075)

    opt_runs = cerebro.run()



    # x = SmoothedRocStops.params.roc_period
    # y = SmoothedRocStops.params.sroc_period
    # z = SmoothedRocStops.params.lookback
    # a = SmoothedRocStops.params.stop_sell_perc
    # b = SmoothedRocStops.params.stop_buy_perc
    #
    # # initialise or load an array for stats
    # if not os.path.exists(f'results_smoothed-roc-stops\{trading_pair}_{x}-{y}-{z}_sqn_1m.npy'): # for optimising stoploss params
    #     sqn_array = np.zeros((2, 2))
    # else:
    #     sqn_array = np.load(f'results_smoothed-roc-stops\{trading_pair}_{x}-{y}-{z}_sqn_1m.npy')# for optimising stoploss params
    #
    # for run in opt_runs:
    #     for strategy in run:
    #         perc_sell = strategy.params.stop_sell_perc
    #         perc_buy = strategy.params.stop_buy_perc
    #         sqn_result = strategy.analyzers.sqn.get_analysis()
    #         # .get_analysis() returns a dict so use dictionary .get method to retrieve sqn score
    #         sqn_value = sqn_result.get('sqn')
    #         print(f'SQN Value:{sqn_value}')
    #         # store all sqn scores from backtests in a numpy array
    #         sqn_array[perc_sell][perc_buy] = sqn_value
    #         ta_analysis = strategy.analyzers.ta.get_analysis()
    #         print(ta_analysis)
    #
    # # initialise or load an array for stats
    # if not os.path.exists(f'results_smoothed-roc-stops\{trading_pair}_{a}-{b}_sqn_1m.npy'):  # for optimising sroc params
    #     sqn_array = np.zeros((100, 50, 100))
    # else:
    #     sqn_array = np.load(f'results_smoothed-roc-stops\{trading_pair}_{a}-{b}_sqn_1m.npy')  # for optimising sroc params
    #
    # for run in opt_runs:
    #     for strategy in run:
    #         period1 = int(strategy.params.roc_period * 0.1)
    #         period2 = int(strategy.params.sroc_period * 0.1)
    #         period3 = int(strategy.params.lookback * 0.1)
    #         sqn_result = strategy.analyzers.sqn.get_analysis()
    #         # .get_analysis() returns a dict so use dictionary .get method to retrieve sqn score
    #         sqn_value = sqn_result.get('sqn')
    #         print(f'SQN Value:{sqn_value}')
    #         # store all sqn scores from backtests in a numpy array
    #         sqn_array[period1][period2][period3] = sqn_value
    #         ta_analysis = strategy.analyzers.ta.get_analysis()
    #         print(ta_analysis)

# TODO find a way to automatically create a folder with a procedurally generated name


    # find index of result with highest score
    # max = np.amax(sqn_array[sqn_array != 0])  # if all values are below zero, this will ignore the zeros
    # ind_max = np.argwhere(sqn_array == max)

    t_end = time.perf_counter()
    total_time = t_end - t_start

    # save the array for future recall
    # np.save(f'results_smoothed-roc-stops\{trading_pair}_{x}-{y}-{z}_sqn_1m.npy', sqn_array)     # for optimising stoploss params
    # np.save(f'results_{str(strategy_name)}\{trading_pair}_{x}-{y}-{z}_sqn_1m.npy', sqn_array) # this is how i want the previous line to work
    np.save(f'results_{str(strategy_name)}\{trading_pair}_{a}-{b}_sqn_1m.npy', sqn_array)     # for optimising sroc params
    # TODO maybe solve this problem by putting the strategy in a dictionary and referencing the dictionary key here


    print('Backtest took:{}h {}m'.format(int(total_time/3600), int(total_time/60)%60))
    # print('Best Settings: {}'.format(ind_max * 10))
    # print('SQN Score: {:.1f}'.format(max))

import backtrader as bt
import backtrader.feeds as btfeeds
import os
import datetime
import time
import numpy as np
from strategies import SmoothedROC
from strategies import SmoothedRocStops
import math

t_start = time.perf_counter()

class PercentSizer(bt.Sizer):
    '''This sizer return percents of available cash
    Params:
      - ``percents`` (default: ``20``)
    '''

    params = (
        ('percents', 99),
        ('retint', False),  # return an int size or rather the float value
    )

    def __init__(self):
        pass

    def _getsizing(self, comminfo, cash, data, isbuy):
        position = self.broker.getposition(data)
        if not position:
            size = cash / data.close[0] * (self.params.percents / 100)
        else:
            size = position.size

        if self.p.retint:
            size = int(size)

        return size


if __name__ == '__main__':

    startcash = 1000
    trading_pair = 'BNBUSDT'
    strategy_name = SmoothedRocStops

    ############### results function ####################

    # array_x = 100
    # array_y = 50
    # array_z = 100
    #
    # results_range_min_x = 1
    # results_range_max_x = 1000
    # results_range_min_y = 5
    # results_range_max_y = 500
    # results_range_min_z = 1
    # results_range_max_z = 1000
    #
    # results_amount_x = 20
    # results_amount_y = 20
    # results_amount_z = 20

    # step_size_x = math.ceil((results_range_max_x - results_range_min_x), results_amount_x

    ############### results function ####################

    cerebro = bt.Cerebro(stdstats=False,optreturn=True,optdatas=True)
    # cerebro.optstrategy(SmoothedROC, roc_period=range(10, 1000, 50), sroc_period=range(10, 500, 25),lookback=range(10, 1000, 50), start=t_start)
    cerebro.optstrategy(strategy_name, stop_sell_perc = range(1, 41, 2), stop_buy_perc = range(1, 41, 2), start=t_start)

    datapath = os.path.abspath(os.getcwd() + f'\Data\{trading_pair}-1m-data.csv')

    # Create a data feed
    data = btfeeds.GenericCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2019, 1, 1),
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

    #cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='ta')
    # TODO work out what tradeanalyzer does and if it would be useful for stats
    cerebro.addanalyzer(bt.analyzers.SQN, _name='sqn')

    cerebro.broker.setcommission(commission=0.0075)

    opt_runs = cerebro.run()



    x = SmoothedRocStops.params.roc_period
    y = SmoothedRocStops.params.sroc_period
    z = SmoothedRocStops.params.lookback
    a = SmoothedRocStops.params.stop_sell_perc
    b = SmoothedRocStops.params.stop_buy_perc

    # initialise or load an array for stats
    if not os.path.exists(f'results_{str(strategy_name)}\{trading_pair}_{x}-{y}-{z}_sqn_1m.npy'):
        sqn_array = np.zeros((41, 41))
    else:
        sqn_array = np.load(f'results_{str(strategy_name)}\{trading_pair}_{x}-{y}-{z}_sqn_1m.npy')

    for run in opt_runs:
        for strategy in run:
            perc_sell = int(strategy.params.stop_sell_perc)
            perc_buy = int(strategy.params.stop_buy_perc)
            sqn_result = strategy.analyzers.sqn.get_analysis()
            # .get_analysis() returns a dict so use dictionary .get method to retrieve sqn score
            sqn_value = sqn_result.get('sqn')
            # store all sqn scores from backtests in a numpy array
            sqn_array[perc_sell][perc_buy] = sqn_value

    # # initialise or load an array for stats
    # if not os.path.exists(f'{trading_pair}_sqn_1m.npy'):
    #     sqn_array = np.zeros((100, 50, 100))
    # else:
    #     sqn_array = np.load(f'results\{trading_pair}_sqn_1m.npy')
    #
    # for run in opt_runs:
    #     for strategy in run:
    #         period1 = int(strategy.params.roc_period * 0.1)
    #         period2 = int(strategy.params.sroc_period * 0.1)
    #         period3 = int(strategy.params.lookback * 0.1)
    #         sqn_result = strategy.analyzers.sqn.get_analysis()
    #         # .get_analysis() returns a dict so use dictionary .get method to retrieve sqn score
    #         sqn_value = sqn_result.get('sqn')
    #         # store all sqn scores from backtests in a numpy array
    #         sqn_array[period1][period2][period3] = sqn_value



    # find index of result with highest score
    max = np.amax(sqn_array[sqn_array != 0])  # if all values are below zero, this will ignore the zeros
    ind_max = np.argwhere(sqn_array == max)

    t_end = time.perf_counter()
    total_time = t_end - t_start

    # save the array for future recall
    np.save(f'results_{str(strategy_name)}\{trading_pair}_{x}-{y}-{z}_sqn_1m.npy', sqn_array)
    # np.save(f'results_{strategy_name}\{trading_pair}_{a}-{b}_sqn_1m.npy', sqn_array)

    print('Backtest took:{}h {}m'.format(int(total_time/3600), int(total_time/60)%60))
    print('Best Settings: {}'.format(ind_max * 10))
    print('SQN Score: {:.1f}'.format(max))

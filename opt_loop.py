import backtrader as bt
import backtrader.feeds as btfeeds
import os
import datetime
import time
from sizers import PercentSizer
from strategies import SmoothedRoc
from strategies import SmoothedRocStops
import extensions as ex
import results_function as rf
from pathlib import Path

pairs = ex.get_pairs('USDT')

for i in pairs:
    startcash = 1000
    trading_pair = i
    strat = SmoothedRocStops
    s_n = strat.params.strat_name      # name of current strategy as a string for generating filenames etc
    pnl_results = True
    sqn_results = True
    signal_or_sl = False                 # True if optimising signal params, False if optimising stoploss params
    start_date = datetime.datetime(2020, 1, 1)
    end_date = datetime.datetime(2020, 1, 30)

    ### optimisation params
    rq = 2           # results quantity
    roc = (10, 100)   # roc range
    sroc = (10, 50)   # sroc range
    lb = (10, 100)    # lookback range
    ss = (1, 100)       # stop sell range
    sb = (1, 100)       # stop buy range
    size = 99

    r_step = ex.param_step(rq, roc[0], roc[1])
    sr_step = ex.param_step(rq, sroc[0], sroc[1])
    lb_step = ex.param_step(rq, lb[0], lb[1])
    ss_step = ex.param_step(rq, ss[0], ss[1])
    sb_step = ex.param_step(rq, sb[0], sb[1])


    cerebro = bt.Cerebro(
        stdstats=False,
        optreturn=True,
        optdatas=True,
        # exactbars=True            # This was the cause of the 'deque index out of range' issue
    )

    t_start = time.perf_counter()

    if signal_or_sl:
        cerebro.optstrategy(strat,
                            roc_period=range(roc[0], roc[1], r_step),
                            sroc_period=range(sroc[0], sroc[1], sr_step),
                            lookback=range(lb[0], lb[1], lb_step),
                            start=t_start)
    else:
        cerebro.optstrategy(strat,
                            stop_sell_perc=range(ss[0], ss[1], ss_step),
                            stop_buy_perc=range(sb[0], sb[1], ss_step),
                            start=t_start)


    datapath = Path(f'Z:/Data/{trading_pair}-1m-data.csv')

    # Create a data feed
    data = btfeeds.GenericCSVData(
        dataname=datapath,
        fromdate=start_date,
        todate=end_date,
        dtformat=('%Y-%m-%d %H:%M:%S'),
        datetime=0, high=2, low=3, open=1, close=4, volume=5, openinterest=-1,
        timeframe=bt.TimeFrame.Minutes,
        compression=1
    )

    # if signal_or_sl:
    #     rt = rq**3
    # else:
    #     rt = rq**2
    # run_counter = 0
    # def cb(SmoothedRocStops):
    #     global run_counter
    #     global t_start
    #     global rt
    #     run_counter += 1
    #     if run_counter%100 == 0:
    #         t_elapsed = time.perf_counter()
    #         elapsed = t_elapsed - t_start
    #         hours = elapsed // 3600
    #         minutes = elapsed // 60
    #         print('-')
    #         print(f'Runs completed: {run_counter}/{rt}, Time elapsed:{int(hours)}h {int(minutes % 60)}m')

    cerebro.adddata(data)
    cerebro.broker.setcash(startcash)
    cerebro.addsizer(PercentSizer)
    PercentSizer.params.percents = size
    cerebro.broker.setcommission(commission=0.00075)
    # cerebro.optcallback(cb)

    if pnl_results:
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='ta')
    if sqn_results:
        cerebro.addanalyzer(bt.analyzers.SQN, _name='sqn')


    if __name__ == '__main__':

        print(f'Running {trading_pair} tests')

        opt_runs = cerebro.run()

        a = strat.params.stop_sell_perc
        b = strat.params.stop_buy_perc
        x = strat.params.roc_period
        y = strat.params.sroc_period
        z = strat.params.lookback

        if signal_or_sl:
            rf.array_func_sroc(opt_runs, s_n, trading_pair, rq, a, b, roc, sroc, lb, pnl_results, sqn_results, start_date, end_date)
        else:
            rf.array_func_sl(opt_runs, s_n, trading_pair, rq, x, y, z, ss, sb, pnl_results, sqn_results, start_date, end_date)

        t_end = time.perf_counter()
        t = t_end - t_start
        hours = t // 3600
        minutes = t // 60
        print(f'Time elapsed:{int(hours)}h {int(minutes%60)}m')

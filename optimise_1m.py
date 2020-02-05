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

startcash = 1000
trading_pair = 'ETHUSDT'
strat = SmoothedRocStops
s_n = strat.params.strat_name      # name of current strategy as a string for generating filenames etc
run_counter = 0           # TODO implement run counter
pnl_results = False
sqn_results = True
signal_or_sl = True                 # True if optimising signal params, False if optimising stoploss params
start_date = datetime.datetime(2020, 1, 1)
end_date = datetime.datetime(2020, 1, 30)

### optimisation params
rq = 2           # results quantity
roc = (10, 100)   # roc range
sroc = (10, 50)   # sroc range
lb = (10, 100)    # lookback range
ss = (1, 5)       # stop sell range
sb = (1, 5)       # stop buy range

r_step = ex.param_step(rq, roc[0], roc[1])
sr_step = ex.param_step(rq, sroc[0], sroc[1])
lb_step = ex.param_step(rq, lb[0], lb[1])


cerebro = bt.Cerebro(
    stdstats=False,
    optreturn=True,
    optdatas=True,
    # exactbars=True            # This was the cause of the 'deque index out of range' issue
)

t_start = time.perf_counter()

cerebro.optstrategy(strat,
                    roc_period=range(roc[0], roc[1], r_step),
                    sroc_period=range(sroc[0], sroc[1], sr_step),
                    lookback=range(lb[0], lb[1], lb_step),
                    # stop_sell_perc=range(ss[0], ss[1]),
                    # stop_buy_perc=range(sb[0], sb[1]),
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

cerebro.adddata(data)
cerebro.broker.setcash(startcash)
cerebro.addsizer(PercentSizer)
cerebro.broker.setcommission(commission=0.00075)

if ta_results:
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='ta')
if sqn_results:
    cerebro.addanalyzer(bt.analyzers.SQN, _name='sqn')


if __name__ == '__main__':

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

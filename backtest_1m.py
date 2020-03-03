import backtrader as bt
import backtrader.feeds as btfeeds
import datetime
import time
from sizers import PercentSizer
import matplotlib
from strategies import SmoothedRoc
from strategies import SmoothedRocStops
from extensions import printTradeAnalysis

startcash = 1000
trading_pair = 'BTCUSDT'
strat = SmoothedRocStops
s_n = strat.params.strat_name
roc = 251
sroc = 76
lb = 301
ss = 50
sb = 50
start_date = datetime.datetime(2020, 1, 1)
end_date = datetime.datetime(2020, 1, 30)        # Can cause errors if too close to start_date

t_start = time.perf_counter()

cerebro = bt.Cerebro()
if strat == SmoothedRocStops:
    cerebro.addstrategy(strat, roc_period=roc, sroc_period=sroc, lookback=lb, stop_sell_perc=ss, stop_buy_perc=sb, start=t_start)
elif strat == SmoothedRoc:
    cerebro.addstrategy(strat, roc_period=roc, sroc_period=sroc, lookback=lb, start=t_start)
datapath = f'Z:\Data\{trading_pair}-1m-data.csv'

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
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='ta')
cerebro.addanalyzer(bt.analyzers.SQN, _name='sqn')




if __name__ == '__main__':
    strategy_list = cerebro.run()   # this returns a list of strategy objects even if there is only 1 strat to return
    first = strategy_list[0]        # so we just extract the first (and only) object from the list for anaylsis

    # t_end = time.perf_counter()
    # total_time = t_end - t_start

    printTradeAnalysis(first.analyzers.ta.get_analysis())
    sqn_result = first.analyzers.sqn.get_analysis()
    # .get_analysis() returns a dict so use dictionary .get method to retrieve sqn score
    sqn_value = sqn_result.get('sqn')

    print(f'Starting Balance: {startcash}')
    print('Final Balance: %.2f' % cerebro.broker.getvalue())
    print(f'SQN Score: {sqn_value:.1f}')

    # ta_dict = first.analyzers.ta.get_analysis()
    # print(ta_dict.keys())
    # print(ta_dict['pnl']['net'])
    # print(first.analyzers.ta.get_analysis()['pnl']['net']['total'])

    cerebro.plot()

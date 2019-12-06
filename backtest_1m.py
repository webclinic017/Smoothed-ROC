import backtrader as bt
import backtrader.feeds as btfeeds
import os
import datetime
import time
import math
import matplotlib

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

class SmoothedROC(bt.Strategy):

    params = (
        ('roc_period', 18000),
        ('sroc_period', 6000),
        ('lookback', 12000),
        ('debug', True),
        )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        #print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.startcash = self.broker.getvalue()
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.roc = bt.indicators.ROC(self.data.close, period=self.params.roc_period)
        self.sroc = bt.indicators.SMA(self.roc, period=self.params.sroc_period)
        self.lookback = self.params.lookback


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Nothing to do since order was submitted/accepted to/by broker
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm: %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm: %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return

        if not self.position:

            if self.sroc > self.sroc[-self.lookback]:

                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()

            elif self.sroc < self.sroc[-self.lookback]:

                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()

        else:

            if self.sroc > self.sroc[-self.lookback]:
                if self.position.size < 0:
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.close()
                    self.order = self.buy()

            elif self.sroc < self.sroc[-self.lookback]:
                if self.position.size > 0:
                    self.log('SELL CREATE, %.2f' % self.dataclose[0])
                    self.order = self.close()
                    self.order = self.sell()

        if self.p.debug:
            print('---------------------------- NEXT ----------------------------------')
            #print("1: Data Name:                            {}".format(data._name))
            #print("2: Bar Num:                              {}".format(len(data)))
            print("3: Current date:                         {}".format(data.datetime.datetime()))
            #print('4: Open:                                 {}'.format(data.open[0]))
            #print('5: High:                                 {}'.format(data.high[0]))
            #print('6: Low:                                  {}'.format(data.low[0]))
            print('7: Close:                                {}'.format(data.close[0]))
            #print('8: Volume:                               {}'.format(data.volume[0]))
            print('9: Position Size:                        {}'.format(self.position.size))
            print('--------------------------------------------------------------------')

if __name__ == '__main__':

    startcash = 1000

    cerebro = bt.Cerebro()
    cerebro.addstrategy(SmoothedROC)
    datapath = os.path.abspath(os.getcwd() + '/BTC_1m_' + str(datetime.datetime.now().strftime("%Y_%m_%d")))

    # Create a data feed
    data = btfeeds.GenericCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2019, 6, 1),
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
    #cerebro.addanalyzer(bt.analyzers.SQN, _name='sqn')

    cerebro.broker.setcommission(commission=0.0075)

    print('Starting Balance: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    #sqn_result = cerebro.analyzers.sqn.get_analysis()
    # .get_analysis() returns a dict so use dictionary .get method to retrieve sqn score
    #sqn_value = sqn_result.get('sqn')

    t_end = time.perf_counter()
    total_time = t_end - t_start

    print('Backtest took:{}h {}m'.format(int(total_time/3600), int(total_time/60)%60))
    print('Final Balance: %.2f' % cerebro.broker.getvalue())
    #print('SQN Score: {:.1f}'.format(sqn_value))

    cerebro.plot()

import datetime
import backtrader as bt


class SmoothedROC(bt.Strategy):

    params = (
        ('roc_period', 1800),
        ('sroc_period', 600),
        ('lookback', 1200),
        ('debug', False),
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
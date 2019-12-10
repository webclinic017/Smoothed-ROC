# Smoothed-ROC

This long-short strategy uses an SMA-smoothed ROC (rate of change) indicator to determine when an asset is trending up or down. It doesn't currently use a trailing stop to close positions but i do plan to include that in the strategy.

get_all_data.py is the best way to download/update all price history for the trading pair/pairs that need to be backtested. run this before each backtest.

optimise_1m.py runs an optimisation session to determine the best settings to use for a given strategy on a given trading pair.

backtest_1m.py runs a backtest of a single set of parameters. run this using the settings that optimisation has suggested will be best to analyse trades in more detail and investigate te reliability of optimisation.

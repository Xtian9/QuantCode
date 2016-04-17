# QuantCode

Quant research and backtesting system

## Installation

Requires pandas, numpy, and matplotlib

Source setup in every new session
```shell
source setup.sh
```

## Run a backtest

1. Define backtest in config file, e.g. backtests/buynhold/buynhold_cfg.py

2. Choose symbols, date start and end, trading frequency, price to trade on (open or close)

3. Define a Strategy, Portfolio, and Analyser to backtest on and run with:
```shell
python buynhold_cfg.py
```

## Create your own backtest modules

- Strategy class generates signals
  
  +1 long, -1 short, 0 cash

- Portfolio class generates positions and compute returns

  e.g. define in dollar amount the fractions (weights) of total capital invested in each asset
  
- Analyser class analyses the performnance of the backtest 

  e.g. equity curve, Sharpe ratio, etc.


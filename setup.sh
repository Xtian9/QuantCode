export QUANTCODEDIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd $QUANTCODEDIR

export PYTHONPATH=${PYTHONPATH}:${PWD}
export PYTHONPATH=${PYTHONPATH}:${PWD}/analysers
export PYTHONPATH=${PYTHONPATH}:${PWD}/backtests
export PYTHONPATH=${PYTHONPATH}:${PWD}/core
export PYTHONPATH=${PYTHONPATH}:${PWD}/portfolios
export PYTHONPATH=${PYTHONPATH}:${PWD}/strategies

#python splash.py
echo "Welcome to QuantCode"

cd - > /dev/null

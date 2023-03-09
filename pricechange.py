import ccxt
import pandas as pd
import time

# Инициализация биржи Binance
exchange = ccxt.binance()

# Выбор символа ETHUSDT
symbol_eth = 'ETH/USDT'
# Выбор символа BTCUSDT
symbol_btc = 'BTC/USDT'

# Определение временного интервала
timeframe = '1h'

# Цикл для непрерывного мониторинга цены
while True:
# Получение исторических данных за последние 60 минут
    data_btc = exchange.fetch_ohlcv(symbol_btc, timeframe)
    df_btc = pd.DataFrame(data_btc, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df_btc['timestamp'] = pd.to_datetime(df_btc['timestamp'], unit='ms')
    df_btc.set_index('timestamp', inplace=True)
    df_btc = df_btc.tail(60)

    data_eth = exchange.fetch_ohlcv(symbol_eth, timeframe)
    df_eth = pd.DataFrame(data_eth, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df_eth['timestamp'] = pd.to_datetime(df_eth['timestamp'], unit='ms')
    df_eth.set_index('timestamp', inplace=True)
    df_eth = df_eth.tail(60)

# Рассчет процентного изменения цены
    price_change_btc = ((df_btc['close'][-1] - df_btc['close'][0]) / df_btc['close'][0]) * 100
    price_change_eth = ((df_eth['close'][-1] - df_eth['close'][0]) / df_eth['close'][0]) * 100

# Рассчет влияния курса BTCUSDT
    if (price_change_eth > 0 and price_change_btc > 0) and (price_change_eth > price_change_btc):
        true_price_change_eth = price_change_eth - price_change_btc
    elif (price_change_eth < 0 and price_change_btc < 0) and (price_change_eth < price_change_btc):
        true_price_change_eth = price_change_eth - price_change_btc
    elif price_change_eth > 0 and price_change_btc < 0:
        true_price_change_eth = price_change_eth
    elif price_change_eth < 0 and price_change_btc > 0:
        true_price_change_eth = price_change_eth
    else:
        true_price_change_eth = 0

# Если процентное изменение превышает 1%, выводим сообщение в консоль
    if abs(true_price_change_eth) > 1:
        print(f'Price change for {symbol_eth}: {true_price_change_eth:.2f}%')

# Задержка в 1 минуту
    time.sleep(60)

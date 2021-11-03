import os
import environ
import asyncio
import datetime
import pandas
import json
import time
from binance import Client
from websock.settings import BASE_DIR

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

api_key = env('API_KEY')
api_secret = env('API_SECRET')

# technical_analysis = "EMA"
# technical_analysis = "SMA"
technical_analysis = env('TECHNICAL_ANALYSIS')

# currentCurrency = "ETH"
# currentCurrency = "BNB"
# currentCurrency = "NEO"
# currentCurrency = "FIL"
currentCurrency = env('CURRENT_CURRENCY')

# baseCurrency = "BTC"
baseCurrency = env('BASE_CURRENCY')

# currentDuration = "30 minutes ago UTC"
currentDuration = env('CURRENT_DURATION')

# baseDuration = "1 day ago UTC"
baseDuration = env('BASE_DURATION')


# period_time = 15
period_time = env('PERIOD_TIME')


async def main():
    # initialise the client
    client = await Client(api_key, api_secret)
    baseMA = await baseCoin(client)
    currentMA = await currentCoin(client)

    print("تو همیشه اینو باید بدونی، که baseCoin واسه مقدار بیشتره، مثلا یک روز در مقابل شش ساعت\n")

    print("baseSMA : ", end="")
    print(baseMA)
    print("currentSMA : ", end="")
    print(currentMA)
    print("")

    # await compare(currentMA, baseMA)
    # await writeInFile(currentMA, baseMA)
    await client.close_connection()


async def baseCoin(client):
    # init historical klines
    bars = await client.get_historical_klines(f'{currentCurrency}{baseCurrency}', client.KLINE_INTERVAL_1MINUTE,
                                              baseDuration)

    # bars = await client.get_historical_klines("BNBBTC", client.KLINE_INTERVAL_1MINUTE, "30 minutes ago UTC")

    # bars = await client.get_klines(symbol='BNBBTC', interval=client.KLINE_INTERVAL_30MIaNUTE)

    for line in bars:
        del line[5:]

    # load DataFrame
    # btc_df = pandas.read_csv('btc_bars.csv', index_col=0)
    btc_df = pandas.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close'])
    btc_df.set_index('date', inplace=True)
    btc_df.index = pandas.to_datetime(btc_df.index, unit='ms')

    if technical_analysis == "EMA":
        # calculate exponential average using Pandas
        btc_df['ema'] = btc_df['close'].ewm(span=4, adjust=False).mean()
        return btc_df.ema[len(btc_df) - 1]
    elif technical_analysis == "SMA":
        # calculate moving average using Pandas
        btc_df['sma'] = btc_df.close.rolling(len(btc_df)).mean()
        return btc_df.sma[len(btc_df) - 1]


async def currentCoin(client):
    # timeText = "30 minutes ago UTC"
    # init historical klines
    # bars = await client.get_historical_klines("BNBBTC", client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
    # bars = await client.get_historical_klines("BNBBTC", client.KLINE_INTERVAL_1MINUTE, timeText)

    # init historical klines
    bars = await client.get_historical_klines(f'{currentCurrency}{baseCurrency}', client.KLINE_INTERVAL_1MINUTE,
                                              currentDuration)

    # bars = await client.get_klines(symbol='BNBBTC', interval=client.KLINE_INTERVAL_30MINUTE)

    for line in bars:
        del line[5:]

    # load DataFrame
    # btc_df = pandas.read_csv('btc_bars.csv', index_col=0)
    btc_df = pandas.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close'])
    btc_df.set_index('date', inplace=True)
    btc_df.index = pandas.to_datetime(btc_df.index, unit='ms')

    if technical_analysis == "EMA":
        # calculate exponential average using Pandas
        btc_df['ema'] = btc_df['close'].ewm(span=4, adjust=False).mean()
        return btc_df.ema[len(btc_df) - 1]
    elif technical_analysis == "SMA":
        # calculate moving average using Pandas
        btc_df['sma'] = btc_df.close.rolling(len(btc_df)).mean()
        return btc_df.sma[len(btc_df) - 1]


async def compare(newCurrentMA, newBaseMA):
    data = await readFromFile()
    if data is None:
        print("its first request .")
    else:
        oldBaseMA = data.get("base_price")
        oldCurrentMA = data.get("current_price")

        if newCurrentMA > newBaseMA:
            if oldCurrentMA < oldBaseMA:
                await doExchange()
        elif newCurrentMA < newBaseMA:
            if oldCurrentMA > oldBaseMA:
                await doExchange()


async def doExchange():
    print("yeah, its good time for exchange . \n")


async def writeInFile(currentMA, baseMA):
    now = datetime.datetime.now()
    dic = {
        "time": now.strftime("%Y, %m, %d, %H:%M"),
        "technical_analysis": technical_analysis,
        "current_currency": currentCurrency,
        "current_duration": currentDuration,
        "current_price": currentMA,
        "base_currency": baseCurrency,
        "base_duration": baseDuration,
        "base_price": baseMA,
    }
    with open(f"{currentCurrency}_{baseCurrency}_{technical_analysis}.txt", "w") as outfile:
        json.dump(dic, outfile)
        outfile.write('\n')
    with open(f"{currentCurrency}_{baseCurrency}_{technical_analysis}_historical.txt", "a") as outfile:
        json.dump(dic, outfile)
        outfile.write('\n')


async def readFromFile():
    try:
        # data = []
        with open(f"{currentCurrency}_{baseCurrency}_{technical_analysis}.txt") as json_file:
            # for line in json_file:
            #     data.append(json.loads(line))
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        return None


if __name__ == "__main__":
    while True:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        time.sleep(period_time)

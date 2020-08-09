
import os
from datetime import datetime
import pandas as pd
import finnhub
import time

current_path = dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(current_path, 'data')
minDate = datetime(2015, 1, 1)
maxDate = datetime(2020, 6, 1)

token = "bslf58frh5rb8ivktbpg"
finnhub_client = finnhub.Client(api_key=token)


def download_data(overwrite=False):
    symbols = getSymbolList()
    for symbol in symbols:
        if os.path.exists(getFileName(symbol)) and not overwrite:
            continue
        print("Downloading " + symbol)
        features = getCandles(symbol)
        if features is None:
            print("Download of " + symbol + " failed")
            continue
        save(features, symbol)


def getFileName(symbol):
    return os.path.join(data_path, symbol + '.csv')


def save(df, name):
    df.to_csv(getFileName(name))


def getCandles(symbol, fromDate=minDate, toDate=maxDate):
    try:
        response = finnhub_client.stock_candles(symbol, 'D', int(datetime.timestamp(fromDate)),
                                                int(datetime.timestamp(toDate)))
        time.sleep(1)
        return pd.DataFrame(response)
    except finnhub.FinnhubAPIException as err:
        print(err)
        print("Waiting 30s...")
        time.sleep(30)
        return None
    except ValueError:
        return None


def getSymbolList():
    return pd.DataFrame(finnhub_client.stock_symbols(exchange='US'))['symbol']


def main():
    if not os.path.exists(data_path):
        os.mkdir(data_path)
    download_data()


if __name__ == "__main__":
    main()
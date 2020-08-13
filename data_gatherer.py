
import os
from datetime import datetime
import pandas as pd
import finnhub
import time
from config import *


minDate = datetime(2015, 1, 1)
maxDate = datetime(2020, 6, 1)
token = "bslf58frh5rb8ivktbpg"
finnhub_client = finnhub.Client(api_key=token)


def download_data(overwrite=False):
    symbols = get_symbol_list()
    for symbol in symbols:
        if os.path.exists(get_file_name(symbol)) and not overwrite:
            continue
        print("Downloading " + symbol)
        features = get_candles(symbol)
        if features is None:
            print("Download of " + symbol + " failed")
            continue
        save(features, symbol)


def save(df, name):
    df.to_csv(get_file_name(name))


def get_candles(symbol, from_date=minDate, to_date=maxDate):
    try:
        response = finnhub_client.stock_candles(symbol, 'D', int(datetime.timestamp(from_date)),
                                                int(datetime.timestamp(to_date)))
        time.sleep(0.5)
        return pd.DataFrame(response)
    except finnhub.FinnhubAPIException as err:
        print(err)
        print("Waiting 30s...")
        time.sleep(30)
        return None
    except ValueError:
        return None


def get_symbol_list():
    return pd.DataFrame(finnhub_client.stock_symbols(exchange='US'))['symbol']


def main():
    if not os.path.exists(data_path):
        os.mkdir(data_path)
    download_data()


if __name__ == "__main__":
    main()

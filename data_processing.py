from config import *
import pandas as pd
from datetime import datetime
from visualization import plot


def select_features(symbol, from_date=datetime(2018, 1, 1), to_date=datetime(2019, 1, 1)):
    df = read_data(symbol)
    start_date = datetime.timestamp(from_date)
    end_date = datetime.timestamp(to_date)
    selected_range = df.loc[(df.t >= start_date) & (df.t <= end_date)][['c', 't']]
    return selected_range


if __name__ == "__main__":
    df = select_features('A')
    plot(df)

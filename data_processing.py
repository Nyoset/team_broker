from config import *
import random
import tensorflow as tf
import pandas as pd
from datetime import datetime
from visualization import plot


# We need to make sure the output is of the same shape
def select_features(symbol, from_date=datetime(2018, 1, 1), to_date=datetime(2019, 1, 1)):
    df = read_data(symbol)
    start_date = datetime.timestamp(from_date)
    end_date = datetime.timestamp(to_date)
    selected_range = df.loc[(df.t >= start_date) & (df.t <= end_date)][['c']]
    return tf.convert_to_tensor(selected_range)


def main():
    symbols = get_downloaded_symbols()
    candidates = random.sample(symbols, 100)
    result = tf.stack([select_features(candidate) for candidate in candidates])
    print(result)


if __name__ == "__main__":
    #df = select_features('A')
    #plot(df)
    main()

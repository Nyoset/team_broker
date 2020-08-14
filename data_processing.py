from config import *
import random
import tensorflow as tf
from datetime import datetime

samples = 100


def select_features(symbol, from_date=min_date, to_date=max_date):
    df = read_data(symbol)
    start_date = datetime.timestamp(from_date)
    end_date = datetime.timestamp(to_date)
    selected_range = df.loc[(df.t >= start_date) & (df.t <= end_date)][['c']]
    row_count = selected_range.shape[0]
    if row_count < samples:
        return None
    return selected_range.head(samples)


def get_random_sample():
    symbols = get_downloaded_symbols()
    candidates = random.sample(symbols, 100)
    features = list(filter(lambda x: x is not None, [select_features(candidate) for candidate in candidates]))
    result = tf.stack([tf.convert_to_tensor(feature) for feature in features])
    return result


if __name__ == "__main__":
    get_random_sample()

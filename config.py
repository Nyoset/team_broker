import os
import pandas as pd

current_path = dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(current_path, 'data')


def get_file_name(symbol):
    return os.path.join(data_path, symbol + '.csv')


def read_data(symbol):
    file_name = get_file_name(symbol)
    df = pd.read_csv(file_name, header=0)
    return df


def get_downloaded_symbols():
    files_list = os.listdir(data_path)
    return [f.replace(".csv", "") for f in files_list if os.path.isfile(os.path.join(data_path, f))]

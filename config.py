import os

current_path = dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(current_path, 'data')


def getFileName(symbol):
    return os.path.join(data_path, symbol + '.csv')

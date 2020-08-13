import matplotlib.pyplot as plt
from config import *
from datetime import datetime


def plot_close(symbol):
    data = read_data(symbol)
    dates = list(map(lambda x: datetime.fromtimestamp(x), data['t']))
    plt.plot(dates, data['c'])
    plt.title(symbol)
    plt.show()


def plot(data):
    dates = list(map(lambda x: datetime.fromtimestamp(x), data['t']))
    plt.plot(dates, data['c'])
    plt.show()


if __name__ == "__main__":
    plot_close('A')

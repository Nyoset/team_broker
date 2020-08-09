import matplotlib.pyplot as plt
from config import *
import pandas as pd
from datetime import datetime


def readData(symbol):
    file_name = getFileName(symbol)
    df = pd.read_csv(file_name, header=0)
    return df


def plotClose(symbol):
    data = readData(symbol)
    dates = list(map(lambda x: datetime.fromtimestamp(x), data['t']))
    plt.plot(dates, data['c'])
    plt.title(symbol)
    plt.show()


if __name__ == "__main__":
    plotClose('A')

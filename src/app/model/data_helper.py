import pandas as pd


def load_dataset(ticker='BBDC4', path='C:\\Repositories\\StockPredictions\\datasets\\b3_stocks_1994_2020.csv'):
    raw_dataframe = pd.read_csv(path)
    dataset = raw_dataframe[raw_dataframe.ticker == ticker]
    try:
        dataset = dataset.drop(columns=["ticker", "datetime"])
    except:
        print('ticker and/or datetime columns doesn\'t not exists')
    return dataset

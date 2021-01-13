import pandas as pd


def load_dataset(ticker='BBDC4', path='C:\\Repositories\\StockPredictions\\datasets\\b3_stocks_1994_2020.csv'):
    raw_dataframe = pd.read_csv(path)
    dataset = raw_dataframe[raw_dataframe.ticker == ticker]
    try:
        dataset = dataset.drop(columns=["ticker", "datetime"])
    except:
        print('ticker and/or datetime columns doesn\'t not exists')
    return dataset


def split_train_test(ochlv_history_normalized, next_open_normalized, split_ratio=0.9):

    test_n = int(ochlv_history_normalized.shape[0] * split_ratio)

    history_train = ochlv_history_normalized[:test_n]
    y_train = next_open_normalized[:test_n]

    history_test = ochlv_history_normalized[test_n:]
    y_test = next_open_normalized[test_n:]

    return history_train, y_train, history_test, y_test

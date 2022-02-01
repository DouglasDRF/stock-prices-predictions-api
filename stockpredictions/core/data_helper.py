import pandas as pd
import os
import boto3
from .consts import BUCKET_NAME

def load_dataset(ticker='BBDC4', path=os.getcwd() + '/datasets/b3_stocks_1994_2020.csv'):

    if not os.path.exists(os.getcwd() + '/datasets'):
        os.makedirs(os.getcwd() + '/datasets')

    if not os.path.exists(path):
        s3 = boto3.client('s3')
        s3.download_file(BUCKET_NAME, 'datasets/b3_stocks_1994_2020.csv', path)
 
    raw_dataframe = pd.read_csv(path)
    dataset = raw_dataframe[raw_dataframe.ticker == ticker]
    try:
        dataset = dataset.drop(columns=["ticker", "datetime"])
    except Exception:
        print('ticker and/or datetime columns doesn\'t not exists')
    return dataset
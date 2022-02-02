import sys
import boto3
from decimal import Decimal
from stockpredictions.models import TrainingLog

dynamodb = boto3.resource('dynamodb')


class TrainingLogRepository:
    def __init__(self):
        pass

    def save_training_log(self, training_log: TrainingLog):
        table = dynamodb.Table('TrainingLog')
        try:
            table.put_item(Item={
                'model_file_name': str(training_log.model_file_name),
                'accuracy': Decimal(str(training_log.accuracy)),
                'samples_count': int(training_log.samples_count),
                'tickers_on_training': str(training_log.tickers_on_training)
            })
        except Exception as e:
            print(sys.exc_info()[0])
            print(e)
            raise

    def get_last_log(self) -> TrainingLog:
        table = dynamodb.Table('TrainingLog')
        response = table.scan()
        if(response['Count'] > 0):
            response['Items'].sort(key=lambda x: x['model_file_name'])
            last = response['Items'][-1]
            return TrainingLog(int(last['samples_count']), float(last['accuracy']), last['model_file_name'],
             last['tickers_on_training'].split(','))

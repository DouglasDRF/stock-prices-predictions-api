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
                'training_date': str(training_log.date),
                'model_file_name': str(training_log.model_file_name[0]),
                'accuracy': Decimal(str(training_log.accuracy[0])),
                'samples_count': int(training_log.samples_count[0])
            })
        except Exception as e:
            print(sys.exc_info()[0])
            raise
    
    def get_last_log(self):
        table = dynamodb.Table('TrainingLog')
        response = table.scan()
        items = response['Items']
        while 'LastEvaluatedKey' in response:
            print(response['LastEvaluatedKey'])
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response['Items'])
        for x in items:
            yield x
        
import sys
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal
from datetime import date
from stockpredictions.models.predicted import Predicted

dynamodb = boto3.resource('dynamodb')

class StatisticsRepository:
    def __init__(self):
        pass

    def get_last_predicted_price(self, ticker) -> Predicted:

        table = dynamodb.Table('PredictionHistories')
        response = table.query(
            KeyConditionExpression=Key('ticker').eq(ticker)
        )
        typedList = []
        for x in response['Items']:
            typedList.append(Predicted(x['ticker'], x['previous'], x['predicted_value'], x['prediction_type'], x['direction'], x['date']))
        
        if len(typedList) >= 2:
            typedList = typedList[-2:]
            return typedList[0]
        elif len(typedList) == 1 and date.today().isoformat() > typedList[0].date:
            return typedList[0]
        else:
            raise Exception('No prediction was found previously')
            
    def save_prediction(self, prediction:Predicted):
        table = dynamodb.Table('PredictionHistories')
        try:
            table.put_item(Item={
                'ticker': prediction.ticker[0],
                'date': prediction.date,
                'direction': prediction.direction[0],
                'prediction_type': prediction.prediction_type[0],
                'previous': Decimal(str(prediction.previous[0])),
                'predicted_value': Decimal(str(prediction.predicted_value[0])),
            })
        except Exception as e:
            print(sys.exc_info()[0])
            raise
    
    def update_logs_with_real_values(self, ticker, dt, real_val, real_dir):

        table = dynamodb.Table('PredictionHistories')
        try:
            response = table.update_item(
                Key={
                    'ticker': ticker,
                    'date': dt
                },
                UpdateExpression='SET real_direction = :rd, real_value= :rv',
                ExpressionAttributeValues={
                    ':rv': Decimal(str(real_val)),
                    ':rd': str(real_dir)
                },
                ReturnValues="UPDATED_NEW"
            )
            return response
        except Exception as e:
            print(sys.exc_info()[0])
            raise
    


from typing import List
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal
from datetime import date
from stockpredictions.data.helper import get_last_working_day
from stockpredictions.models.predicted import Predicted

dynamodb = boto3.resource('dynamodb')


class StatisticsRepository:

    def get_last_predicted_price(self, ticker) -> Predicted:

        table = dynamodb.Table('PredictionHistories')
        response = table.query(
            KeyConditionExpression=Key('ticker').eq(ticker) & Key(
                'date').eq(get_last_working_day().isoformat())
        )
        typedList = []
        for x in response['Items']:
            typedList.append(Predicted(
                x['ticker'], float(x['previous']), float(x['predicted_value']), x['prediction_type'], x['direction'], date.fromisoformat(x['date'])))

        if len(typedList) == 1:
            return typedList[0]
        else:
            raise Exception('No prediction was found previously')

    def save_prediction(self, prediction: Predicted):
        table = dynamodb.Table('PredictionHistories')
        try:
            table.put_item(Item={
                'ticker': prediction.ticker,
                'date': prediction.date,
                'direction': prediction.direction,
                'prediction_type': prediction.prediction_type,
                'previous': Decimal(str(prediction.previous)),
                'predicted_value': Decimal(str(prediction.predicted_value)),
            })
        except Exception as e:
            print(e)
            raise

    def update_logs_with_real_values(self, ticker, dt, real_val, real_dir):

        table = dynamodb.Table('PredictionHistories')
        try:
            response = table.update_item(
                Key={
                    'date': dt.isoformat(),
                    'ticker': ticker
                },
                UpdateExpression='SET real_direction = :rd, real_value= :rv',
                ExpressionAttributeValues={
                    ':rv': Decimal(str(real_val)),
                    ':rd': str(real_dir)
                },
                ReturnValues="UPDATED_NEW"
            )
            return response['Attributes']
        except Exception as e:
            print(e)
            raise

    def get_all_predictions_updated(self) -> List:
        table = dynamodb.Table('PredictionHistories')
        try:
            response = table.scan()
            items = response['Items']
            while 'LastEvaluatedKey' in response:
                print(response['LastEvaluatedKey'])
                response = table.scan(
                    ExclusiveStartKey=response['LastEvaluatedKey'])
                items.extend(response['Items'])
            result = []
            for x in items:
                try:
                    result.append(Predicted(ticker=x['ticker'], predicted_value=x['predicted_value'], date=x['date'],
                                            real_direction=x['real_direction'], real_value=x['real_value'], previous=['previous'], direction=x['direction'],
                                            prediction_type=x['prediction_type']))
                except KeyError:
                    pass
            return result
        except Exception as e:
            print(e)
            raise

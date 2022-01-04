import secrets, boto3

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from boto3.dynamodb.conditions import Key

security = HTTPBasic()
dynamodb = boto3.resource('dynamodb')

def get_basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    table = dynamodb.Table('ApiCredentials')
    response = table.query(
        KeyConditionExpression=Key('ApiKey').eq(credentials.username) & Key('ApiSecret').eq(credentials.password)
    )
    try:
        correct_username = secrets.compare_digest(credentials.username, response['Items'][0]['ApiKey'])
        correct_password = secrets.compare_digest(credentials.password, response['Items'][0]['ApiSecret'])
        if not (correct_username and correct_password):
            return credentials
    except:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Basic"},
            )
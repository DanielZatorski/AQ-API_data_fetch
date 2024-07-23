import requests
from datetime import datetime
import pandas as pd
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal

#Initialize tables
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('your_table_name') #your dynamoDB table

#Function to request data via API

def get_measurements(api_key, cities_data):
    measurements = []
    url = 'https://api.openaq.org/v2/measurements'
    headers = {"accept": "application/json"}

    for city in cities_data:
        params = {
            'apikey': api_key,
            'limit': 1,
            'city': city,
            'parameter_id': 2,  # based on PM2.5 data
            'order_by': 'datetime',
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            measurements.extend(data['results'])
        else:
            error_info = {
                'city': city,
                'error': f"Error: {response.status_code}, {response.text}"
            }
            measurements.append(error_info)

    if measurements:
        try:
            df = pd.DataFrame(measurements)
            extract_local_time = lambda date_dict: datetime.fromisoformat(date_dict['local'])
            df['timestamp'] = df['date'].apply(lambda x: extract_local_time(x).timestamp())
            df = df.drop(columns=['isMobile', 'isAnalysis', 'entity', 'sensorType', 'coordinates', 'city', 'country', 'date', 'unit', 'parameter', 'location'])
            df = df.sort_values(by='timestamp', ascending=True)
            return df.to_dict(orient='records')
        except Exception as e:
            print(f"Error processing DataFrame: {e}")
            return []
    else:
        print("No data collected")
        return []


#Writing data to DynamoDB table

def lambda_handler(event, context):
    api_key = 'your_api_key'  # Replace with your actual API key
    cities_data = ['Kraków', 'Gdańsk', 'Warszawa']  # Replace with your list of cities

    measurements = get_measurements(api_key, cities_data)

    if measurements:
        try:
            for measurement in measurements:

                item = {
                    'locationId': measurement['locationId'],
                    'timestamp': int(measurement['timestamp']),  # Ensure timestamp is an integer
                    'value': Decimal(str(measurement['value']))  # Convert float to Decimal
                }
                try:
                    table.put_item(Item=item)
                except ClientError as e:
                    print(f"Error putting item {item} into DynamoDB: {e}")
        except Exception as e:
            print(f"Error writing to DynamoDB: {e}")
    else:
        print("No measurements to write")



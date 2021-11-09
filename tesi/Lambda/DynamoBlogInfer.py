import greengrasssdk
import boto3
import logging
import os
import time
import json

dynamodb = boto3.resource("dynamodb", region_name="eu-west-1")
tableName = "DBTesiAlessandro"
client = greengrasssdk.client('iot-data')

OUTPUT_TOPIC = 'dynamo/output'


def lambda_handler(event, context):
	
	logging.info(event["prediction"])
	global tableName
	
	table = dynamodb.Table(tableName)
	table.put_item(
		Item={
			"Gesture ID": str(time.time()),
			"prediction":event["prediction"],
			"filepath": event["filepath"]
			}
	)
		
	client.publish(topic=OUTPUT_TOPIC, payload=json.dumps("funzione partita"))
	

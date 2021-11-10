#
# Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
 
# Lambda entry point
from model_loader import MLModel
import logging
import os
import time
import json
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import os
import numpy as np
import urllib
import cv2
 
dynamodb = boto3.resource("dynamodb", region_name="eu-west-1")
tableName = "DBTesiAlessandro"
predicted_gesture = "none"
seven_days_as_seconds = 604800

s3_signature ={
'v4':'s3v4',
'v2':'s3'
}
 
ML_MODEL_BASE_PATH = 'model/'
ML_MODEL_PREFIX = 'deploy_model_algo_1'
ML_MODEL_PATH = os.path.join(ML_MODEL_BASE_PATH, ML_MODEL_PREFIX)
# Creating a greengrass core sdk client
 
#client=boto3.client('iot-data', endpoint_url='a3gtyikpk9vqi1-ats.iot.eu-west-1.amazonaws.com')
 
model = None
 
# Load the model at startup
def initialize(param_path=ML_MODEL_PATH):
 global model
 model = MLModel(param_path)
 
 
def lambda_handler(event, context):
 bucket_name = event['Records'][0]['s3']['bucket']['name']
 key = event['Records'][0]['s3']['object']['key']

 generated_signed_url = create_presigned_url(bucket_name, key,
 seven_days_as_seconds, s3_signature['v4'])
 print(generated_signed_url)
 image_complete = url_to_image(generated_signed_url)
 
 start = int(round(time.time() * 1000))
 prediction = model.predict_from_file(image_complete)
 end = int(round(time.time() * 1000))
 
 response = {
  'prediction': prediction,
  'timestamp': time.time()
 }
 
 if prediction[0][0] == 0:
  predicted_gesture = "hello"
 elif prediction[0][0] == 1:
  predicted_gesture = "thanks"
 else:
  predicted_gesture = "i love you"
  
 global tableName
 table = dynamodb.Table(tableName)
 table.put_item(
  Item={
   "Gesture ID": str(time.time()),
   "prediction": predicted_gesture,
   "filepath": key
  }
 )
  
 return response
 
 
def url_to_image(URL):
    resp = urllib.request.urlopen(URL)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    
    return image
    
def create_presigned_url(bucket_name, bucket_key, expiration=3600, signature_version=s3_signature['v4']):

    s3_client = boto3.client('s3',
                         aws_access_key_id=#YOUR ACCESS KEY ID",
                         aws_secret_access_key=#YOUR SECRET ACCESS KEY,
                         config=Config(signature_version=signature_version),
                         region_name='eu-west-1'
                         )
    try:
        response = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': bucket_key}, ExpiresIn=expiration)
        print(s3_client.list_buckets()['Owner'])
        for key in s3_client.list_objects(Bucket=bucket_name,Prefix=bucket_key)['Contents']:
            print(key['Key'])
    except ClientError as e:
        logging.error(e)
        return None
 # The response contains the presigned URL
 
    return response
 
# If this path exists then this code is running on the greengrass core and has the ML resources it needs to initialize.
if os.path.exists(ML_MODEL_BASE_PATH):
    initialize()
else:
 logging.info('{} does not exist and we cannot initialize this lambda function.'.format(ML_MODEL_BASE_PATH))

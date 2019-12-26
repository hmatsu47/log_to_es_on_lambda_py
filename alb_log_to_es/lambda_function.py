import boto3
import os
import gzip
import requests
from datetime import datetime
from requests_aws4auth import AWS4Auth

def lambda_handler(event, context):
    print('Started')
    es_index = os.environ['ES_INDEX_PREFIX'] + "-" + datetime.strftime(datetime.now(), "%Y%m%d")
    region = os.environ["AWS_REGION"]
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    s3 = boto3.resource('s3')
    s3.Bucket(bucket).download_file(key, '/tmp/log.gz')

    with gzip.open('/tmp/log.gz', mode='rt') as f:
        data = ""

        for line in f:
            data += '{"index":{"_index":"%s","_type":"log"}}\n' % es_index
            data += '{"message":"%s"}\n' % line.strip().replace('"', '\\"')
    
            if len(data) > 3000000:
                _bulk(data, awsauth)
                data = ""

        if data != "":
            _bulk(data, awsauth)

    return 'Completed'

def _bulk(data, awsauth):    
    es_host = os.environ['ES_HOST']
    pipeline = os.environ['PIPELINE_NAME']
    url = 'https://%s/_bulk?pipeline=%s' % (es_host, pipeline)

    headers = {'Content-Type': 'application/json'}
    response = request(url, awsauth, headers=headers, data=data)
    
    if response.status_code != requests.codes.ok:
        print(response.text)

def request(url, awsauth, headers=None, data=None):
    return requests.post(url, auth=awsauth, headers=headers, data=data)

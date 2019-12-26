import boto3
import datetime
import os
import pymysql
import re
import sys
import requests
from requests_aws4auth import AWS4Auth

aurora_host = os.environ["AURORA_HOST"]
aurora_user = os.environ["AURORA_USER"]
aurora_pass = os.environ["AURORA_PASS"]

try:
    conn = pymysql.connect(aurora_host, user=aurora_user, passwd=aurora_pass, db="mysql", connect_timeout=10)
except:
    print("ERROR: Could not connect to Aurora instance : [%s]." % aurora_host)
    sys.exit()

def lambda_handler(event, context):

    print("Started")
    lasthour = datetime.datetime.today() - datetime.timedelta(hours = (1 - 9))
    exportdate1 = lasthour.strftime('%Y%m%d')
    exportdate2 = lasthour.strftime('%Y-%m-%d')
    exporttime = lasthour.strftime('%H')
    es_host = os.environ["ES_HOST"]
    es_index = os.environ["ES_INDEX_PREFIX"] + "-" + exportdate1
    s3_bucket = os.environ["S3_BUCKET"]
    s3_key = os.environ["S3_PREFIX"] + "/" + exportdate2 + "_" + exporttime
    region = os.environ["AWS_REGION"]
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    print("Export: " + exportdate1 + "_" + exporttime)

    with conn.cursor() as cur:
        cur.execute("SELECT CONCAT(DATE(CONVERT_TZ(start_time, '+09:00', 'UTC')), 'T', TIME(CONVERT_TZ(start_time, '+09:00', 'UTC')), 'Z ', REPLACE(user_host, ' ', ''), ' ', TIME_TO_SEC(query_time), ' ', TIME_TO_SEC(lock_time), ' ', rows_sent, ' ', rows_examined, ' ', (CASE WHEN db='' THEN '-' ELSE db END), ' ', sql_text) FROM mysql.slow_log WHERE start_time BETWEEN '%s %s:00:00' AND '%s %s:59:59.999'" % (exportdate2, exporttime, exportdate2, exporttime))
        file_data = ""
        file_count = 1
        es_data = ""

        for line in cur:
            line_data = re.sub(r"(\\t| )+", " ", re.sub(r"\?+", "?", "".join(str(line)).strip()[2:-3].replace('"', '\\"')))
            file_data += "%s\n" % line_data
            es_data += '{"index":{"_index":"%s","_type":"log"}}\n' % es_index
            es_data += '{"message":"%s"}\n' % line_data
            if len(file_data) > 3000000:
                s3_client = boto3.client("s3")
                s3_client.put_object(
                  Bucket=s3_bucket,
                  Key=s3_key + "-" + str(file_count),
                  Body=file_data
                )
                #print("--- file: %s" % file_count)
                #print(file_data)
                file_data = ""
                file_count += 1
            if len(es_data) > 3000000:
                _bulk(es_host, es_data, awsauth)
                #print("--- es")
                #print(es_data)
                es_data = ""

        if file_data != "":
            s3_client = boto3.client("s3")
            s3_client.put_object(
              Bucket=s3_bucket,
              Key=s3_key + "-" + str(file_count),
              Body=file_data
            )
            #print("--- file: %s" % file_count)
            #print(file_data)

        if es_data != "":
            _bulk(es_host, es_data, awsauth)
            #print("--- es")
            #print(es_data)

    return "Completed"

def _bulk(host, doc, awsauth):
    pipeline = os.environ["PIPELINE_NAME"]
    
    url = "https://%s/_bulk?pipeline=%s" % (host, pipeline)
    headers = {"Content-Type": "application/json"}
    response = request(url, awsauth, headers=headers, data=doc)

    if response.status_code != requests.codes.ok:
        print(response.text)

def request(url, awsauth, headers=None, data=None):
    return requests.post(url, auth=awsauth, headers=headers, data=data)

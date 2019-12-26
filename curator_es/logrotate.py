import boto3
import curator
import os
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

es_host = os.environ["ES_HOST"]
es_index = os.environ["ES_INDEX_PREFIX"] + "-"
rotation_period = int(os.environ["ROTATION_PERIOD"])
region = os.environ["AWS_REGION"]

def lambda_handler(event, context):
    awsauth = AWS4Auth(
        os.environ["AWS_ACCESS_KEY_ID"],
        os.environ["AWS_SECRET_ACCESS_KEY"],
        region,
        "es",
        session_token=os.environ["AWS_SESSION_TOKEN"]
    )

    es = Elasticsearch(
        hosts=[{"host": es_host, "port": 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    runCurator(es)


def runCurator(es):
    ilo = curator.IndexList(es)
    ilo.filter_by_regex(kind="prefix", value=es_index)
    ilo.filter_by_age(source="name", direction="older", timestring="%Y%m%d", unit="days", unit_count=rotation_period)
    delete_indices = curator.DeleteIndices(ilo)
    delete_indices.do_action()

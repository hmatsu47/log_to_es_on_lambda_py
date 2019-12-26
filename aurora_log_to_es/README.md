# For AWS Lambda (Python 3.8) : Aurora MySQL Slow Logs to Elasticsearch Service 6.8

- Create zip file

```sh:create_zip_file
$ . dev/bin/activate
(dev) $ mkdir aurora_log_to_es_s3
(dev) $ cd aurora_log_to_es_s3/
(dev) $ pip install requests pymysql requests_aws4auth -t ./

...

Installing collected packages: urllib3, certifi, idna, chardet, requests, requests-aws4auth
Successfully installed certifi-2019.11.28 chardet-3.0.4 idna-2.8 requests-2.22.0 requests-aws4auth-0.9 urllib3-1.25.7

...

(dev) $ rm -rf *.dist-info
(dev) $ vi auroralog.py

...

(dev) $ zip -r ../auroralog.zip

...
```
## For AWS Lambda (Python 3.8) : Aurora MySQL Slow Logs to Elasticsearch Service 6.8

- Create zip file

```sh:create_zip_file
$ . dev/bin/activate
(dev) $ mkdir aurora_log_to_es_s3
(dev) $ cd aurora_log_to_es_s3/
(dev) $ pip install requests pymysql requests_aws4auth -t ./

...

(dev) $ rm -rf *.dist-info
(dev) $ vi auroralog.py

...

(dev) $ zip -r ../auroralog.zip

...
```

## For AWS Lambda (Python 3.8) : CloudFront Logs to Elasticsearch Service 6.8

- Create zip file

```sh:create_zip_file
$ python3 -m venv dev
$ . dev/bin/activate
(dev) $ mkdir cf_log_to_es_s3
(dev) $ cd cf_log_to_es_s3/
(dev) $ pip install requests requests_aws4auth -t ./

...

(dev) $ rm -rf *.dist-info
(dev) $ vi lambda_function.py

...

(dev) $ zip -r ../cflog.zip

...
```

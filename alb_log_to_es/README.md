## For AWS Lambda (Python 3.8) : ALB/CLB Logs to Elasticsearch Service 6.8

- Create zip file

```sh:create_zip_file
$ . dev/bin/activate
(dev) $ mkdir alb_log_to_es_s3
(dev) $ cd alb_log_to_es_s3/
(dev) $ pip install requests requests_aws4auth -t ./

...

(dev) $ rm -rf *.dist-info
(dev) $ vi lambda_function.py

...

(dev) $ zip -r ../alblog.zip

...
```

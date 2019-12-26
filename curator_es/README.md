## For AWS Lambda (Python 3.8) : Rotate Logs on Elasticsearch Service 6.8

- Create zip file

```sh:create_zip_file
$ . dev/bin/activate
(dev) $ mkdir logrotate
(dev) $ cd logrotate/
(dev) $ pip install curator elasticsearch requests_aws4auth -t ./

...

(dev) $ rm -rf *.dist-info
(dev) $ vi logrotate.py

...

(dev) $ zip -r ../logrotate.zip

...
```

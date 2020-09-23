## For AWS Lambda (Python 3.8) : Rotate Logs on Elasticsearch Service 6.8

- Create zip file

```sh:create_zip_file
$ python3 -m venv dev
$ . dev/bin/activate
(dev) $ mkdir logrotate
(dev) $ cd logrotate/
(dev) $ pip install elasticsearch-curator requests_aws4auth -t ./

...

(dev) $ rm -rf *.dist-info
(dev) $ vi logrotate.py

...

(dev) $ zip -r ../logrotate.zip *

...
```

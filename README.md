

# Installing

Install the package using pip: 
```shell
pip install aws_lambda_mess
```
After a successful installation check that the cli works:
```shell
alm --help
```

# Create and run a new project
Create a new project using th cli:
```shell
alm new demo
```
This will: 
 * create a new directory with the name you specified 
 * populate the directory with some standard boilerplate

A sample app has been created for you in ```src\app.py``` 

```python
from aws_lambda_mess.framework.Route import Route
from aws_lambda_mess.framework.success import success
from aws_lambda_mess.framework.failures import bad_request
from aws_lambda_mess.framework.server import run


def index(params, body):
    return success({"Hallo": "Index"})


def greet(params, body):
    return success({"Hallo": params["name"]})


def default(params, body):
    return bad_request()


routes = [
    Route(method_pattern="GET", path_pattern="/", handler=index),
    Route(method_pattern="GET", path_pattern="/greet/<name>", handler=greet),
    Route(method_pattern=".*", path_pattern=".*", handler=default)
]

from aws_lambda_mess.framework.lambda_dispatcher import get_handler
lambda_handler = get_handler(routes)

if __name__ == "__main__":
    run(9000, routes)
```

To run the app locally simply run:
```shell
python app.py
```

A webserver serving the above routes  will spin up on port 9000

```shell
$ curl -X GET localhost:9000/
{"Hallo": "Index"}

$ curl -X GET localhost:9000/greet/somebody
{"Hallo": "somebody"}

$ curl -X GET localhost:9000/whatwhere -v
Note: Unnecessary use of -X or --request, GET is already inferred.
*   Trying 127.0.0.1:9000...
* Connected to localhost (127.0.0.1) port 9000 (#0)
> GET /whatwhere HTTP/1.1
> Host: localhost:9000
> User-Agent: curl/7.88.1
> Accept: */*
>
* HTTP 1.0, assume close after body
< HTTP/1.0 400 Bad Request
< Server: BaseHTTP/0.6 Python/3.9.13
< Date: Sun, 30 Apr 2023 06:38:25 GMT
<
* Closing connection 0
```

# Build the aws lambda zip

To build the package to be uploaded to aws simply run:
```shell
alm build
```
This will create a zip file in the ```dist``` directory called ```package.zip```

Upload this package to aws lambda either in the lambda console or via s3.

# Install the package
Once the package has been uploaded change the ```handler``` setting under runtime settings to ```app.lambda_handler```

Now test the package with some of these json test cases:

## Test /
```json
{
  "body": "{}",
  "resource": "/{proxy+}",
  "path": "/",
  "httpMethod": "GET",
  "isBase64Encoded": true,
}
```
Returns 
```json
{
  "isBase64Encoded": false,
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"Hallo\": \"Index\"}"
}
```
## Test /greet/somebody
```json
{
  "body": "{}",
  "resource": "/{proxy+}",
  "path": "/greet/somebody",
  "httpMethod": "GET",
  "isBase64Encoded": true
}
```
Returns
```json
{
  "isBase64Encoded": false,
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"Hallo\": \"somebody\"}"
}
```
## Test invalid route or method
```json
{
  "body": "{}",
  "resource": "/{proxy+}",
  "path": "/greet/somebody",
  "httpMethod": "POST",
  "isBase64Encoded": true
}
```
```json
{
  "isBase64Encoded": false,
  "statusCode": 400
}
```
This json gets converted to a proper http response by the proxy.









----------------
Build aws_lambda_mess
```shell
hatch build
```
Upload to pip
```shell
py -m twine upload dist/* --user johanjordaan
```





# Commented copy of 09-serverless/code/test.py (lessons 9.5 and 9.7).
# The original is untouched in ../../../notebooks/code/test.py.

# PYTHON: requests is the standard HTTP client library (pip install requests).
import requests

# GOAL: the address of the Lambda Runtime Interface Emulator inside the running container.
# WHY:  the Lambda base image exposes this fixed path on port 8080. It is NOT a REST API you design yourself:
#       it imitates the AWS "Invoke" API, so the request body becomes the handler's 'event'.
# NOTE: the port before the colon is the HOST port of 'docker run -p HOST:8080'. The lecture maps 8080:8080;
#       HW9 maps 9000:8080, so there the URL is http://localhost:9000/...
# NOTE: after lesson 9.7 you replace this with the API Gateway URL (https://<id>.execute-api.<region>.amazonaws.com/<stage>/predict).
url = 'http://localhost:8080/2015-03-31/functions/function/invocations'

# GOAL: the event payload. The key must be the one the handler reads: 'url' here, 'image_url' in HW9.
data = {'url': 'http://bit.ly/mlbookcamp-pants'}

# PYTHON: json=data serialises the dict to JSON and sets the Content-Type header; .json() parses the reply.
result = requests.post(url, json=data).json()
print(result)

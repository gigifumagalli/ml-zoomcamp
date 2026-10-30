#!/usr/bin/env python
# coding: utf-8
# Commented copy of 05-deployment/code/predict-test.py (lesson 5.4: the client side).
# The original is untouched in ../../notebooks/code/predict-test.py. Code unchanged, comments added.
#
# Start the service first (commented/predict.py), then:   python commented/predict-test.py

# GOAL: play the role of "the marketing system" that calls our churn service over HTTP.
# WHY:  the client knows nothing about pickle, sklearn or the model: it only knows a URL and a JSON
#       contract. That separation is the whole point of a web service.
import requests


url = 'http://localhost:9696/predict'

customer_id = 'xyz-123'
# WHY: the keys must be EXACTLY the training column names (lower-case, underscores) and the values
#      cleaned the same way as in training ('month-to-month', 'electronic_check'). DictVectorizer
#      silently ignores unknown keys and unseen values -> a typo gives a wrong prediction, not an error.
#      (The workshop's FastAPI + Pydantic version rejects such input with HTTP 422 instead.)
customer = {
    "gender": "female",
    "seniorcitizen": 0,
    "partner": "yes",
    "dependents": "no",
    "phoneservice": "no",
    "multiplelines": "no_phone_service",
    "internetservice": "dsl",
    "onlinesecurity": "no",
    "onlinebackup": "yes",
    "deviceprotection": "no",
    "techsupport": "no",
    "streamingtv": "no",
    "streamingmovies": "no",
    "contract": "month-to-month",
    "paperlessbilling": "yes",
    "paymentmethod": "electronic_check",
    "tenure": 24,
    "monthlycharges": 29.85,
    "totalcharges": (24 * 29.85)
}


# PYTHON: requests.post(url, json=d) serialises d to JSON, sets Content-Type: application/json,
#         sends it, and .json() parses the response body back into a dict.
response = requests.post(url, json=customer).json()
print(response)

# GOAL: turn the prediction into a business action.
if response['churn'] == True:
    print('sending promo email to %s' % customer_id)
else:
    print('not sending promo email to %s' % customer_id)

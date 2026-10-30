# Commented copy of notebooks/code/churn/churn-test.py (lessons 11.3-11.4).
# Needs the port-forward running in another terminal:
#   kubectl port-forward -n istio-system service/istio-ingressgateway 8080:80
# (that is the Knative + Istio install of the lecture; with another install mode or gateway, port-forward
#  whatever service your KServe docs name as the ingress.)

# PYTHON: requests is the HTTP client used since Module 5.
import requests

# GOAL: build the URL of the InferenceService.
# WHY: all services share ONE ingress (the Istio gateway). The gateway routes by the Host header,
#      <name>.<namespace>.<domain>; example.com is the default domain of a local install.
service_name = 'churn'
host = f'{service_name}.default.example.com'

actual_domain = 'http://localhost:8080'
# WHY: /v1/models/<name>:predict is KServe's V1 inference protocol (V2 is /v2/models/<name>/infer).
url = f'{actual_domain}/v1/models/{service_name}:predict'

headers = {'Host': host}

# GOAL: the request body: a list of "instances", one per customer.
# WHY: lecture format (KServe 0.8): each instance is a plain dict, which the DictVectorizer pipeline reads.
#      On current KServe this exact body fails with "If using all scalar values, you must pass an index":
#      use churn-train-2026.py and {'contract': ['one_year'], 'tenure': [34], 'monthlycharges': [56.95]}.
request = {
    "instances": [
        {'contract': 'one_year', 'tenure': 34, 'monthlycharges': 56.95},
        {'contract': 'month-to-month', 'tenure': 13, 'monthlycharges': 49.95}
    ]
}

# PYTHON: json=... serialises the dict to JSON and sets Content-Type: application/json.
response = requests.post(url, json=request, headers=headers)
# WHY: {"predictions": [0, 0]} from the stock image (labels), [[p0, p1], ...] from the predict_proba one.
print(response.json())

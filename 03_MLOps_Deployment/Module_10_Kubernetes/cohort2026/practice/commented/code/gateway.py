#!/usr/bin/env python
# coding: utf-8

# Commented copy of ../../../notebooks/code/gateway.py (lessons 10.3, 10.4, 10.7).
# The gateway: JSON {"url": ...} in -> preprocess -> gRPC to TF Serving -> JSON {class: score} out.
# Not runnable here: it needs TF Serving at TF_SERVING_HOST and the 2021 Pipfile environment.

import os
import grpc

# NOTE: the lesson removes TensorFlow from the gateway (10.3). This import is a leftover in the final file:
#       with only tensorflow-protobuf installed (the Pipfile), 'import tensorflow as tf' still succeeds
#       because that package provides the tensorflow namespace, but nothing below uses 'tf'.
import tensorflow as tf

from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc

from keras_image_helper import create_preprocessor

from flask import Flask
from flask import request
from flask import jsonify

# GOAL: the lightweight replacement for tf.make_tensor_proto (see proto.py).
from proto import np_to_protobuf

# GOAL: where is TF Serving? Read it from an environment variable, default to localhost for local runs.
# WHY: the same code runs in three places with three different addresses:
#      laptop -> 'localhost:8500'; docker-compose -> 'clothing-model:8500' (service name);
#      Kubernetes -> 'tf-serving-clothing-model.default.svc.cluster.local:8500' (service DNS name).
#      Configuration goes in the environment, not in the code (12-factor app rule).
# PYTHON: os.getenv(name, default) returns the variable's value, or the default if it is not set.
host = os.getenv('TF_SERVING_HOST', 'localhost:8500')

# WHY: created ONCE at import time, not per request: opening a gRPC channel is expensive, reusing it is cheap.
channel = grpc.insecure_channel(host)
stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

preprocessor = create_preprocessor('xception', target_size=(299, 299))


# GOAL: wrap the input matrix in a PredictRequest addressed to the right model / signature / input name.
def prepare_request(X):
    pb_request = predict_pb2.PredictRequest()

    pb_request.model_spec.name = 'clothing-model'
    pb_request.model_spec.signature_name = 'serving_default'

    pb_request.inputs['input_8'].CopyFrom(np_to_protobuf(X))
    return pb_request


classes = [
    'dress',
    'hat',
    'longsleeve',
    'outwear',
    'pants',
    'shirt',
    'shoes',
    'shorts',
    'skirt',
    't-shirt'
]


# GOAL: protobuf response -> plain dict. The website never has to know about protobuf.
# WHY: the values are logits (unbounded scores), not probabilities.
def prepare_response(pb_response):
    preds = pb_response.outputs['dense_7'].float_val
    return dict(zip(classes, preds))


# GOAL: the whole pipeline for one URL: preprocess -> request -> call -> postprocess.
# WHY: keeping this a plain function (no Flask inside) means you can test it without a web server.
def predict(url):
    X = preprocessor.from_url(url)
    pb_request = prepare_request(X)
    pb_response = stub.Predict(pb_request, timeout=20.0)
    response = prepare_response(pb_response)
    return response


app = Flask('gateway')


# GOAL: the HTTP endpoint. POST /predict with JSON {"url": "..."}.
# PYTHON: the decorator registers the function as the handler for that route and method;
#         request.get_json() parses the body; jsonify() builds a JSON HTTP response.
@app.route('/predict', methods=['POST'])
def predict_endpoint():
    data = request.get_json()
    url = data['url']
    result = predict(url)
    return jsonify(result)


# WHY: this block runs only with `python gateway.py` (development server). In Docker the entry point is
#      gunicorn (image-gateway.dockerfile), which imports `gateway:app` and never executes this block.
#      Uncomment the three lines to send one test request without starting a server (lesson 10.4 / 10.7).
if __name__ == '__main__':
    # url = 'http://bit.ly/mlbookcamp-pants'
    # response = predict(url)
    # print(response)
    app.run(debug=True, host='0.0.0.0', port=9696)

# Commented script version of ../../../notebooks/10-kubernetes-lecture.ipynb (= code/tf-serving-connect.ipynb).
# Lesson 10.2: talk to a TensorFlow Serving container from Python over gRPC.
#
# NOT RUNNABLE on your Mac as-is: it needs TF Serving listening on localhost:8500 with the clothing
# SavedModel loaded (lesson 10.2, docker run tensorflow/serving:2.7.0), plus the 2021 client libraries
# (grpcio==1.42.0, tensorflow-serving-api==2.7.0, full TensorFlow). HW10 uses none of this.
#
# Dropped from the notebook: %autosave 0 and the two !pip install cells. The last cell's bare expression
# dict(zip(...)) becomes print(...), since a script shows nothing otherwise.

# GOAL: the gRPC client library and the request/response classes generated from TF Serving's .proto files.
# WHY: TF Serving speaks gRPC (binary, typed, fast), not JSON. The client must build a typed protobuf message.
# PYTHON: predict_pb2 holds message classes (PredictRequest); *_pb2_grpc holds the client "stub" class.
import grpc

import tensorflow as tf

from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc


# GOAL: open a connection to TF Serving and create the object we call methods on.
# WHY: insecure = no TLS/auth. Acceptable here because, in the final setup, TF Serving sits inside the
#      Kubernetes cluster behind an internal (ClusterIP) service and is never exposed to the internet.
# PYTHON: a "stub" is a local object whose methods (stub.Predict) are executed on the remote server.
host = 'localhost:8500'

channel = grpc.insecure_channel(host)

stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)


# GOAL: turn an image URL into the model's input matrix X.
# WHY: the Xception model was trained on 299x299 images scaled the Xception way. Serving must apply the
#      SAME preprocessing as training, or predictions silently degrade (training/serving skew).
# PYTHON: create_preprocessor returns an object; .from_url downloads, resizes and scales in one call.
from keras_image_helper import create_preprocessor

preprocessor = create_preprocessor('xception', target_size=(299, 299))

url = 'http://bit.ly/mlbookcamp-pants'
X = preprocessor.from_url(url)     # shape (1, 299, 299, 3), float32: a batch of one image


# GOAL: convert the NumPy array into a protobuf TensorProto.
# WHY: gRPC cannot send a NumPy array; it sends protobuf messages. This one line is the ONLY reason the
#      notebook imports the whole of TensorFlow (~1.7 GB) - lesson 10.3 replaces it with proto.py.
def np_to_protobuf(data):
    return tf.make_tensor_proto(data, shape=data.shape)


# GOAL: build the request: which model, which signature, which named input.
# WHY: the names come from `saved_model_cli show --dir clothing-model --all` (lesson 10.2):
#      model folder 'clothing-model', signature 'serving_default', input 'input_8', output 'dense_7'.
#      A wrong name gives an error from the server, not from Python, so read the signature first.
# PYTHON: protobuf message fields are set by attribute; .CopyFrom copies a whole sub-message into a map entry.
pb_request = predict_pb2.PredictRequest()

pb_request.model_spec.name = 'clothing-model'
pb_request.model_spec.signature_name = 'serving_default'

pb_request.inputs['input_8'].CopyFrom(np_to_protobuf(X))


# GOAL: call the model. timeout=20.0 seconds: never wait forever on a network call.
pb_response = stub.Predict(pb_request, timeout=20.0)


# GOAL: read the 10 scores back out of the response message.
# WHY: these are LOGITS (unbounded scores), not probabilities - the model has no softmax layer.
#      The largest one wins; apply softmax if you need numbers that sum to 1.
# PYTHON: .float_val is a repeated protobuf field - it behaves like a Python list of floats.
preds = pb_response.outputs['dense_7'].float_val

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

# GOAL: human-readable output: {class name: score}.
# PYTHON: zip pairs the i-th class with the i-th score; dict() turns those pairs into a dictionary.
print(dict(zip(classes, preds)))

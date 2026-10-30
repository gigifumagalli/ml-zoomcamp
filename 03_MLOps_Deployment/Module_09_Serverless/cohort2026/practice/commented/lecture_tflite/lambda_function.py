#!/usr/bin/env python
# coding: utf-8
# Commented copy of 09-serverless/code/lambda_function.py (lessons 9.4 - 9.6, the TF-Lite LECTURE stack).
# The original is untouched in ../../../notebooks/code/lambda_function.py.
# OUTDATED STACK: tflite_runtime has no wheels for Python 3.12+, so this only runs on the
# python:3.10 Lambda image with a custom wheel (see the Dockerfile next to this file).
# HW9 does NOT use this: it uses ONNX Runtime + plain Pillow (see ../workshop_onnx/ and ../../../homework/).

# GOAL: the interpreter that runs a .tflite model, WITHOUT the 1.7 GB TensorFlow package.
# WHY:  Lambda bills for cold-start time and image size; TF-Lite only does inference, which is all we need here.
# PYTHON: 'import a.b as c' loads the submodule a.b under the short name c.
import tflite_runtime.interpreter as tflite

# GOAL: image download + resize + Xception scaling, also without TensorFlow.
# WHY:  keras.applications.xception.preprocess_input lives inside TensorFlow; keras-image-helper re-implements it
#       in NumPy + Pillow (a few KB instead of a GB).
# NOTE: keras-image-helper resizes with Image.NEAREST. HW9 pins BILINEAR - do not reuse this helper there.
from keras_image_helper import create_preprocessor


# GOAL: one preprocessor configured for the model: Xception scaling (x / 127.5 - 1), 299 x 299 pixels.
# WHY:  the input must be prepared EXACTLY as during training, or the model sees different numbers than it learned on.
preprocessor = create_preprocessor('xception', target_size=(299, 299))


# GOAL: load the model ONCE, at import time (module level), not inside the handler.
# WHY:  Lambda keeps the process alive between requests ("warm" container). Code at module level runs only on a
#       cold start; code inside lambda_handler runs on every request. Loading a model per request would be slow.
interpreter = tflite.Interpreter(model_path='clothing-model.tflite')
# WHY:  TF-Lite pre-allocates the memory for all intermediate tensors before the first inference.
interpreter.allocate_tensors()

# GOAL: find WHERE to write the input and WHERE to read the output.
# PYTHON: get_input_details() returns a list of dicts (one per input tensor); [0]['index'] = the first one's slot id.
input_index = interpreter.get_input_details()[0]['index']
output_index = interpreter.get_output_details()[0]['index']


# GOAL: map the 10 output positions to class names (same order as the Keras training generator in Module 8).
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

# url = 'http://bit.ly/mlbookcamp-pants'

def predict(url):
    # GOAL: URL -> batch of one preprocessed image, shape (1, 299, 299, 3), float32.
    X = preprocessor.from_url(url)

    # GOAL: run the model: write the input, invoke, read the output.
    # PYTHON: TF-Lite is stateful: set_tensor / invoke / get_tensor, instead of Keras' single model.predict(X).
    interpreter.set_tensor(input_index, X)
    interpreter.invoke()
    preds = interpreter.get_tensor(output_index)

    # WHY:  preds[0] holds np.float32 values, and json cannot serialise np.float32 ("Object of type float32 is not
    #       JSON serializable", lesson 9.5). .tolist() converts them to plain Python floats.
    float_predictions = preds[0].tolist()

    # PYTHON: zip pairs the two lists element by element; dict() turns the pairs into {class: score}.
    return dict(zip(classes, float_predictions))


def lambda_handler(event, context):
    # GOAL: the entry point AWS calls. 'event' = the JSON payload, already parsed into a dict.
    # WHY:  'context' (request id, remaining time, ...) is unused here, but Lambda always passes it.
    # NOTE: with the lecture's non-proxy API Gateway integration, event IS the request body. With a proxy
    #       integration the body arrives as a JSON STRING in event['body'] - the HW9 handler handles both.
    url = event['url']
    result = predict(url)
    # WHY:  the return value must be JSON-serialisable: Lambda converts it to JSON for the caller.
    return result

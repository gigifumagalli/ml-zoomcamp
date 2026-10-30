# Commented copy of 09-serverless/workshop/lambda-onnx/lambda_function.py (the ONNX workshop: the CURRENT stack).
# The original is untouched in ../../../notebooks/workshop/lambda-onnx/lambda_function.py.
# The code is unchanged; only comments are added. 09-serverless_commented.ipynb imports this file and calls
# lambda_handler() locally, without Docker or AWS.
# Model: clothing_classifier_mobilenet_v2_latest.onnx (MobileNetV2 trained in PyTorch, exported to ONNX).

import os

import numpy as np
# GOAL: ONNX Runtime replaces TF-Lite as the inference-only engine.
# WHY:  one runtime for models from Keras, PyTorch, scikit-learn...; ordinary wheels for current Python on Linux,
#       macOS (arm64 too) and Amazon Linux, so no custom-compiled wheel as in the TF-Lite lecture.
import onnxruntime as ort
# NOTE: keras-image-helper resizes with Image.NEAREST. HW9 pins Image.Resampling.BILINEAR in its own
#       prepare_image(): reuse the IDEA (HWC -> CHW, ImageNet mean/std) but not this helper.
from keras_image_helper import create_preprocessor


# GOAL: the model file name comes from an environment variable, with a fallback.
# WHY:  the Dockerfile sets ENV MODEL_NAME, so one handler can serve different model files without code changes.
# PYTHON: os.getenv(name, default) returns the variable's value, or the default if it is not set.
model_name = os.getenv("MODEL_NAME", "clothing-model-new.onnx")


def preprocess_pytorch_style(X):
    # GOAL: turn keras-image-helper's batch into what a PyTorch-trained network expects.
    # (The original comment says 299 x 299; with target_size=(224, 224) below the shape is (1, 224, 224, 3).)
    # X: shape (1, 299, 299, 3), dtype=float32, values in [0, 255]
    # WHY:  1) scale pixels to [0, 1]
    X = X / 255.0

    # WHY:  2) ImageNet per-channel mean and std: the statistics the pretrained backbone was trained with.
    # PYTHON: reshape(1, 3, 1, 1) lets NumPy broadcast one value per CHANNEL over the whole (1, 3, H, W) batch.
    mean = np.array([0.485, 0.456, 0.406]).reshape(1, 3, 1, 1)
    std = np.array([0.229, 0.224, 0.225]).reshape(1, 3, 1, 1)

    # Convert NHWC → NCHW
    # from (batch, height, width, channels) → (batch, channels, height, width)
    # WHY:  Keras/TF use channels-last (NHWC); PyTorch uses channels-first (NCHW). The ONNX graph keeps the
    #       layout of the framework it came from - check session.get_inputs()[0].shape to know which one.
    # PYTHON: transpose(0, 3, 1, 2) = new axis order, given as positions of the old axes.
    X = X.transpose(0, 3, 1, 2)

    # Normalize
    X = (X - mean) / std

    # WHY:  mean/std are float64, so X became float64. ONNX Runtime refuses float64 for a float32 input
    #       ("Unexpected input data type. Actual: (tensor(double))"): cast back.
    return X.astype(np.float32)


# GOAL: a preprocessor that downloads/opens, resizes to 224 x 224 and applies the function above.
# PYTHON: create_preprocessor accepts either a name ('xception') or any callable (a function) as the first argument.
preprocessor = create_preprocessor(
    preprocess_pytorch_style,
    target_size=(224, 224)
)



# GOAL: load the ONNX graph once per container (module level = cold start only, as in the TF-Lite version).
# WHY:  CPUExecutionProvider is the only provider on Lambda (no GPU); naming it explicitly avoids warnings.
session = ort.InferenceSession(
    model_name, providers=["CPUExecutionProvider"]
)
# GOAL: read the graph's input/output NAMES instead of hard-coding them (ONNX feeds and fetches by name).
# PYTHON: get_inputs() returns NodeArg objects with .name, .shape and .type.
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

classes = [
    "dress",
    "hat",
    "longsleeve",
    "outwear",
    "pants",
    "shirt",
    "shoes",
    "shorts",
    "skirt",
    "t-shirt",
]


def predict(url):
    X = preprocessor.from_url(url)
    # PYTHON: session.run(list_of_output_names, {input_name: array}) returns a LIST of arrays, one per output.
    #         [0] = the first (only) output, shape (1, 10); the second [0] = the row of our single image.
    result = session.run([output_name], {input_name: X})
    # WHY:  .tolist() -> plain Python floats, so the handler's return value is JSON-serialisable.
    #       These are raw LOGITS (scores), not probabilities: the largest one wins.
    float_predictions = result[0][0].tolist()
    return dict(zip(classes, float_predictions))


def lambda_handler(event, context):
    # WHY:  same contract as the lecture: the event dict carries 'url'. A proxy-integration API Gateway event
    #       would carry it inside event['body'] as a JSON string -> KeyError here (the HW9 handler parses both).
    url = event["url"]
    result = predict(url)
    return result

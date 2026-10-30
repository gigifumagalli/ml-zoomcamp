# Commented copy of ../../../../notebooks/workshop/service/app.py (2025 workshop, the HW10-shaped flow).
# ONE service instead of two: FastAPI + ONNX Runtime run the model in-process (no TF Serving, no gRPC).
# Verified while building this folder (uvicorn, clothing-model.onnx downloaded): /health -> {"status":"healthy"},
# /predict on a pants photo -> top_class "pants".

import numpy as np
import onnxruntime as ort
from keras_image_helper import create_preprocessor
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
import uvicorn

# PYTHON: FastAPI() creates the ASGI app; uvicorn serves it ("app:app" = module app.py, variable app).
app = FastAPI(title="clothing-classifier")


# GOAL: reproduce the preprocessing the PyTorch model was trained with.
# WHY:  a PyTorch ImageNet model expects pixels in [0, 1], normalised per channel with the ImageNet
#       mean/std, and channels FIRST (N, C, H, W). Keras/Xception (the lecture) expects channels LAST.
#       Get this wrong and the model still returns numbers - just meaningless ones.
# PYTHON: reshape(1, 3, 1, 1) makes mean/std broadcast over batch, height and width;
#         transpose(0, 3, 1, 2) reorders axes NHWC -> NCHW.
def preprocess_pytorch_style(X):
    X = X / 255.0

    mean = np.array([0.485, 0.456, 0.406]).reshape(1, 3, 1, 1)
    std = np.array([0.229, 0.224, 0.225]).reshape(1, 3, 1, 1)

    X = X.transpose(0, 3, 1, 2)
    X = (X - mean) / std

    return X.astype(np.float32)


# PYTHON: keras_image_helper accepts a custom function instead of a model name like 'xception'.
preprocessor = create_preprocessor(
    preprocess_pytorch_style,
    target_size=(224, 224)
)

# GOAL: load the model ONCE at startup, not per request.
# WHY:  loading takes time and memory; every request would pay it again. It also means a pod is only
#       useful after this line has run - which is what the readinessProbe in k8s/deployment.yaml waits for.
session = ort.InferenceSession(
    "clothing-model.onnx", providers=["CPUExecutionProvider"]
)
# WHY:  read the input/output names from the model instead of hard-coding them ('input_8', 'dense_7' in
#       the lecture) - one less thing that breaks when the model is re-exported.
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


# GOAL: typed request/response contracts. FastAPI validates input against them and answers 422 if invalid.
# PYTHON: pydantic BaseModel = a class whose annotated attributes are checked/converted on creation.
class PredictRequest(BaseModel):
    url: HttpUrl


class PredictResponse(BaseModel):
    predictions: dict[str, float]
    top_class: str
    top_probability: float


def predict(url: str):
    X = preprocessor.from_url(url)
    result = session.run([output_name], {input_name: X})
    float_predictions = result[0][0].tolist()
    predictions_dict = dict(zip(classes, float_predictions))

    # PYTHON: max(d, key=d.get) returns the KEY with the largest value.
    top_class = max(predictions_dict, key=predictions_dict.get)
    # WHY:  despite the name this is a LOGIT, not a probability (the model has no softmax): a pants photo
    #       gave 6.4 in the check run, so test.py's {:.2%} prints "639.59%". Apply softmax for real probabilities.
    top_probability = predictions_dict[top_class]

    return predictions_dict, top_class, top_probability


@app.get("/")
def root():
    return {"message": "Clothing Classification Service"}


# GOAL: a cheap endpoint Kubernetes can poll (liveness + readiness probes). It touches no model code,
#       so it answers fast; it only answers at all once the module above has loaded.
@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict", response_model=PredictResponse)
def predict_endpoint(request: PredictRequest):
    # PYTHON: HttpUrl is a pydantic type, not a str; str() converts it for the image downloader.
    predictions, top_class, top_prob = predict(str(request.url))

    return PredictResponse(
        predictions=predictions,
        top_class=top_class,
        top_probability=top_prob
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

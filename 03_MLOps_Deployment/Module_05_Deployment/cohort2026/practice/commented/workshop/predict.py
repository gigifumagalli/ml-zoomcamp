# Commented copy of 05-deployment/workshop/predict.py: the FastAPI version of the churn service.
# The original is untouched in ../../../notebooks/workshop/predict.py. Code unchanged, comments added.
#
# THIS is the stack Homework 5 uses (FastAPI + uvicorn + uv + one Pipeline artifact).
# The homework's own predict.py follows the same pattern for the lead-scoring model.
#
# Run from practice/ (model.bin is opened relative to the CURRENT directory):
#   uvicorn --app-dir commented/workshop predict:app --host 0.0.0.0 --port 9696
#   (in the workshop folder itself:  uv run uvicorn predict:app --host 0.0.0.0 --port 9696 --reload)
# Then open http://localhost:9696/docs : FastAPI generates an interactive API page from the types below.

import pickle
from typing import Literal
from pydantic import BaseModel, Field


from fastapi import FastAPI
import uvicorn



# GOAL: describe the INPUT contract as a Python class.
# WHY:  Flask hands you whatever JSON arrived; a typo ("contrac") or an impossible value
#       ("streamingtv": "maybe") silently becomes a wrong prediction, because DictVectorizer ignores
#       unknown keys and values. With Pydantic, FastAPI checks every request against this class and
#       answers HTTP 422 with an explanation before the model is ever called.
# PYTHON: a class inheriting from BaseModel; each annotated attribute is a required field.
#         Literal["male", "female"] = only these exact values are accepted.
#         Field(..., ge=0): '...' means required (no default), ge=0 means "greater or equal to 0".
#         Extra unknown keys are ignored by default; model_config = ConfigDict(extra="forbid") rejects them.
class Customer(BaseModel):
    gender: Literal["male", "female"]
    seniorcitizen: Literal[0, 1]
    partner: Literal["yes", "no"]
    dependents: Literal["yes", "no"]
    phoneservice: Literal["yes", "no"]
    multiplelines: Literal["no", "yes", "no_phone_service"]
    internetservice: Literal["dsl", "fiber_optic", "no"]
    onlinesecurity: Literal["no", "yes", "no_internet_service"]
    onlinebackup: Literal["no", "yes", "no_internet_service"]
    deviceprotection: Literal["no", "yes", "no_internet_service"]
    techsupport: Literal["no", "yes", "no_internet_service"]
    streamingtv: Literal["no", "yes", "no_internet_service"]
    streamingmovies: Literal["no", "yes", "no_internet_service"]
    contract: Literal["month-to-month", "one_year", "two_year"]
    paperlessbilling: Literal["yes", "no"]
    paymentmethod: Literal[
        "electronic_check",
        "mailed_check",
        "bank_transfer_(automatic)",
        "credit_card_(automatic)",
    ]
    tenure: int = Field(..., ge=0)
    monthlycharges: float = Field(..., ge=0.0)
    totalcharges: float = Field(..., ge=0.0)


# GOAL: the OUTPUT contract. Same keys as the Flask version (churn_probability, churn).
#       HW5's service answers {"conversion_probability": ..., "conversion": ...} instead.
class PredictResponse(BaseModel):
    churn_probability: float
    churn: bool


# PYTHON: the application object; 'app' is what uvicorn looks for in "predict:app".
app = FastAPI(title="customer-churn-prediction")

# GOAL: load the artifact once at start-up. It is ONE Pipeline (dv + model inside), not a tuple.
with open('model.bin', 'rb') as f_in:
    pipeline = pickle.load(f_in)


def predict_single(customer):
    # WHY: the Pipeline takes the raw dict: its DictVectorizer step does the transform.
    #      (DictVectorizer accepts one dict or a list of dicts; HW5 passes a list: [record].)
    # PYTHON: float() turns np.float64 into a plain float for the JSON response.
    result = pipeline.predict_proba(customer)[0, 1]
    return float(result)


# GOAL: POST /predict. The type hints ARE the validation and the documentation.
# PYTHON: 'customer: Customer' tells FastAPI to parse the JSON body into a Customer (or answer 422);
#         '-> PredictResponse' declares (and checks) the response shape.
#         .model_dump() converts the Pydantic object back into a plain dict for the pipeline
#         (.dict() is the deprecated Pydantic v1 name).
@app.post("/predict")
def predict(customer: Customer) -> PredictResponse:
    prob = predict_single(customer.model_dump())

    return PredictResponse(
        churn_probability=prob,
        churn=prob >= 0.5
    )


# PYTHON: 'python predict.py' starts uvicorn programmatically. The usual way is the CLI:
#         uvicorn predict:app --host 0.0.0.0 --port 9696
# WHY:    uvicorn is an ASGI server (FastAPI's equivalent of gunicorn for Flask). It also runs on Windows.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9696)

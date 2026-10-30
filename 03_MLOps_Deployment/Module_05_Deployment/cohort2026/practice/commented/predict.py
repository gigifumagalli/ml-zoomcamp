# Commented copy of 05-deployment/code/predict.py (lesson 5.4: serving the churn model with Flask).
# The original is untouched in ../../notebooks/code/predict.py. Code unchanged, comments added.
#
# LECTURE stack (2021):  Flask + gunicorn + pipenv, model saved as a (dv, model) tuple.
# HOMEWORK 5 stack (2026): FastAPI + uvicorn + uv, model saved as ONE sklearn Pipeline (pipeline.bin).
# Compare with commented/workshop/predict.py, which is the FastAPI version the homework follows.
#
# Run from practice/ (the model file is opened relative to the CURRENT directory):
#   python commented/predict.py                                        (Flask dev server, debug mode)
#   gunicorn --bind=0.0.0.0:9696 --pythonpath commented predict:app    (production WSGI server)

import pickle

# PYTHON: Flask is the web framework; request gives access to the incoming HTTP request,
#         jsonify turns a dict into an HTTP response with a JSON body.
from flask import Flask
from flask import request
from flask import jsonify


model_file = 'model_C=1.0.bin'

# GOAL: load the artifact ONCE, when the process starts.
# WHY:  loading inside predict() would re-read the file on every request (slow). Module-level code
#       runs once at import, then every request reuses dv and model from memory.
# PYTHON: 'rb' = read binary. pickle.load returns exactly what was dumped: here a 2-tuple,
#         unpacked straight into two names.
with open(model_file, 'rb') as f_in:
    dv, model = pickle.load(f_in)

# PYTHON: Flask('churn') creates the application object. The string is just its name.
#         'app' is what gunicorn looks for in "predict:app" (= module predict, variable app).
app = Flask('churn')

# GOAL: one endpoint, POST /predict, that takes a customer as JSON and returns a churn decision.
# WHY:  POST, not GET, because the client SENDS a body (the customer's features).
# PYTHON: @app.route(...) is a decorator: it registers the function below as the handler for
#         that URL and HTTP method.
@app.route('/predict', methods=['POST'])
def predict():
    # PYTHON: get_json() parses the request body into a Python dict. The client must send the header
    #         Content-Type: application/json (requests.post(url, json=...) does that for you;
    #         with curl you add -H 'Content-Type: application/json').
    customer = request.get_json()

    # WHY: dv.transform expects a LIST of dicts (one per row), hence [customer].
    X = dv.transform([customer])
    # PYTHON: [0, 1] = first (only) row, column 1 = P(churn).
    y_pred = model.predict_proba(X)[0, 1]
    churn = y_pred >= 0.5

    # WHY: float() / bool() convert NumPy types (np.float64, np.bool_) into plain Python types.
    #      jsonify cannot serialise np.bool_, so without bool() the request fails with a TypeError.
    result = {
        'churn_probability': float(y_pred),
        'churn': bool(churn)
    }

    return jsonify(result)


# PYTHON: this block runs only for 'python predict.py', not when gunicorn imports the module.
# WHY:  host='0.0.0.0' listens on all network interfaces, which is required inside Docker
#       (127.0.0.1 would only accept connections from inside the container itself).
#       debug=True is for development only: auto-reload and an interactive debugger in the browser.
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)

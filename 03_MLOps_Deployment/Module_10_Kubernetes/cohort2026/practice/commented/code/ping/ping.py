# Commented copy of ../../../../notebooks/code/ping/ping.py (lesson 10.6).
# The smallest possible web service: one GET endpoint answering "PONG". Used to learn Kubernetes
# without any ML getting in the way. Verified while building this folder: under gunicorn it answers PONG.

from flask import Flask

# PYTHON: Flask(name) creates the application object; gunicorn later imports it as `ping:app`.
app = Flask('ping')


# GOAL: GET /ping -> "PONG". A liveness check in its simplest form.
# WHY: in Kubernetes, an endpoint like this is what a readinessProbe / livenessProbe calls
#      (the workshop and HW10 use GET /health for exactly that).
@app.route('/ping', methods=['GET'])
def ping():
    return "PONG"


# WHY: development server only (`python ping.py`). The Docker image runs gunicorn instead.
#      host='0.0.0.0' = listen on all interfaces; with the default 127.0.0.1, nothing outside the
#      container (port mapping, Kubernetes service) could reach it.
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)

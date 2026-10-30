# Commented copy of 05-deployment/code/ping.py (lesson 5.3: the smallest possible Flask app).
# The original is untouched in ../../notebooks/code/ping.py. Code unchanged, comments added.
# Run:  python commented/ping.py     then:  curl http://localhost:9696/ping
# FastAPI version: commented/workshop/ (the workshop's ping.py is the same thing with FastAPI).

from flask import Flask

# PYTHON: the application object; 'ping' is only its name.
app = Flask('ping')

# GOAL: answer GET /ping with the text PONG - a health check before any ML is involved.
# WHY:  GET because the client sends nothing, it only asks. Opening the URL in a browser is a GET.
@app.route('/ping', methods=['GET'])
def ping():
    return "PONG"

# WHY: port 9696 is the course convention; every service in Module 5 and HW5 uses it.
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)

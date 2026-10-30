# Commented copy of ../../../../notebooks/code/ping/Dockerfile (lesson 10.6).
# GOAL:   image for the ping service. Same recipe as the Module 5 (2021) Dockerfile, different app.
# SYNTAX: build from the COMPLETE folder ../../../../notebooks/code/ping/ (it has the Pipfile.lock):
#         docker build -t ping:v001 .
# WHY:    give an explicit tag (v001). With no tag Docker uses :latest, and Kubernetes then defaults to
#         imagePullPolicy: Always - it tries to pull from Docker Hub instead of using the image you loaded.
# NOTE:   checked while building this folder: `pip install pipenv` + `pipenv install --system --deploy`
#         with this Pipfile.lock still works on Python 3.8 (flask 2.0.2, gunicorn 20.1.0).

FROM python:3.8.12-slim

RUN pip install pipenv

WORKDIR /app

# WHY:    dependency files first, code last -> the install layer is cached across code edits.
COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY "ping.py" .

EXPOSE 9696

# SYNTAX: "ping:app" = module ping.py, Flask object `app`.
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "ping:app"]

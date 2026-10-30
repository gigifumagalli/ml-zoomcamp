# Commented copy of ../../../notebooks/code/image-gateway.dockerfile (lesson 10.4).
# GOAL:   package the Flask gateway (gateway.py + proto.py) with its pinned dependencies.
# SYNTAX: build with  docker build -t zoomcamp-10-gateway:002 -f image-gateway.dockerfile .
# NOTE:   2021 stack: Python 3.8 + pipenv. Module 5 (2026) uses uv + pyproject.toml + uv.lock for the
#         same job; HW10's image is built from homework/05-deployment/Dockerfile, not from this file.

# SYNTAX: slim = Debian with the bare minimum, a much smaller image than the full python image.
FROM python:3.8.12-slim

RUN pip install pipenv

# SYNTAX: WORKDIR creates /app if needed and makes it the current directory for the following lines.
WORKDIR /app

# WHY:    copy ONLY the dependency files first and install. Docker caches each layer: as long as the
#         Pipfiles do not change, editing gateway.py does not re-run the slow install below.
# SYNTAX: the JSON-array form of COPY; the last element is the destination.
COPY ["Pipfile", "Pipfile.lock", "./"]

# WHY:    --system installs into the image's Python (a container needs no virtualenv);
#         --deploy fails the build if Pipfile.lock is out of date instead of silently re-resolving.
RUN pipenv install --system --deploy

COPY ["gateway.py", "proto.py", "./"]

# SYNTAX: EXPOSE is documentation only; publishing the port happens with docker run -p / compose ports.
EXPOSE 9696

# WHY:    gunicorn is a production WSGI server (several workers, no debug mode), unlike app.run().
# SYNTAX: "gateway:app" = module gateway.py, variable app inside it.
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "gateway:app"]

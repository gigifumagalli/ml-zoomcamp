# Commented copy of notebooks/code/image_transfomer/Dockerfile (lesson 11.6). The build context must hold
# Pipfile, Pipfile.lock and image_transformer.py, so point it at the lecture folder. From practice/commented/:
#   docker build -t image-transformer:v1 -f Dockerfile ../../notebooks/code/image_transfomer
#
# GOAL: package image_transformer.py as the transformer tier's container.
# WHY:  KServe runs any container as a transformer, as long as it serves the KServe protocol on port 8080.

# SYNTAX: FROM = base image. python:3.8 is end-of-life (Oct 2024); current kserve needs Python >= 3.10.
FROM python:3.8.12-slim

RUN pip install pipenv

WORKDIR /app

# WHY: copy the lock files first so the dependency layer is cached when only the code changes.
COPY ["Pipfile", "Pipfile.lock", "./"]

# SYNTAX: --system installs into the image's Python (no virtualenv in a container); --deploy fails if the
#         lock is out of date. The lock pins kserve==0.7.0, the only version where KFModel/KFServer exist.
RUN pipenv install --system --deploy

# WHY: the lecture's Dockerfile copies "image_tranformer.py" (missing 's') but the file is image_transformer.py,
#      so the original build fails at this line. Fixed here.
COPY "image_transformer.py" .

# SYNTAX: exec form ENTRYPOINT; KServe appends --model_name and --predictor_host as arguments.
ENTRYPOINT ["python", "image_transformer.py"]

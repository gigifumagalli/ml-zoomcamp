# Commented copy of 05-deployment/workshop/Dockerfile: the uv + FastAPI image.
# The original is untouched in ../../../notebooks/workshop/Dockerfile.
# HW5's Dockerfile (../../homework/Dockerfile) is this same recipe, made stricter: exact image tags
# pinned by digest, 'uv sync --locked --no-dev', and the homework's own files.
#
# Build and run (in notebooks/workshop/, where model.bin, uv.lock and .python-version are):
#   docker build -t predict-churn .
#   docker run -it --rm -p 9696:9696 predict-churn

# GOAL:   base image with the Python version the project was developed with (.python-version = 3.13).
# SYNTAX: FROM <image>:<tag>. 'slim-bookworm' = minimal Debian 12.
FROM python:3.13.5-slim-bookworm

# GOAL:   get the uv binary without installing it with pip.
# SYNTAX: COPY --from=<image> copies files OUT OF another image (here the official uv image) into this one.
# WHY:    ':latest' means a rebuild next month may get a different uv. HW5 pins uv:0.10.11 + a digest.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /code

# GOAL:   put the project's virtualenv first on PATH, so 'uvicorn' below is the one uv installed.
# SYNTAX: ENV KEY="value" sets an environment variable for build steps AND the running container.
ENV PATH="/code/.venv/bin:$PATH"

# GOAL:   dependency files first, code later (layer cache: editing predict.py won't reinstall packages).
# WHY:    .python-version is a hidden file (starts with a dot). If it is missing from the build
#         folder, the build stops here with "not found". ls -a shows it.
COPY "pyproject.toml" "uv.lock" ".python-version" ./
# WHY:    --locked: install exactly uv.lock, fail if it does not match pyproject.toml.
RUN uv sync --locked

COPY "predict.py" "model.bin" ./

# SYNTAX: documentation only; the port is published by 'docker run -p 9696:9696' (HOST:CONTAINER).
EXPOSE 9696

# GOAL:   start the ASGI server. predict:app = variable 'app' in predict.py.
# WHY:    --host 0.0.0.0 so the Mac can reach it through the published port.
ENTRYPOINT ["uvicorn", "predict:app", "--host", "0.0.0.0", "--port", "9696"]

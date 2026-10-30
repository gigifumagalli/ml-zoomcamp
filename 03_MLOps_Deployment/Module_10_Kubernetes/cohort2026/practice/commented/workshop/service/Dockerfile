# Commented copy of ../../../../notebooks/workshop/service/Dockerfile (2025 workshop).
# GOAL:   image for the ONNX FastAPI service: uv-managed environment + app.py + the model file.
# SYNTAX: from the complete folder ../../../../notebooks/workshop/service/:
#         docker build -t clothing-classifier:v1 .
#
# Two fixes before this builds (both found while building this folder):
#  1. clothing-model.onnx is not in the repo. It is in the MANIFEST download list for this workspace; if it is
#     missing, download it from the workshop README link into the service/ folder.
#  2. the checked-in uv.lock is truncated: `uv sync --locked` stops with "Failed to parse uv.lock".
#     And pyproject.toml declares a hatchling build-system, so uv also tries to build the folder as a
#     package (it fails: no package directory, and README.md is not copied).
#     Fix: in service/, run `uv lock` once (regenerates the lock), and use --no-install-project below.
#     The original line is kept as a comment.

# WHY:    pin the Python patch version and Debian release (bookworm); the HW5/HW10 Dockerfile goes further
#         and pins the image digest (@sha256:...) so the bytes can never change under the same tag.
FROM python:3.13.5-slim-bookworm

# GOAL:   get the uv binary without installing it: copy it out of uv's own image (multi-stage COPY).
# NOTE:   :latest is unpinned here; the HW5 Dockerfile pins uv 0.10.11 by digest.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# WHY:    uv creates /app/.venv; putting its bin/ first on PATH makes `uvicorn` below the venv's uvicorn.
ENV PATH="/app/.venv/bin:$PATH"

# WHY:    dependency files first (cached layer), code later. .python-version is a dotfile - easy to lose
#         when copying folders around, and the build fails without it.
COPY pyproject.toml uv.lock .python-version ./

# WHY:    --locked = install exactly the lockfile, fail if it does not match pyproject.toml.
# RUN uv sync --locked
RUN uv sync --locked --no-install-project

COPY app.py clothing-model.onnx ./

EXPOSE 8080

ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]

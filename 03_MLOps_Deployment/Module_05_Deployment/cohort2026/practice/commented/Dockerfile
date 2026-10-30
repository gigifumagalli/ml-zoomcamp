# Commented copy of 05-deployment/code/Dockerfile (lesson 5.6). Original in ../../notebooks/code/Dockerfile.
# LECTURE image (2021): Python 3.8 + pipenv + gunicorn + Flask.
# HOMEWORK 5 image (2026): Python 3.11.15 + uv + uvicorn + FastAPI -> see commented/workshop/Dockerfile
# for the same idea in the homework's stack, and ../homework/Dockerfile for the image you actually build.
#
# Build and run (from the folder that contains predict.py, the Pipfiles and model_C=1.0.bin):
#   docker build -t churn-prediction .
#   docker run -it --rm -p 9696:9696 churn-prediction

# GOAL:   start from an image that already has Python installed.
# WHY:    pins the interpreter for everyone; '-slim' = Debian with the bare minimum (smaller image).
# SYNTAX: FROM <image>:<tag>. Every Dockerfile starts with FROM.
FROM python:3.8.12-slim

# GOAL:   install the environment manager inside the image.
# SYNTAX: RUN executes a shell command at BUILD time; its result becomes a layer of the image.
RUN pip install pipenv

# SYNTAX: WORKDIR creates /app (if needed) and cds into it for every following instruction.
WORKDIR /app

# GOAL:   copy ONLY the dependency files first.
# WHY:    Docker caches each layer. Dependencies change rarely, code changes often: copying the
#         Pipfiles before the code means editing predict.py does not re-install every package.
# SYNTAX: COPY ["src1", "src2", "dest/"] (JSON form) copies files from the build context.
COPY ["Pipfile", "Pipfile.lock", "./"]

# WHY:    --system installs into the image's own Python (a container is already isolated, so a
#         virtualenv inside it adds nothing). --deploy fails if Pipfile.lock is out of date
#         instead of silently re-resolving: the image gets exactly the locked versions.
RUN pipenv install --system --deploy

# GOAL:   now the code and the model artifact.
COPY ["predict.py", "model_C=1.0.bin", "./"]

# SYNTAX: EXPOSE documents the port the service listens on. It does NOT publish it: that is
#         docker run -p HOST:CONTAINER (here -p 9696:9696).
EXPOSE 9696

# GOAL:   the command the container runs when it starts.
# WHY:    gunicorn, not 'python predict.py': Flask's built-in server is for development only.
#         --bind=0.0.0.0 so connections from outside the container (your Mac) are accepted.
# SYNTAX: the JSON (exec) form runs gunicorn directly as PID 1, without a shell in between,
#         so Ctrl+C / docker stop reach it.
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "predict:app"]

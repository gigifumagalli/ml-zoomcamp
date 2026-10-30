# Commented copy of 09-serverless/workshop/lambda-onnx/Dockerfile (the ONNX workshop: the CURRENT stack).
# The original is untouched in ../../../notebooks/workshop/lambda-onnx/Dockerfile.
# Build it from notebooks/workshop/lambda-onnx/ (the build context must contain the .onnx file and lambda_function.py).

# GOAL: the official AWS Lambda base image, Python 3.13.
# WHY:  ships with the Runtime Interface Client + Emulator: the container answers on port 8080 locally exactly like
#       a deployed Lambda. Multi-arch tag: on Apple Silicon it pulls arm64, on Intel/AWS x86_64 it pulls amd64.
# SYNTAX: FROM image:tag. HW9 pins the image by digest (@sha256:...), so the build cannot drift.
FROM public.ecr.aws/lambda/python:3.13

# GOAL: install the inference runtime and the image helper.
# WHY:  no custom wheel needed (contrast with the TF-Lite Dockerfile): onnxruntime publishes manylinux wheels.
# NOTE: onnxruntime is unpinned here, so a rebuild next year may get a different version. HW9 pins every
#       package in requirements-lambda.txt - prefer that pattern for anything you ship.
RUN pip install onnxruntime keras-image-helper==0.0.2

# GOAL: make the model file name a build parameter AND a runtime environment variable.
# SYNTAX: ARG = exists only during 'docker build' (override with --build-arg MODEL_NAME=...).
#         ENV = baked into the image, visible to the running code: lambda_function.py reads os.getenv("MODEL_NAME").
ARG MODEL_NAME=clothing_classifier_mobilenet_v2_latest.onnx
ENV MODEL_NAME=${MODEL_NAME}

# GOAL: copy the model next to the code (the working directory is ${LAMBDA_TASK_ROOT} = /var/task).
# SYNTAX: ${MODEL_NAME} is expanded by Docker at build time.
COPY ${MODEL_NAME} ${MODEL_NAME}

# WHY:  code LAST: it changes most often, and Docker reuses every cached layer above an unchanged line.
COPY lambda_function.py ./

# GOAL: the handler to call, as <module>.<function>.
CMD ["lambda_function.lambda_handler"]

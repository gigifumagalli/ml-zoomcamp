# Commented copy of 09-serverless/code/Dockerfile (lesson 9.5, the TF-Lite LECTURE stack).
# The original is untouched in ../../../notebooks/code/Dockerfile.
# OUTDATED: needs clothing-model.tflite (produced by convert-model.py, which needs TensorFlow) and a custom
# tflite_runtime wheel built for Python 3.10 on Amazon Linux. HW9 uses ../../../homework/Dockerfile instead.

# GOAL: start from the official AWS Lambda Python image.
# WHY:  it already contains the Lambda Runtime Interface Client AND the Runtime Interface Emulator, so the same
#       image runs locally (docker run -p 8080:8080) and on AWS without changes.
# SYNTAX: FROM <registry>/<repository>:<tag>. Tag 3.10 = Python 3.10.
FROM public.ecr.aws/lambda/python:3.10

# GOAL: install the image-preprocessing helper.
# SYNTAX: RUN executes a shell command at BUILD time; the result becomes a layer of the image.
RUN pip install keras-image-helper
# GOAL: install the TF-Lite interpreter from a wheel compiled for Amazon Linux + Python 3.10 (cp310, x86_64).
# WHY:  the wheel on PyPI was built against a newer glibc than Amazon Linux has ("GLIBC_2.27 not found",
#       lesson 9.5), so Alexey compiled one for Lambda. On an Apple Silicon Mac this x86_64 wheel only installs
#       when the image is built with --platform linux/amd64.
# NOTE: lesson 9.10 adds numpy==1.23.1 and --no-deps here, because this wheel was compiled against NumPy 1.
RUN pip install https://github.com/alexeygrigorev/tflite-aws-lambda/raw/main/tflite/tflite_runtime-2.14.0-cp310-cp310-linux_x86_64.whl

# GOAL: put the model and the code into the image's working directory (${LAMBDA_TASK_ROOT} = /var/task).
# SYNTAX: COPY <path on your machine, relative to the build context> <path in the image>; '.' = the WORKDIR.
COPY clothing-model.tflite .
COPY lambda_function.py .

# GOAL: tell the Lambda runtime which function to call: <file without .py>.<function name>.
# SYNTAX: CMD in exec form (a JSON list). In Lambda images CMD is the handler, not a shell command.
CMD [ "lambda_function.lambda_handler" ]

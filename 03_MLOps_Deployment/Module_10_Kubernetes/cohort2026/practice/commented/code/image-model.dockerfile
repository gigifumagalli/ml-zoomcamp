# Commented copy of ../../../notebooks/code/image-model.dockerfile (lesson 10.4).
# GOAL:   bake the SavedModel into the TF Serving image, so the container needs no -v volume and no -e flag.
# WHY:    an image that contains its model is one immutable, versioned artifact: the same tag runs
#         identically under docker run, docker-compose and Kubernetes (which cannot mount your laptop folder).
# SYNTAX: build with  docker build -t zoomcamp-10-model:xception-v4-001 -f image-model.dockerfile .
#         -f picks a Dockerfile with a non-default name; the final '.' is the build context (current folder).
# NOTE:   needs the clothing-model/ SavedModel folder next to this file (converted from the Module 8 Keras
#         model in lesson 10.2). It is not in this workspace.

# GOAL:   start from Google's official TF Serving server (C++ binary, gRPC on 8500, REST on 8501).
# SYNTAX: FROM <image>:<tag> - always pin the tag; 'latest' changes under your feet.
FROM tensorflow/serving:2.7.0

# GOAL:   put the model where TF Serving looks for it: /models/<MODEL_NAME>/<version>/
# WHY:    the version sub-folder (1) is mandatory; without it TF Serving finds no servable.
# SYNTAX: COPY <path in build context> <path in image>
COPY clothing-model /models/clothing-model/1

# GOAL:   tell the server which folder under /models to load. Must equal the folder name above.
# SYNTAX: ENV KEY="value" sets an environment variable for every container started from this image.
ENV MODEL_NAME="clothing-model"

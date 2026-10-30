# Commented copy of notebooks/code/image_transfomer/image_transformer.py (lesson 11.6).
#
# 2026: this is the kserve 0.7 API (the version pinned in the Pipfile). From kserve 0.8 on:
#       kserve.KFModel -> kserve.Model, kserve.KFServer -> kserve.ModelServer,
#       kserve.kfserver.parser -> kserve.model_server.parser, and preprocess/postprocess became
#       `async def preprocess(self, payload, headers=None)` / `async def postprocess(self, result, headers=None, ...)`.
#       Upgrading kserve without these edits fails at import time (AttributeError: KFModel).

import kserve
from typing import List, Dict

# PYTHON: keras_image_helper is Alexey's tiny package (Module 8-10): URL -> resized, normalised NumPy array,
#         without installing TensorFlow in the transformer image.
from keras_image_helper import create_preprocessor


# GOAL: a transformer = a KServe model that does NOT predict. It edits the request on the way in
#       (preprocess) and the response on the way out (postprocess); KServe forwards to the predictor in between.
# WHY: the same split as Module 10's gateway: heavy model in TF Serving, light Python logic in front.
class ImageTransformer(kserve.KFModel):
    def __init__(self, name: str, predictor_host: str):
        # PYTHON: super().__init__(name) runs the parent class's constructor (registers the model name).
        super().__init__(name)
        # WHY: KServe passes the predictor's address; the base class POSTs the preprocessed body there.
        self.predictor_host = predictor_host
        # WHY: Xception expects 299x299 images scaled to [-1, 1]; the preprocessor knows that recipe.
        self.preprocessor = create_preprocessor('xception', target_size=(299, 299))
        # WHY: the model returns 10 scores in this exact order; the labels must match the training order.
        self.classes = [
            'dress',
            'hat',
            'longsleeve',
            'outwear',
            'pants',
            'shirt',
            'shoes',
            'shorts',
            'skirt',
            't-shirt'
        ]

    # GOAL: one URL -> one image as nested Python lists (JSON cannot carry NumPy arrays).
    # PYTHON: from_url returns a batch of shape (1, 299, 299, 3); X[0] is the single image; .tolist() -> lists.
    def prepare_input(self, url: str) -> List:
        X = self.preprocessor.from_url(url)
        return X[0].tolist()

    # GOAL: client body {"instances": [{"url": ...}, ...]} -> predictor body {"instances": [image, ...]}.
    # WHY: the client sends tiny URLs; only the cluster-internal hop carries the multi-MB JSON tensors.
    def preprocess(self, request: Dict) -> Dict:
        result = []

        # NOTE: test-transformer.py sends instances as {'url': ...} dicts (the format of Alexey's prebuilt
        #       transformer image in clothes-service.yaml), but prepare_input expects a URL STRING here.
        #       With this class, send plain URL strings or call self.prepare_input(url['url']).
        for url in request['instances']:
            row = self.prepare_input(url)
            result.append(row)

        return {'instances': result}

    # GOAL: predictor body {"predictions": [[10 scores], ...]} -> {"predictions": [{label: score}, ...]}.
    # PYTHON: zip pairs label i with score i; dict() turns those pairs into {label: score}.
    def postprocess(self, response: Dict) -> Dict:
        result = []

        for prediction in response['predictions']:
            output = dict(zip(self.classes, prediction))
            result.append(output)

        return {'predictions': result}

# PYTHON: this block runs only when the file is executed (python image_transformer.py), not when imported.
if __name__ == '__main__':
    import argparse

    # PYTHON: parents=[...] inherits KServe's standard server flags (ports, workers) into our parser.
    parser = argparse.ArgumentParser(parents=[kserve.kfserver.parser])
    parser.add_argument("--predictor_host", help="The URL for the model predict function", required=True)
    parser.add_argument("--model_name", help="The name of the model", required=True)

    # PYTHON: parse_known_args ignores flags we did not declare instead of crashing on them.
    args, _ = parser.parse_known_args()

    model_name = args.model_name
    host = args.predictor_host

    # NOTE: 'tranformer' (sic) is the lecture's variable name; kept so the file diffs cleanly with the original.
    tranformer = ImageTransformer(model_name, predictor_host=host)

    # GOAL: start the HTTP server (port 8080) and register the transformer under its name.
    server = kserve.KFServer()
    server.start(models=[tranformer])

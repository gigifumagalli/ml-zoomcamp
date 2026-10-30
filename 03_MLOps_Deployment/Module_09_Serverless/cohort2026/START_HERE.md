# Module 9 — Serverless Deep Learning, session plan

Everything is in this folder. Nothing to download: the two ONNX models (HW9 hair classifier, 80 MB in two files; workshop clothing MobileNetV2, 10 MB) and the test images are already here.

**Homework 9:** platform deadline **Mon 7 Dec**. Target: submit in the Tue 1 Dec 08:00 session.
**Submit at:** https://courses.datatalks.club/ml-zoomcamp-2026/homework/hw09

> **The lecture and the homework use different stacks.** Videos 9.3 – 9.6 use **TF-Lite** (Python 3.10, custom wheel, keras-image-helper); Alexey's own README marks them outdated. **HW9 uses ONNX Runtime** with plain Pillow preprocessing and its own pinned Dockerfile. The bridge is the ONNX workshop ([notebooks/workshop/README.md](notebooks/workshop/README.md), 1,929 words), and `practice/09-serverless_commented.ipynb` follows the lessons' order but runs the workshop's ONNX code. Watch 9.3 – 9.6 for the ideas (why not TensorFlow, model loading, Docker, ECR), don't copy their code into HW9.

---

## Sessions

**Session 1 — Fri 27 Nov, 08:00.** Read [9.1](lessons/01-intro.md) → [9.4](lessons/04-preparing-code.md) (~4,000 words, ~17 min), then the workshop README's "AWS Lambda" and "TensorFlow/PyTorch Models" parts. In `practice/`: the handler as a plain function, the scikit-learn Lambda, an ONNX session (inputs/outputs), preprocessing by hand, `NEAREST` vs `BILINEAR`, calling `lambda_function.py` locally (commented notebook 9.1 – 9.4).

**Session 2 — Mon 30 Nov, 08:00.** Read [9.5](lessons/05-docker-image.md) → [9.7](lessons/07-api-gateway.md) (~3,000 words, ~12 min): the Lambda base image, ECR + creating the function, API Gateway and its two event shapes (commented notebook 9.5 – 9.7). Then HW9 **setup, Q1 – Q4** (all local Python). HW8 closes tonight.

**Session 3 — Tue 1 Dec, 08:00.** HW9 **smoke test, Q5, Q6** (build and run the container, curl it), check, **submit** (target; closes Mon 7 Dec). [9.8](lessons/08-summary.md) → [9.10](lessons/10-updates.md) (~1,000 words) as reading in the evening slot. Playbook cards: serverless vs serverful, ONNX as the inference format, preprocessing as part of the model interface.

> Sun 29 Nov 09:00 – 11:00 is the Capstone 1 weekend block, not Module 9.
> AWS account, CLI and billing alarm come from the November setup session (Module 8 week). Lambda + API Gateway stay inside the free tier for test calls; afterwards `aws lambda delete-function`, `aws apigateway delete-rest-api` and `aws ecr delete-repository --force` (the ECR image is the only part that keeps billing).
> Docker Desktop must be running for Q6 and for building the workshop image.
> Only three slots. If it gets tight, drop the AWS deployment first (optional in HW9, not graded), then Q5 – Q6. Homework isn't required for the certificate.

---

## Five traps in this homework

**1. The lecture code is the wrong stack.** TF-Lite, `public.ecr.aws/lambda/python:3.10`, Xception 299 × 299 channels-last, `x / 127.5 - 1`, event key `url`, port 8080. HW9: ONNX Runtime, its own pinned `Dockerfile` and `requirements-lambda.txt`, channels-first with ImageNet mean/std, event key `image_url`, port 9000. Start from the files in `homework/`, not from `notebooks/code/`.

**2. keras-image-helper resizes with `NEAREST`; HW9 pins `BILINEAR`.** The workshop's `preprocess_pytorch_style` looks exactly like HW9's normalisation, but the helper underneath uses `NEAREST`. Checked on the pants photo with the HW9 model: **0.79 with `BILINEAR`, 0.34 with `NEAREST`**, while the top-left pixel was identical in both. A correct Q3 does not prove a correct Q4. Use the pinned `prepare_image`.

**3. One model, two files.** `hair_classifier_v1.onnx` (10 KB graph) points to `hair_classifier_v1.onnx.data` (80 MB weights) by name. Separate or rename the `.data` file and `InferenceSession` fails with *"cannot get file size ... hair_classifier_v1.onnx.data"*. Both stay in `homework/`; the Dockerfile copies both.

**4. ONNX Runtime checks dtype and layout strictly.** `float64` → *"Unexpected input data type. Actual: (tensor(double))"*; channels-last → *"Got invalid dimensions for input"*. The output has shape `(1, 1)` and is already a probability: take the single value, no extra sigmoid.

**5. The container answer is wrapped twice.** Call `localhost:9000` (`-p 9000:8080`), send `{"image_url": ...}`, and the reply's `body` is a JSON **string**: `json.loads(resp['body'])['straight_probability']`. Q6 must match Q4 within tolerance; if it doesn't, the image is stale or the files differ.

---

## Lessons in this folder

| File | Title | Words | Video |
|---|---|---:|---|
| [01-intro.md](lessons/01-intro.md) | 9.1 Introduction to Serverless | 601 | [video](https://www.youtube.com/watch?v=JLIVwIsU6RA&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [02-aws-lambda.md](lessons/02-aws-lambda.md) | 9.2 AWS Lambda | 1,370 | [video](https://www.youtube.com/watch?v=_UX8-2WhHZo&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [03-tensorflow-lite.md](lessons/03-tensorflow-lite.md) | 9.3 TensorFlow Lite (outdated) | 1,386 | [video](https://www.youtube.com/watch?v=OzZA4mSBE0Q&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [04-preparing-code.md](lessons/04-preparing-code.md) | 9.4 Preparing the code for Lambda (outdated) | 668 | [video](https://www.youtube.com/watch?v=XXBUivsHhec&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [05-docker-image.md](lessons/05-docker-image.md) | 9.5 Preparing a Docker image (outdated) | 1,109 | [video](https://www.youtube.com/watch?v=y4_YQjfOsDo&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [06-creating-lambda.md](lessons/06-creating-lambda.md) | 9.6 Creating the lambda function (outdated) | 1,207 | [video](https://www.youtube.com/watch?v=kBch5oD5BkY&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [07-api-gateway.md](lessons/07-api-gateway.md) | 9.7 API Gateway: exposing the lambda function | 661 | [video](https://www.youtube.com/watch?v=wyZ9aqQOXvs&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [08-summary.md](lessons/08-summary.md) | 9.8 Summary | 555 | [video](https://www.youtube.com/watch?v=bu3nPiHCNLU&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [09-explore-more.md](lessons/09-explore-more.md) | 9.9 Explore more | 275 | — |
| [10-updates.md](lessons/10-updates.md) | 9.10 Python 3.12 vs TF Lite 2.17 | 188 | — |

~8,020 words ≈ 33 min of reading (+ 1,929 for the workshop README, [video](https://www.youtube.com/watch?v=sHQaeVm5hT8)). Alexey's lecture notebook and the workshop are in [notebooks/](notebooks/).

## What is where

```
cohort2026/
├── START_HERE.md                          ← this file
├── lessons/                               ← 10 written lessons + images/
├── notebooks/
│   ├── 09-serverless-lecture.ipynb        ← Alexey's TF-Lite notebook (reference: needs TensorFlow + the .h5, not installed)
│   ├── pants.jpg                          ← the lecture's test image
│   ├── code/                              ← the lecture's files, verbatim (lambda_function.py, Dockerfile, test.py, ...)
│   └── workshop/                          ← the ONNX workshop, verbatim; lambda-onnx/ has its model, ready to docker build
├── practice/
│   ├── 09-serverless_practice.ipynb       ← your practice notebook
│   ├── 09-serverless_commented.ipynb      ← the commented walkthrough (ONNX path, all cells run on CPU)
│   ├── commented/                         ← lecture_tflite/ and workshop_onnx/ files with GOAL/WHY comments
│   └── pants.jpg · clothing_classifier_mobilenet_v2_latest.onnx · data-week-3.csv
└── homework/
    ├── Homework9_2026.ipynb               ← scaffold: setup, Q1–Q6, no answers
    ├── homework9_2026.md                  ← the official question text
    ├── Dockerfile · lambda_function.py · smoke_test.py · requirements*.txt · asset_manifest.json
    └── hair_classifier_v1.onnx + .onnx.data · sample.jpeg   ← the frozen, checksummed assets
```

## Connections

- [Home](../../../00_Reference_Materials/Home.md) · [Resource Map](../../../00_Reference_Materials/Resource_Map_Cohort2026.md)
- [Playbook](../../../00_Reference_Materials/ML_Strategist_Playbook.md): *Shipping the model* (the arm64/amd64 gotcha matters here)

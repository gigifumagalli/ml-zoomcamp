
# Module 11 — KServe, session plan

Everything to read is in this folder. The KServe install (11.2) and the clothing model (11.5, the Module 10 download link) come from the internet when you get there.

**No homework: Module 11 is optional and not part of the 2026 cohort.** The cohort ends at Module 10; certification is the midterm + Capstone 1 (complete Mon 11 Jan 2027).

---

## Sessions

No fixed dates. If you do it, take four 08:00 slots after certification:

**Session 1 — Tue 12 Jan, 08:00.** Watch [11.1](lessons/01-overview.md) → [11.2](lessons/02-kserve-local.md) (~180 words + 2 videos). Install KServe on kind with the 2026 commands in `practice/11-kserve_commented.ipynb` (section 11.2), deploy the iris example, call it.

**Session 2 — Wed 13 Jan, 08:00.** Watch [11.3](lessons/03-kserve-sklearn.md) → [11.4](lessons/04-kserve-custom-image.md) (~150 words + 2 videos). Retrain the churn pipeline in `practice/`, then deploy it. Use the 2026 variant (`churn-train-2026.py` + `churn-service-2026.yaml`): the lecture version does not run on current KServe (traps 3 and 4).

**Session 3 — Thu 14 Jan, 08:00.** Watch [11.5](lessons/05-tensorflow-kserve.md) → [11.6](lessons/06-kserve-transformers.md) (~160 words + 2 videos). Convert the clothing model, deploy predictor + transformer, test with URLs.

**Session 4 — Fri 15 Jan, 08:00.** Watch [11.7](lessons/07-kserve-eks.md), then read [the 2022 update](lessons/07-kserve-eks-upd.md) and [11.8](lessons/08-summary.md) → [11.9](lessons/09-explore-more.md) (~400 words + 1 video). Watching is enough: EKS costs money by the hour. Delete the kind cluster, then write the Playbook card: InferenceService, predictor vs transformer, train/serve version pinning.

> Skip it entirely if January is for portfolio polish and applications. Nothing depends on it.
> Needs the kind cluster from Module 10 (Docker Desktop, kind, kubectl). Check `kubectl version` first: current KServe needs a server >= v1.32.
> The lesson pages are video stubs: the written notes are empty ("Add notes from the video"). The substance is in the videos and in `notebooks/code/`.
> Two pages for 11.7: `07-kserve-eks.md` is the video page; `07-kserve-eks-upd.md` (13 July 2022) is the newer text with the commands to use instead of the video's. Read both, in that order.

---

## 6 traps in this module

**1. The 2022 install commands are dead.** Lesson 11.2 pins kind 0.11.1, kubectl 1.21, `kindest/node:v1.21.1` and KServe 0.8's `release-0.8/hack/quick_install.sh` (the script is gone from current releases). KServe 0.20/0.21 needs Kubernetes >= 1.32 and installs from the release scripts (`kserve-knative-mode-full-install-with-manifests.sh`). Module 10's `kindest/node:v1.23.0` is too old as well. The EKS update pins Kubernetes 1.21 (EKS no longer creates it) and Istio 1.6.2. `apiVersion: serving.kserve.io/v1beta1` is still current.

**2. `churn-train.py` fails on pandas 3, with a misleading error.** `df.dtypes == 'object'` selects nothing, so every churn label is 0, and scikit-learn 1.9 reports *"'liblinear' solver does not support multiclass classification"*, although the real problem is a single class. Use `select_dtypes(include=['object', 'string'])`, as `practice/commented/churn-train.py` does.

**3. Train with the scikit-learn version of the server, not yours.** The server unpickles `model.joblib` with its own version: KServe 0.21's image ships scikit-learn 1.5.2 (and pandas < 3). A model pickled with your 1.9 returns HTTP 500 *"'LogisticRegression' object has no attribute 'multi_class'"* (checked). The repo's 2022 `model.joblib` is scikit-learn 1.0: on 1.9 it predicts but crashes when printed. Train in a separate env: `conda create -n kserve-train python=3.12 "scikit-learn=1.5.2" "pandas<3" joblib`.

**4. Current KServe hands the model a DataFrame, not a list of dicts.** With the lecture's request, the 0.21 server answers 500 *"If using all scalar values, you must pass an index"*. With `{"contract": ["one_year"], ...}` rows, the `DictVectorizer` pipeline fails on *"'str' object has no attribute 'items'"*. What works (checked against KServe 0.21's sklearn server, run locally): `OneHotEncoder` in a `ColumnTransformer` (`churn-train-2026.py`), values wrapped in lists, and `PREDICT_PROBA=true` in the YAML. That variable also replaces the custom predict_proba image of 11.4 (`agrigorev/sklearnserver:3.8-1.0-predict-proba`, built for scikit-learn 1.0).

**5. Every `storageUri` points somewhere you can't reach.** `http://172.31.13.90:8000/...` (churn, clothes) is the private IP of Alexey's EC2 machine. Upload the model to S3/GCS or any URL your cluster reaches. The iris bucket moved: use `gs://kfserving-examples/models/sklearn/1.0/model` (lesson 11.2's update, and what KServe's samples still use). A folder URI must hold exactly one model file.

**6. The image transformer doesn't build or run as written.** The Dockerfile copies `image_tranformer.py` but the file is `image_transformer.py` (the folder is `image_transfomer`, also a typo). The code uses `kserve.KFModel`, `KFServer` and `kserve.kfserver.parser`, which exist only up to `kserve==0.7.0` (the Pipfile pin, Python 3.8). From 0.8 on they are `kserve.Model`, `kserve.ModelServer`, `kserve.model_server.parser`, and current kserve needs Python >= 3.10. `test-transformer.py` sends `{'url': ...}` dicts, which suit Alexey's prebuilt transformer image but not this class (it expects plain URL strings).

---

## Lessons in this folder

| File | Title | Words | Video |
|---|---|---:|---|
| [01-overview.md](lessons/01-overview.md) | 11.1 Overview | 60 | [video](https://www.youtube.com/watch?v=CFWK05dQoGM&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [02-kserve-local.md](lessons/02-kserve-local.md) | 11.2 Running KServe locally | 120 | [video](https://www.youtube.com/watch?v=A3tFt14iTEI&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [03-kserve-sklearn.md](lessons/03-kserve-sklearn.md) | 11.3 Deploying a Scikit-Learn model with KServe | 73 | [video](https://www.youtube.com/watch?v=8kBIDggLwgE&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [04-kserve-custom-image.md](lessons/04-kserve-custom-image.md) | 11.4 Deploying custom Scikit-Learn images with KServe | 75 | [video](https://www.youtube.com/watch?v=REGNWrHZiCw&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [05-tensorflow-kserve.md](lessons/05-tensorflow-kserve.md) | 11.5 Serving TensorFlow models with KServe | 87 | [video](https://www.youtube.com/watch?v=iXwQb2LRKGI&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [06-kserve-transformers.md](lessons/06-kserve-transformers.md) | 11.6 KServe transformers | 70 | [video](https://www.youtube.com/watch?v=haowRqeAqJU&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [07-kserve-eks.md](lessons/07-kserve-eks.md) | 11.7 Deploying with KServe and EKS | 76 | [video](https://www.youtube.com/watch?v=MpuTzBSYBBI&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [07-kserve-eks-upd.md](lessons/07-kserve-eks-upd.md) | 11.7 update (13 July 2022): EKS commands without a custom domain | 202 | — |
| [08-summary.md](lessons/08-summary.md) | 11.8 Summary | 69 | — |
| [09-explore-more.md](lessons/09-explore-more.md) | 11.9 Explore more | 56 | — |

~890 words ≈ 4 min of reading; the content is in the 7 videos. Alexey's code is in [notebooks/code/](notebooks/code/).

## What is where

```
cohort2026/
├── START_HERE.md                         ← this file
├── lessons/                              ← 10 lesson pages (video stubs; two for 11.7) + images/
├── notebooks/
│   └── code/                             ← Alexey's code, verbatim: churn/, iris/, clothes/, image_transfomer/, eks/, plan.md
└── practice/
    ├── 11-kserve_practice.ipynb          ← your practice notebook (Telco data loaded)
    ├── 11-kserve_commented.ipynb         ← commented walkthrough: churn train → YAML → request, 2026 variant, transformer
    ├── data-week-3.csv                   ← Telco churn (same file as Modules 3-4)
    └── commented/                        ← commented copies: churn-train.py, churn-service.yaml, churn-test.py,
                                            iris-example.yaml, clothes-service.yaml, image_transformer.py, Dockerfile,
                                            + 2026 variants churn-train-2026.py, churn-service-2026.yaml
```

## Connections

- [Home](../../../00_Reference_Materials/Home.md) · [Resource Map](../../../00_Reference_Materials/Resource_Map_Cohort2026.md)

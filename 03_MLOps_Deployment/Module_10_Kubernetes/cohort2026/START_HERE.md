# Module 10 — Kubernetes and TensorFlow Serving, session plan

Everything is in this folder. Nothing to download. (The workshop's ONNX model, 9.8 MB, is already in `notebooks/workshop/service/`.)

**Homework 10:** platform deadline **Mon 14 Dec**. Target: submit in the Mon 7 Dec session, so Module 10 is closed before Capstone 1 starts on Tue 8 Dec.
**Submit at:** https://courses.datatalks.club/ml-zoomcamp-2026/homework/hw10

**The lecture is not the homework.** The lessons deploy a TF Serving image model plus a Flask gateway (two deployments, gRPC, docker-compose). HW10 deploys the **HW5 lead-scoring FastAPI image** to a named `kind` cluster: one Deployment, one `ClusterIP` Service with port-forward, one HPA. The workshop (`notebooks/workshop/`) is the material that looks like HW10; the commented notebook gives it its own section.

---

## Sessions

**Before Session 1 — install the tools** (Docker Desktop is already on the Mac):

```bash
brew install kind kubectl
kind --version && kubectl version --client
```

That is all HW10 needs: the image builds its own Python environment inside Docker, and `q6_test.py` uses only the standard library.

**Session 1 — Wed 2 Dec, 08:00.** Read [10.1](lessons/01-overview.md) → [10.4](lessons/04-docker-compose.md) (~3,770 words, ~16 min). TF Serving, the gateway, `proto.py`, docker-compose: read sections 10.1–10.4 of `practice/10-kubernetes_commented.ipynb`. They are read-only, because the SavedModel and the 2021 stack are not here and HW10 does not use them.

**Session 2 — Wed 2 Dec, 20:00 (long hour).** Read [10.5](lessons/05-kubernetes-intro.md) (~1,190 words). Pods, deployments, services, HPA. Then the first half of the 10.6 sequence in the commented notebook: build and run the ping image, `kind create cluster`, `kubectl get service / pod / deployment`.

**Session 3 — Thu 3 Dec, 08:00.** Read [10.6](lessons/06-kubernetes-simple-service.md) → [10.7](lessons/07-kubernetes-tf-serving.md) (~2,640 words). Deploy ping: deployment, `kind load docker-image`, service, port-forward. Run the 10.7 cells and the **workshop section** (probes, requests, HPA: the HW10 shape). Then `kind delete cluster`.

**Session 4 — Fri 4 Dec, 08:00.** Skim [10.8](lessons/08-eks.md) and read [10.9](lessons/09-summary.md) → [10.10](lessons/10-explore-more.md) (~2,100 words). Don't create an EKS cluster: it's optional and costs money. Then HW10 **Q1–Q5**: build and run the image, version check, named cluster, `kubectl get services`, `kind load`. Leave the cluster running for Monday.

**Session 5 — Mon 7 Dec, 08:00.** HW10 **Q6–Q8** (deployment, service + port-forward, HPA), clean up, **submit**. Then the Playbook cards: Deployment, Service types, probes, HPA, kind. **All course modules are done.**

> Sun 6 Dec 09:00–11:00 is the Capstone 1 weekend block. It is not HW10 time.
> Capstone 1 starts Tue 8 Dec. Don't let HW10 run into it: it isn't required for the certificate. If Monday doesn't close it, drop it rather than use the extra week.
> If you do try EKS anyway: `eksctl delete cluster --name mlzoomcamp-eks` the same day. The cluster, the node and the load balancer are billed by the hour.
> The kind cluster lives in a Docker container and usually comes back when Docker Desktop restarts. If `kubectl cluster-info --context kind-mlzoomcamp-2026` fails on Monday, recreate it and run `kind load` again (a few minutes).

---

## Five traps in this homework

**1. The paths in `homework10_2026.md` are for the course repo, not this folder.** Here the HW5 release is the subfolder `homework/05-deployment/`. Build with `cd 05-deployment && docker build -t zoomcamp-model:2026-hw10 .` and test from `homework/` with `python 05-deployment/q6_test.py`, not `../05-deployment/q6_test.py`.

**2. The cluster only runs the exact tag you loaded.** `deployment.yaml` asks for `zoomcamp-model:2026-hw10` (the HW5 text built `:2026-hw5`; `docker tag` gives it the second name). kind nodes can't see Docker Desktop's images, so run `kind load docker-image zoomcamp-model:2026-hw10 --name mlzoomcamp-2026` after every build. If you skip it, use the wrong tag, or leave out `--name`, the pod sits in `ErrImagePull` / `ImagePullBackOff`. `kubectl describe pod` shows why.

**3. One cluster, two names.** kind commands take `--name mlzoomcamp-2026`. kubectl commands take `--context kind-mlzoomcamp-2026`. Without `--name`, kind looks for a cluster called `kind`. Without `--context`, kubectl may talk to another cluster, such as Docker Desktop's own Kubernetes or your Thursday practice cluster.

**4. Port-forward to the service port, from a free local port.** `service.yaml` maps port 80 to `targetPort` 9696, so the command is `kubectl port-forward service/subscription 9696:80` (`9696:9696` fails). "address already in use" means the Q1 container is still running. The port-forward blocks its terminal, so run `q6_test.py` from a second one.

**5. HPA `TARGETS <unknown>` is not a failure.** kind has no metrics-server, so the HPA can't read CPU yet. Q8 asks about what `hpa.yaml` declares, not what the cluster does. Installing metrics-server is optional; the commands are in the workshop section of the commented notebook.

---

## Lessons in this folder

| File | Title | Words | Video |
|---|---|---:|---|
| [01-overview.md](lessons/01-overview.md) | 10.1 Overview | 957 | [video](https://www.youtube.com/watch?v=mvPER7YfTkw&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [02-tensorflow-serving.md](lessons/02-tensorflow-serving.md) | 10.2 TensorFlow Serving | 1,022 | [video](https://www.youtube.com/watch?v=deXR2fThYDw&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [03-preprocessing.md](lessons/03-preprocessing.md) | 10.3 Creating a pre-processing service | 1,008 | [video](https://www.youtube.com/watch?v=OIlrS14Zi0o&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [04-docker-compose.md](lessons/04-docker-compose.md) | 10.4 Running everything locally with Docker-compose | 780 | [video](https://www.youtube.com/watch?v=ZhQQfpWfkKY&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [05-kubernetes-intro.md](lessons/05-kubernetes-intro.md) | 10.5 Introduction to Kubernetes | 1,188 | [video](https://www.youtube.com/watch?v=UjVkpszDzgk&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [06-kubernetes-simple-service.md](lessons/06-kubernetes-simple-service.md) | 10.6 Deploying a simple service to Kubernetes | 1,515 | [video](https://www.youtube.com/watch?v=PPUCVRIV9t8&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [07-kubernetes-tf-serving.md](lessons/07-kubernetes-tf-serving.md) | 10.7 Deploying TensorFlow models to Kubernetes | 1,129 | [video](https://www.youtube.com/watch?v=6vHLMdnjO2w&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [08-eks.md](lessons/08-eks.md) | 10.8 Deploying to EKS | 1,120 | [video](https://www.youtube.com/watch?v=89jxeddZtC0&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [09-summary.md](lessons/09-summary.md) | 10.9 Summary | 860 | [video](https://www.youtube.com/watch?v=J5LMRTIu4jY&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [10-explore-more.md](lessons/10-explore-more.md) | 10.10 Explore more | 115 | — |

~9,690 words ≈ 40 min of reading. Alexey's lecture notebook, `code/` and the workshop are in [notebooks/](notebooks/).

## What is where

```
cohort2026/
├── START_HERE.md                          ← this file
├── lessons/                               ← 10 written lessons + images/
├── notebooks/
│   ├── 10-kubernetes-lecture.ipynb        ← tf-serving-connect.ipynb (needs TF Serving running)
│   ├── code/                              ← lecture files: gateway.py, proto.py, Dockerfiles, compose, ping/, kube-config/
│   └── workshop/                          ← 2025 workshop: README, service/ (FastAPI + ONNX model), k8s/, load_test.py
├── practice/
│   ├── 10-kubernetes_practice.ipynb       ← your practice notebook (manifests loaded)
│   ├── 10-kubernetes_commented.ipynb      ← commented walkthrough, lecture + workshop section
│   └── commented/                         ← GOAL/WHY commented copies of the lecture and workshop files
└── homework/
    ├── Homework10_2026.ipynb              ← checklist scaffold: commands per question, no answers
    ├── homework10_2026.md                 ← the official question text (repo paths!)
    ├── deployment.yaml, service.yaml, hpa.yaml   ← the manifests you apply
    └── 05-deployment/                     ← the frozen HW5 release: Dockerfile, predict.py, pipeline.bin, q6_test.py, ...
```

## Connections

- [Home](../../../00_Reference_Materials/Home.md) · [Resource Map](../../../00_Reference_Materials/Resource_Map_Cohort2026.md)
- [Playbook](../../../00_Reference_Materials/ML_Strategist_Playbook.md): *Shipping the model* (readiness probe = `/health`)

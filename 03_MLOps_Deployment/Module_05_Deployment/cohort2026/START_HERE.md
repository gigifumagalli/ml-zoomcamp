# Module 5 — Deployment, session plan

Everything is in this folder. Nothing to download. (Installs needed: `uv` on the Mac, Docker Desktop, and `flask gunicorn fastapi uvicorn requests` in the `ml-zoomcamp` env for the commented notebook.)

**Homework 5:** platform deadline **Mon 26 Oct** (repo says Oct 19; the platform runs a week later). Target: **submit Mon 19 Oct**, as in the tracker. The platform week is cushion, not schedule.
**Submit at:** https://courses.datatalks.club/ml-zoomcamp-2026/homework/hw05

---

## Sessions

The course README says: lessons 5.1 – 5.6 for the theory, then the **workshop** (uv + FastAPI, [notebooks/workshop/README.md](notebooks/workshop/README.md), [video](https://www.youtube.com/watch?v=jzGzw98Eikk)) for the practical part. The homework follows the workshop. The sessions mix both.

Re-plan (Tue 13 Oct): Module 4 is finished on Wed 14 Oct, so Module 5 runs **Thu 15 – Mon 19 Oct inclusive**, on the Thu and Sun trains plus three morning slots.

**Session 1 — Thu 15 Oct, 08:00.** Read [5.1](lessons/01-intro.md) → [5.4](lessons/04-flask-deployment.md) (~3,750 words, ~16 min). In `practice/05-deployment_commented.ipynb`: retrain, `pickle` save/load, `commented/train.py`, the ping service, then the Flask churn service under gunicorn and `predict-test.py`. Then HW5 **Q1**: install uv (`brew install uv`) and check `uv --version`. Also run `uv sync --locked` once in `homework/` while you still have home Wi-Fi: it downloads the packages the train rides will need.

**Session 2 — Thu 15 Oct, train Zug → Milano (16:00–18:50).** Read [5.5](lessons/05-pipenv.md) (~1,090 words) + workshop "Scikit-Learn Pipelines", "Pydantic and Validation", "Environment management". pipenv vs uv; in `notebooks/workshop/` run `uv run uvicorn ...`. Then HW5 setup (smoke test, checksum), **Q2, Q3**.

**Session 3 — Fri 16 Oct, 08:00 (Turin).** Read [5.6](lessons/06-docker.md) (~1,090 words) + workshop "Docker". Build and run the churn container from `notebooks/workshop/`. Then HW5 **Q5**. Docker Desktop must be installed and running by now.

**Session 4 — Sun 18 Oct, train Turin → Zug (from 15:50).** HW5 **Q4** (serve with uvicorn) and **Q6** (build and run the homework container). Docker Desktop on the laptop is enough once the homework image has been built: do the first `docker build` in `homework/` on Fri 16 while you have Wi-Fi (it pulls the pinned base image, which differs from the workshop's).

**Session 5 — Mon 19 Oct, 08:00.** Check, **submit** (target; the platform closes Mon 26 Oct), then the Playbook cards: pickle artifact + version pinning, Flask vs FastAPI (validation), uv lock workflow, Docker image / container / port mapping.

> Docker Desktop must be installed **and running** before Fri 16 Oct; best before the Thu train. It was planned for Oct 7; check with the last code cell of the commented notebook or `docker version`.
> [5.7](lessons/07-aws-eb.md) (AWS Elastic Beanstalk) is optional: skim it. No AWS account until Nov 10. The workshop's Fly.io deploy is optional too.
> On scikit-learn 1.9, `DictVectorizer()` + `LogisticRegression(solver='liblinear')` crashes at `fit` ("Only sparse matrices with 32-bit integer indices are accepted"). Use `DictVectorizer(sparse=False)`. The commented material does; the workshop's original code doesn't.
> The midterm service (FastAPI + Docker) follows this pattern: use the workshop as a template only.
> If the week collapses: homework isn't required for the certificate. Skip it rather than let it push Module 6 (starts Tue 20 Oct).

---

## Six traps in this homework

**1. The lessons teach a different stack from the homework.** 5.3 – 5.6 (2021) use Flask + gunicorn + pipenv and pickle a `(dv, model)` tuple. HW5 uses **FastAPI + uvicorn + uv** and one sklearn `Pipeline` in `pipeline.bin`: `uv sync --locked`, then `uv run uvicorn predict:app --host 0.0.0.0 --port 9696`, and the response key is `conversion_probability`, not `churn_probability`. The commented notebook opens with a lecture / workshop / homework comparison table.

**2. Run it in the locked environment, not in conda.** Your `ml-zoomcamp` env has a newer scikit-learn: `pipeline.bin` loads with an `InconsistentVersionWarning`, and Q2 asks for the version in `pyproject.toml` / `uv.lock`, not yours. Run `uv sync --locked` once in `homework/`, then `uv run python q3.py` or `uv run --with jupyter jupyter lab` (this adds Jupyter without touching `uv.lock`).

**3. `smoke_test.py` scores the Q4 lead, not the Q3 one.** Q3 needs your own script with the Q3 lead. Q3, Q4 and Q6 are free numeric answers (3 decimals, ±0.005), with no option list to check against.

**4. Don't retrain, don't re-lock.** `train.py` overwrites `pipeline.bin`, `feature_defaults.json` and `model_metadata.json` in place, and a retrain gives a different checksum even with the same data and versions (checked). Its default data path (`../../data/`) doesn't exist in this folder anyway. `uv lock` / `uv add` rewrite `uv.lock`, and you'd be grading a different environment.

**5. Q6: stop the Q4 server first.** Only one process can hold port 9696. If uvicorn is still running, `docker run -p 9696:9696` fails with "port is already allocated", and `q6_test.py` answers from the **local** server: you'd report Q4 again without testing the container. `docker ps` proves what's listening. Docker Desktop must be running ("Cannot connect to the Docker daemon" otherwise).

**6. `.python-version` is hidden but required.** The Dockerfile copies it (the build stops with `".python-version": not found` without it) and uv reads it to pick Python 3.11.15. Finder doesn't show dotfiles: check with `ls -a`. Also on macOS `sha256sum` may not exist: use `shasum -a 256 pipeline.bin`.

---

## Lessons in this folder

| File | Title | Words | Video |
|---|---|---:|---|
| [01-intro.md](lessons/01-intro.md) | 5.1 Intro / Session overview | 766 | [video](https://www.youtube.com/watch?v=agIFak9A3m8&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [02-pickle.md](lessons/02-pickle.md) | 5.2 Saving and loading the model | 754 | [video](https://www.youtube.com/watch?v=EJpqZ7OlwFU&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [03-flask-intro.md](lessons/03-flask-intro.md) | 5.3 Web services: introduction to Flask | 924 | [video](https://www.youtube.com/watch?v=W7ubna1Rfv8&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [04-flask-deployment.md](lessons/04-flask-deployment.md) | 5.4 Serving the churn model with Flask | 1,311 | [video](https://www.youtube.com/watch?v=Q7ZWPgPnRz8&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [05-pipenv.md](lessons/05-pipenv.md) | 5.5 Python virtual environment: Pipenv | 1,085 | [video](https://www.youtube.com/watch?v=BMXh8JGROHM&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [06-docker.md](lessons/06-docker.md) | 5.6 Environment management: Docker | 1,094 | [video](https://www.youtube.com/watch?v=wAtyYZ6zvAs&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [07-aws-eb.md](lessons/07-aws-eb.md) | 5.7 Deployment to the cloud: AWS Elastic Beanstalk (optional) | 1,132 | [video](https://www.youtube.com/watch?v=HGPJ4ekhcLg&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [08-summary.md](lessons/08-summary.md) | 5.8 Summary | 439 | [video](https://www.youtube.com/watch?v=sSAqYSk7Br4&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [09-explore-more.md](lessons/09-explore-more.md) | 5.9 Explore more | 103 | — |

~7,610 words ≈ 32 min of reading. Plus the workshop write-up, [notebooks/workshop/README.md](notebooks/workshop/README.md) (1,986 words ≈ 8 min, [video](https://www.youtube.com/watch?v=jzGzw98Eikk)). Alexey's lecture notebook and scripts are in [notebooks/](notebooks/).

## What is where

```
cohort2026/
├── START_HERE.md                         ← this file
├── lessons/                              ← 9 written lessons + images/
├── notebooks/
│   ├── 05-deployment-lecture.ipynb       ← Alexey's lecture notebook (untouched) + data-week-3.csv
│   ├── code/                             ← lecture scripts: train.py, predict.py (Flask), Pipfile, Dockerfile
│   └── workshop/                         ← uv + FastAPI workshop: README, train.py, predict.py, pyproject.toml, uv.lock, Dockerfile
├── practice/
│   ├── 05-deployment_practice.ipynb      ← your starter: rebuild the service the HW5 way
│   ├── 05-deployment_commented.ipynb     ← commented walkthrough; starts and queries each service
│   ├── commented/                        ← commented copies of the lecture files + commented/workshop/
│   └── data-week-3.csv                   ← Telco churn (same file as Modules 3–4)
└── homework/
    ├── Homework5_2026.ipynb              ← scaffold: setup, Q1–Q6 checklist, no answers
    ├── homework5_2026.md                 ← the official question text
    ├── pipeline.bin, model_metadata.json, feature_defaults.json   ← the frozen artifact + its checksums
    ├── predict.py, model.py, smoke_test.py, q6_test.py, train.py  ← the provided service and scripts
    ├── pyproject.toml, uv.lock, .python-version, Dockerfile        ← the locked environment and image
    └── course_lead_scoring_2026.csv      ← the training data (reference only: don't retrain)
```

## Connections

- [Home](../../../00_Reference_Materials/Home.md) · [Resource Map](../../../00_Reference_Materials/Resource_Map_Cohort2026.md)
- [Playbook](../../../00_Reference_Materials/ML_Strategist_Playbook.md): *Where does preprocessing live?*, *Shipping the model*
- Used by: [Midterm: hospital readmission](../../../00_Reference_Materials/projects/Midterm_Readmission.md)
- Used by: [Capstone 1: turbofan RUL](../../../00_Reference_Materials/projects/Capstone1_CMAPSS.md)

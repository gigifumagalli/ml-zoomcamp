# Module 1 — Wednesday 16 September, session plan

Everything you need tomorrow is in this folder. Nothing else to download.

**Deadline:** Homework 1 is due **Monday 21 September, 23:00 UTC**.
**Submit at:** https://courses.datatalks.club/ml-zoomcamp-2026/homework/hw01

---

## Slot 1 — 08:00–09:00

1. **Enrol** in the 2026 cohort at https://courses.datatalks.club/ml-zoomcamp-2026 and join the DataTalks.Club Slack channel `#course-ml-zoomcamp`. (~10 min)
2. **Read** [01-what-is-ml](lessons/01-what-is-ml.md) → [02-ml-vs-rules](lessons/02-ml-vs-rules.md) → [03-supervised-ml](lessons/03-supervised-ml.md) → [04-crisp-dm](lessons/04-crisp-dm.md) → [05-model-selection](lessons/05-model-selection.md) → [06-environment](lessons/06-environment.md). About 7,700 words — you have seen all of this before, so skim for vocabulary rather than studying it. The one worth watching instead of reading is [06-environment](lessons/06-environment.md) if anything in your setup feels stale.
3. **Check the environment still works** — open [Homework1_2026.ipynb](Homework1_2026.ipynb), run the setup cell. It prints the pandas version, which is literally Q1.

## Slot 2 — 20:00–21:00

4. **Read** [07-numpy](lessons/07-numpy.md), [08-linear-algebra](lessons/08-linear-algebra.md), [09-pandas](lessons/09-pandas.md) — then [10-summary](lessons/10-summary.md) if there is time. Notebooks for these three are in [notebooks/](notebooks/) if you want to run along.
5. **Do the homework** in [Homework1_2026.ipynb](Homework1_2026.ipynb), then submit.

> If slot 2 finishes early — and it probably will — start Module 2. Its lessons and the 2026 HW2 are already waiting in [../../Module_02_Regression/cohort2026/](../../Module_02_Regression/cohort2026/). Submitting HW2 by Friday puts you a full week ahead.

---

## ⚠️ Do not reuse your spring answers

The 2026 cohort uses a **different pinned dataset**: `car_fuel_efficiency_2026.csv` (621 KB), not the `car_fuel_efficiency.csv` in your Module_02 folder from April. Same column names, different values, different answers. Your old notebooks are useful as reference for *how* you did something, never for *what* the answer was.

---

## Lessons in this folder

| File | Title | Words | Video |
|---|---|---:|---|
| [01-what-is-ml.md](lessons/01-what-is-ml.md) | Introduction to Machine Learning | 989 | [video](https://www.youtube.com/watch?v=Crm_5n4mvmg&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR&index=2) |
| [02-ml-vs-rules.md](lessons/02-ml-vs-rules.md) | ML vs Rule-Based Systems | 1,379 | [video](https://www.youtube.com/watch?v=CeukwyUdaz8&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR&index=3) |
| [03-supervised-ml.md](lessons/03-supervised-ml.md) | Supervised Machine Learning | 1,543 | [video](https://www.youtube.com/watch?v=j9kcEuGcC2Y&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR&index=4) |
| [04-crisp-dm.md](lessons/04-crisp-dm.md) | CRISP-DM | 1,692 | [video](https://www.youtube.com/watch?v=dCa3JvmJbr0&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR&index=5) |
| [05-model-selection.md](lessons/05-model-selection.md) | Model Selection Process | 1,424 | [video](https://www.youtube.com/watch?v=OH_R0Sl9neM&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR&index=6) |
| [06-environment.md](lessons/06-environment.md) | Setting up the Environment | 1,186 | [video](https://www.youtube.com/watch?v=pqQFlV3f9Bo&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [07-numpy.md](lessons/07-numpy.md) | Introduction to NumPy | 2,361 | [video](https://www.youtube.com/watch?v=Qa0-jYtRdbY&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR&index=7) |
| [08-linear-algebra.md](lessons/08-linear-algebra.md) | Linear Algebra Refresher | 2,130 | [video](https://www.youtube.com/watch?v=zZyKUeOR4Gg&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR&index=8) |
| [09-pandas.md](lessons/09-pandas.md) | Introduction to Pandas | 2,958 | [video](https://www.youtube.com/watch?v=0j3XK5PsnxA&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR&index=9) |
| [10-summary.md](lessons/10-summary.md) | Summary | 1,455 | [video](https://www.youtube.com/watch?v=VRrEEVeJ440&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR&index=10) |

Total: ~17,100 words ≈ 60–70 min of reading, versus ~3 h of video.

## What is where

```
cohort2026/
├── START_HERE.md                    ← this file
├── Homework1_2026.ipynb             ← scaffold: questions + empty cells, no answers
├── homework1_2026.md                ← the official question text
├── car_fuel_efficiency_2026.csv     ← the 2026 pinned dataset
├── lessons/                         ← the 10 written lessons
└── notebooks/                       ← Alexey's numpy / linalg / pandas notebooks
```

Full upstream repo (all modules, all cohorts): `00_Reference_Materials/mlzoomcamp-2026/` — `git pull` there to pick up homework for later modules as it is released.

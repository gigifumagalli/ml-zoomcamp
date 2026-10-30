# Module 6 — Decision Trees and Ensemble Learning, session plan

Everything is in this folder. Nothing to download. XGBoost must be installed in your environment once (`pip install xgboost`, or `conda install -c conda-forge xgboost`).

**Homework 6:** platform deadline **Mon 2 Nov**. Target: **submit Mon 26 Oct**, as in the tracker, so the midterm starts on time on Tue 27 Oct.
**Submit at:** https://courses.datatalks.club/ml-zoomcamp-2026/homework/hw06

---

## Sessions

**Session 1 — Tue 20 Oct, 08:00.** Read [6.1](lessons/01-credit-risk.md) → [6.3](lessons/03-decision-trees.md) (~2,510 words, ~10 min). In `practice/`: decode the credit data, `99999999` → NaN, split, first `DecisionTreeClassifier`. See the overfit (train AUC 1.0, validation ~0.65), then `max_depth=2` and `export_text`.

**Session 2 — Wed 21 Oct, 08:00.** Read [6.4](lessons/04-decision-tree-learning.md) → [6.5](lessons/05-decision-tree-tuning.md) (~2,680 words, ~11 min). Split finding by hand on the 8-client toy data (misclassification rate per threshold), then the `max_depth` × `min_samples_leaf` grid and its heatmap.

**Session 3 — Wed 21 Oct, 20:00 (long hour).** Read [6.6](lessons/06-random-forest.md) (~1,410 words). Random forest: AUC vs `n_estimators`, then tune `max_depth` and `min_samples_leaf`.

**Session 4 — Thu 22 Oct, 08:00.** Read [6.7](lessons/07-boosting.md) (~1,540 words). XGBoost: `DMatrix`, the first model, the watchlist, parsing the monitoring output, then the same curve from `evals_result`.

**Session 5 — Fri 23 Oct, 08:00.** Read [6.8](lessons/08-xgb-tuning.md) → [6.11](lessons/11-explore-more.md) (~2,510 words). Tune `eta`, `max_depth`, `min_child_weight`; compare the three tuned models; final model on train + val, test once. Then HW6 **start**: the `zc-hw06` kernel (trap 2), data prep, **Q1, Q2**.

**Session 6 — Mon 26 Oct, 08:00.** HW6 **Q3 – Q6**, check, **submit** (target; the platform closes Mon 2 Nov). If time is left, the Playbook cards: decision tree, random forest, gradient boosting / XGBoost, feature importance.

> Sat 24 Oct 09–11 is the midterm prep weekend block (repo, load the data, first EDA), not Module 6. The midterm starts Tue 27 Oct: if HW6 isn't done by Mon 26, skip it (homework isn't required for the certificate); the lessons are needed for the midterm's model selection.
> The lecture is classification (credit default, AUC); HW6 is **regression** (MPG, RMSE) on the HW1/HW2 car data. Same tree families, the `...Regressor` versions.

---

## Five traps in this homework

**1. The lecture notebook breaks on XGBoost 3.** In 6.9, `feature_names=dv.get_feature_names_out()` (a NumPy array) raises *"Expecting a sequence of strings for feature names"*; the next cells fail and the last one scores a stale model (AUC ~0.51). Its 6.8 comparison plots also show one curve, or none, because only the last run of each comparison was kept. `practice/06-trees_commented.ipynb` fixes both (`list(...)`, a loop over every value). `notebooks/` is left exactly as Alexey wrote it.

**2. scikit-learn 1.9 changes the random-forest numbers.** The options were computed with scikit-learn 1.7.2 (1.8.0 gives the same numbers; 1.9.1 does not). On 1.9, Q2 lands next to an option instead of on it, and the 3-decimal ranking in Q3 changes. Make a separate kernel for this homework, leave `ml-zoomcamp` alone:
`conda create -n zc-hw06 -c conda-forge python=3.11 scikit-learn=1.7.2 pandas xgboost ipykernel`, then pick `zc-hw06` as the notebook's kernel. The setup cell prints a warning on 1.9+.

**3. Clean before you vectorise.** `horsepower` and `acceleration` have gaps: `fillna(0)` first, or `RandomForestRegressor` stops with *"Input X contains NaN"*. Drop `fuel_efficiency_mpg` before `to_dict`, or Q1's depth-1 tree splits on the target itself. Q1 wants the **original** column: `origin=USA` → `origin`.

**4. RMSE, then round.** `mean_squared_error(..., squared=False)` is gone since scikit-learn 1.6 (`TypeError`): use `root_mean_squared_error`. Q3 says compare at **3 decimals**: round first, then pick.

**5. Q5 and Q6 read narrowly.** Q5: rank only the four listed features; a feature outside the list or a one-hot column may rank higher. Q6: `feature_names` must be a `list`; with `reg:squarederror` the watchlist reports `val-rmse` by default; compare the trained models' RMSE (last round), and use `evals_result={}` rather than parsing printed text.

---

## Lessons in this folder

| File | Title | Words | Video |
|---|---|---:|---|
| [01-credit-risk.md](lessons/01-credit-risk.md) | 6.1 Credit risk scoring project | 685 | [video](https://www.youtube.com/watch?v=GJGmlfZoCoU&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [02-data-prep.md](lessons/02-data-prep.md) | 6.2 Data cleaning and preparation | 925 | [video](https://www.youtube.com/watch?v=tfuQdI3YO2c&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [03-decision-trees.md](lessons/03-decision-trees.md) | 6.3 Decision trees | 901 | [video](https://www.youtube.com/watch?v=YGiQvFbSIg8&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [04-decision-tree-learning.md](lessons/04-decision-tree-learning.md) | 6.4 Decision tree learning algorithm | 1,512 | [video](https://www.youtube.com/watch?v=XODz6LwKY7g&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [05-decision-tree-tuning.md](lessons/05-decision-tree-tuning.md) | 6.5 Decision trees parameter tuning | 1,164 | [video](https://www.youtube.com/watch?v=XJaxwH50Qok&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [06-random-forest.md](lessons/06-random-forest.md) | 6.6 Ensemble learning and random forest | 1,405 | [video](https://www.youtube.com/watch?v=FZhcmOfNNZE&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [07-boosting.md](lessons/07-boosting.md) | 6.7 Gradient boosting and XGBoost | 1,541 | [video](https://www.youtube.com/watch?v=xFarGClszEM&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [08-xgb-tuning.md](lessons/08-xgb-tuning.md) | 6.8 XGBoost parameter tuning | 1,180 | [video](https://www.youtube.com/watch?v=VX6ftRzYROM&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [09-final-model.md](lessons/09-final-model.md) | 6.9 Selecting the best model | 606 | [video](https://www.youtube.com/watch?v=lqdnyIVQq-M&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [10-summary.md](lessons/10-summary.md) | 6.10 Summary | 486 | [video](https://www.youtube.com/watch?v=JZ6sRZ_5j_c&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [11-explore-more.md](lessons/11-explore-more.md) | 6.11 Explore more | 236 | — |

~10,640 words ≈ 44 min of reading. Alexey's lecture notebook is in [notebooks/](notebooks/).

## What is where

```
cohort2026/
├── START_HERE.md                         ← this file
├── lessons/                              ← 11 written lessons + images/
├── notebooks/                            ← Alexey's lecture notebook (06-trees-lecture.ipynb) + CreditScoring.csv
├── practice/                             ← your practice notebook, the commented walkthrough + CreditScoring.csv
└── homework/
    ├── Homework6_2026.ipynb              ← scaffold: data prep, Q1–Q6, no answers
    ├── homework6_2026.md                 ← the official question text
    └── car_fuel_efficiency_2026.csv      ← the 2026 pinned dataset (10,000 cars, same file as HW1/HW2)
```

## Connections

- [Home](../../../00_Reference_Materials/Home.md) · [Resource Map](../../../00_Reference_Materials/Resource_Map_Cohort2026.md)
- [Playbook](../../../00_Reference_Materials/ML_Strategist_Playbook.md): `DecisionTreeRegressor`, `RandomForestRegressor` (XGBoost card still to write)
- Used by: [Midterm: hospital readmission](../../../00_Reference_Materials/projects/Midterm_Readmission.md)
- Used by: [Capstone 1: turbofan RUL](../../../00_Reference_Materials/projects/Capstone1_CMAPSS.md)

# Module 2 — Regression, session plan

Everything is in this folder. Nothing to download.

**Deadline:** Homework 2 is due **Monday 28 September, 23:00 UTC**.
**Submit at:** https://courses.datatalks.club/ml-zoomcamp-2026/homework/hw02

---

## The four sessions

**Session 1 — Fri 18 Sep, 08:00.** Read [01-car-price-intro](lessons/01-car-price-intro.md) → [06-linear-regression-vector](lessons/06-linear-regression-vector.md). The problem framing, data prep, EDA, the train/val/test split, and linear regression in scalar then vector form. You know this material — skim, but slow down on 04 (the validation framework), because HW2 Q5 is entirely about how much the split seed moves your score.

**Session 2 — Mon 21 Sep, 08:00.** Read [07-linear-regression-training](lessons/07-linear-regression-training.md) → [11-feature-engineering](lessons/11-feature-engineering.md). Lesson 07 is the one that matters: `train_linear_regression` via the normal equation. **Type it out yourself** into the homework notebook — the homework is graded against that implementation, not against sklearn.

**Session 3 — Tue 22 Sep, 08:00.** Read [12-categorical-variables](lessons/12-categorical-variables.md) → [16-summary](lessons/16-summary.md), then do HW2 **Q1 and Q2** (missing-value column, median horsepower). Lesson 13 gives you `train_linear_regression_reg`, which Q4 needs.

**Session 4 — Wed 23 Sep, 08:00.** HW2 **Q3 → Q6**, then submit. (That evening's 20:00 slot is already booked for Module 3 videos — you're running ahead by then.)

> Finish early and Module 3 is next — its folder isn't built yet, tell me and I'll prepare it. Submitting HW2 before Friday 25th puts you a full week ahead of the cohort.

---

## ⚠️ Two traps in this homework

**1. sklearn is not the lecture's code.** Q3 and Q4 say "using the code from the lessons". `sklearn.linear_model.LinearRegression` fits an intercept differently and `Ridge(alpha=r)` is *not* the same as the lecture's `train_linear_regression_reg(X, y, r)` — it scales the penalty differently and regularises the bias term differently. This cost you points on this exact question in the spring. Use the lesson functions.

**2. Different dataset from spring.** `car_fuel_efficiency_2026.csv` in this folder, not the `car_fuel_efficiency.csv` one level up. Same columns, different numbers, different answers.

Also worth noting: the 2026 homework pins rounding deliberately — 3 decimals in Q3, **4 decimals in Q4** — precisely so the options don't collapse into a tie. Don't round early.

---

## Lessons in this folder

| File | Title | Words | Video |
|---|---|---:|---|
| [01-car-price-intro.md](lessons/01-car-price-intro.md) | Car price prediction project | 610 | [video]("https://www.youtube.com/watch?v=vM3SqPNlStE&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR&index=12") |
| [02-data-preparation.md](lessons/02-data-preparation.md) | Data preparation | 801 | [video]("https://www.youtube.com/watch?v=Kd74oR4QWGM&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR&index=13") |
| [03-eda.md](lessons/03-eda.md) | Exploratory data analysis | 1,545 | [video]("https://www.youtube.com/watch?v=k6k8sQ0GhPM&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR&index=14") |
| [04-validation-framework.md](lessons/04-validation-framework.md) | Setting up the validation framework | 1,246 | [video]("https://www.youtube.com/watch?v=ck0IfiPaQi0&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR&index=15") |
| [05-linear-regression-simple.md](lessons/05-linear-regression-simple.md) | Linear regression | 1,233 | [video]("https://www.youtube.com/watch?v=Dn1eTQLsOdA&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR&index=16") |
| [06-linear-regression-vector.md](lessons/06-linear-regression-vector.md) | Linear regression: vector form | 1,085 | [video]("https://www.youtube.com/watch?v=YkyevnYyAww&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR&index=17") |
| [07-linear-regression-training.md](lessons/07-linear-regression-training.md) | Training linear regression: Normal equation | 1,015 | [video]("https://www.youtube.com/watch?v=hx6nak-Y11g&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR&index=18") |
| [08-baseline-model.md](lessons/08-baseline-model.md) | Baseline model for car price prediction project | 851 | [video]("https://www.youtube.com/watch?v=SvPpMMYtYbU&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR&index=19") |
| [09-rmse.md](lessons/09-rmse.md) | Root Mean Squared Error (RMSE) | 686 | [video]("https://www.youtube.com/watch?v=0LWoFtbzNUM&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR&index=20") |
| [10-car-price-validation.md](lessons/10-car-price-validation.md) | Computing RMSE on validation data | 666 | [video](https://www.youtube.com/watch?v=rawGPXg2ofE&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR&index=21) |
| [11-feature-engineering.md](lessons/11-feature-engineering.md) | Feature engineering | 770 | [video](https://www.youtube.com/watch?v=-aEShw4ftB0&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR&index=22) |
| [12-categorical-variables.md](lessons/12-categorical-variables.md) | Categorical variables | 1,117 | [video](https://www.youtube.com/watch?v=sGLAToAAMa4&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR&index=23) |
| [13-regularization.md](lessons/13-regularization.md) | Regularization | 1,271 | [video](https://www.youtube.com/watch?v=91ve3EJlHBc&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR&index=24) |
| [14-tuning-model.md](lessons/14-tuning-model.md) | Tuning the model | 421 | [video](https://www.youtube.com/watch?v=lW-YVxPgzQw&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR&index=25) |
| [15-using-model.md](lessons/15-using-model.md) | Using the model | 946 | [video](https://www.youtube.com/watch?v=KT--uIJozes&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR&index=26) |
| [16-summary.md](lessons/16-summary.md) | Car price prediction project summary | 1,060 | [video](https://www.youtube.com/watch?v=_qI01YXbyro&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR&index=27) |
| [17-explore-more.md](lessons/17-explore-more.md) | Explore more | 129 | — |

~15,700 words ≈ 60 min of reading, versus ~3 h of video. Alexey's own lecture notebook: [notebooks/02-regression-lecture.ipynb](notebooks/02-regression-lecture.ipynb).

## What is where

```
cohort2026/
├── START_HERE.md                    ← this file
├── Homework2_2026.ipynb             ← scaffold: Q1–Q6, function stubs, no answers
├── homework2_2026.md                ← the official question text
├── car_fuel_efficiency_2026.csv     ← the 2026 pinned dataset
├── lessons/                         ← 17 written lessons + images/
└── notebooks/                       ← Alexey's lecture notebook
```

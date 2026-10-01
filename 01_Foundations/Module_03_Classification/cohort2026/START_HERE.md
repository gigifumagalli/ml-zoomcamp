# Module 3 — Classification, session plan

Everything is in this folder. Nothing to download.

**Homework 3:** platform deadline **Mon 12 Oct**, but you're at Realize Club 11–13 Oct, so **submit by Fri 9 Oct**.
**Submit at:** https://courses.datatalks.club/ml-zoomcamp-2026/homework/hw03

---

## Sessions

You're about two sessions behind the tracker (the Sep 29 – Oct 1 Module 3 slots went to finishing HW2), so this compresses the module into three slots.

**Session 1 — Fri 2 Oct, 08:00.** Read [3.1](lessons/01-churn-project.md) → [3.7](lessons/07-correlation.md) (~5,300 words, ~20 min). Data prep (the `TotalCharges` object-dtype trap), the split, EDA, then three ways to rank features: risk ratio, mutual information, correlation. Try them in `practice/` on the Telco data.

**Session 2 — Mon 5 Oct, 08:00.** Read [3.8](lessons/08-ohe.md) → [3.13](lessons/13-summary.md) (~4,200 words). One-hot encoding with `DictVectorizer`, logistic regression, interpreting coefficients. Then HW3 **data prep, Q1, Q2**.

**Session 3 — Wed 7 Oct, 20:00 (catch-up hour).** HW3 **Q3 → Q6**, then submit.

> Module 4 starts Tue 6 Oct on the tracker, so this overlaps. If the week collapses, remember homework isn't required for the certificate: skip rather than let it eat into Module 4 before your trip.

---

## Five traps in this homework

**1. This time sklearn *is* the required code.** The opposite of HW2: the homework pins `train_test_split(..., random_state=42)` and `LogisticRegression(solver='liblinear', C=1.0, max_iter=1000, random_state=42)`. Use them exactly, or your accuracy won't match the options.

**2. Fit `DictVectorizer` on train only.** `fit_transform` on train, `transform` on validation. Fitting on validation leaks its categories and can also give a different column layout from the one the model was trained on.

**3. Remove `converted` before building features.** If it's left in, validation accuracy comes out at ~1.0, which is the giveaway.

**4. Smaller `C` = stronger regularisation.** sklearn's `C` is the *inverse* of HW2's `r`. Q6's tiny values (10⁻⁶ to 10⁻³) are very heavy regularisation.

**5. Different dataset from spring.** The lecture uses Telco churn; the homework uses `course_lead_scoring_2026.csv`. Nothing in `../solo_spring2026/` carries over to the answers.

---

## Lessons in this folder

| File | Title | Words | Video |
|---|---|---:|---|
| [01-churn-project.md](lessons/01-churn-project.md) | 3.1 Churn prediction project | 709 | [video](https://www.youtube.com/watch?v=0Zw04wdeTQo&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [02-data-preparation.md](lessons/02-data-preparation.md) | 3.2 Data preparation | 951 | [video](https://www.youtube.com/watch?v=VSGGU9gYvdg&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [03-validation.md](lessons/03-validation.md) | 3.3 Setting up the validation framework | 515 | [video](https://www.youtube.com/watch?v=_lwz34sOnSE&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [04-eda.md](lessons/04-eda.md) | 3.4 EDA | 601 | [video](https://www.youtube.com/watch?v=BNF1wjBwTQA&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [05-risk.md](lessons/05-risk.md) | 3.5 Feature importance: churn rate and risk ratio | 1,065 | [video](https://www.youtube.com/watch?v=fzdzPLlvs40&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [06-mutual-info.md](lessons/06-mutual-info.md) | 3.6 Feature importance: mutual information | 591 | [video](https://www.youtube.com/watch?v=_u2YaGT6RN0&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [07-correlation.md](lessons/07-correlation.md) | 3.7 Feature importance: correlation | 861 | [video](https://www.youtube.com/watch?v=mz1707QVxiY&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [08-ohe.md](lessons/08-ohe.md) | 3.8 One-hot encoding | 904 | — |
| [09-logistic-regression.md](lessons/09-logistic-regression.md) | 3.9 Logistic regression | 837 | — |
| [10-training-log-reg.md](lessons/10-training-log-reg.md) | 3.10 Training logistic regression with Scikit-Learn | 670 | — |
| [11-log-reg-interpretation.md](lessons/11-log-reg-interpretation.md) | 3.11 Model interpretation | 826 | — |
| [12-using-log-reg.md](lessons/12-using-log-reg.md) | 3.12 Using the model | 596 | — |
| [13-summary.md](lessons/13-summary.md) | 3.13 Summary | 396 | — |
| [14-explore-more.md](lessons/14-explore-more.md) | 3.14 Explore more | 138 | — |

~9,660 words ≈ 40 min of reading. Alexey's lecture notebooks are in [notebooks/](notebooks/).

## What is where

```
cohort2026/
├── START_HERE.md                         ← this file
├── lessons/                              ← 14 written lessons + images/
├── notebooks/                            ← Alexey's two lecture notebooks + data-week-3.csv (Telco)
├── practice/                             ← your lecture practice notebook + data-week-3.csv
└── homework/
    ├── Homework3_2026.ipynb              ← scaffold: data prep, Q1–Q6, no answers
    ├── homework3_2026.md                 ← the official question text
    └── course_lead_scoring_2026.csv      ← the 2026 pinned dataset (5,000 leads)
```

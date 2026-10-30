# Module 4 — Evaluation, session plan

Everything is in this folder. Nothing to download.

**Homework 4:** platform deadline **Mon 19 Oct**, but the plan (re-planned Tue 13 Oct) is to finish Module 4 **including HW4 by the end of Wed 14 Oct**. Module 5 then runs Thu 15 – Mon 19 Oct.
**Submit at:** https://courses.datatalks.club/ml-zoomcamp-2026/homework/hw04

---

## Sessions

Re-plan: Module 4 is done by the end of Wed 14 Oct, homework included. Everything here is local (data included), so airport or train Wi-Fi doesn't matter.

**Session 1 — Tue 13 Oct (travel back from Realize Club: airport, train, evening). No tracker slot.** Read [4.1](lessons/01-overview.md) → [4.7](lessons/07-cross-validation.md) (~5,980 words, ~25 min) and run `practice/04-evaluation_commented.ipynb` top to bottom: accuracy vs the dummy model, confusion table, precision/recall, ROC, AUC, K-fold CV. This is the extra hour that makes Wednesday work.

**Session 2 — Wed 14 Oct, 08:00.** HW4 **data prep, Q1 → Q3**: AUC of each numerical feature, validation AUC of the model, where precision and recall cross.

**Session 3 — Wed 14 Oct, 20:00 (long hour).** **Q4 → Q6**: F1 maximum, 5-fold CV std, tuning `C` with CV. Check, **submit** (platform closes Mon 19 Oct).

> If Session 1 doesn't happen: read the lessons at the start of Wed 08:00 and decide at 20:00 whether HW4 stays. Module 5 starts Thu 15 Oct 08:00 either way.
> Docker Desktop: install it any time Wed or Thu morning (it needs no study slot). Module 5 uses it from Fri 16 Oct.
> Playbook cards (confusion table, precision/recall, ROC AUC, K-fold CV): on the Mon 26 Oct session, together with Module 6's.
> If it doesn't work out: skip HW4 (homework isn't required for the certificate), but read the lessons. AUC and cross-validation are what the midterm is judged on.

---

## Five traps in this homework

**1. The lecture notebook crashes on pandas 3.** `df.dtypes == 'object'` selects no columns, so nothing is lower-cased, `churn == 'yes'` never matches, and `LogisticRegression` stops with *"only one class"*. Use `select_dtypes(include=['object', 'string'])`, as `practice/04-evaluation_commented.ipynb` does. `notebooks/` is left exactly as Alexey wrote it.

**2. Same dataset as HW3, different settings.** The split is `random_state=1` (HW3: 42), and the model is `LogisticRegression(solver='liblinear', C=1.0, max_iter=1000)` with no `random_state`. HW3 numbers don't carry over. And use `DictVectorizer(sparse=False)`: on scikit-learn 1.9 the default sparse matrix makes `liblinear` crash at `fit` (*"Only sparse matrices with 32-bit integer indices"*).

**3. AUC wants scores, not decisions.** `roc_auc_score(y_true, score)`: in Q1 the score is the raw column (negate it if AUC < 0.5); in Q2 it's `predict_proba(X)[:, 1]`. Passing `>= 0.5` decisions gives a different, worse number. Q1 is on the **training set**.

**4. Threshold loops have two edges.** At high thresholds nothing is predicted positive, so precision is 0/0 (decide what you store there before taking a minimum). `np.arange(0, 1.01, 0.01)` produces `0.07000000000000001`-style values, so round before reading the threshold off.

**5. Cross-validation runs on `df_full_train`, which still holds `converted`.** Fit a **new** `DictVectorizer` inside every fold, take `y` from the fold, keep `converted` out of the feature dicts. Q6: round mean and std to 3 digits, then apply the tie rules (lowest std, then smallest `C`).

---

## Lessons in this folder

| File | Title | Words | Video |
|---|---|---:|---|
| [01-overview.md](lessons/01-overview.md) | 4.1 Evaluation metrics: session overview | 690 | [video](https://www.youtube.com/watch?v=gmg5jw1bM8A&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [02-accuracy.md](lessons/02-accuracy.md) | 4.2 Accuracy and dummy model | 853 | [video](https://www.youtube.com/watch?v=FW_l7lB0HUI&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [03-confusion-table.md](lessons/03-confusion-table.md) | 4.3 Confusion table | 793 | [video](https://www.youtube.com/watch?v=Jt2dDLSlBng&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [04-precision-recall.md](lessons/04-precision-recall.md) | 4.4 Precision and Recall | 649 | [video](https://www.youtube.com/watch?v=gRLP_mlglMM&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [05-roc.md](lessons/05-roc.md) | 4.5 ROC Curves | 1,325 | [video](https://www.youtube.com/watch?v=dnBZLk53sQI&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [06-auc.md](lessons/06-auc.md) | 4.6 ROC AUC | 747 | [video](https://www.youtube.com/watch?v=hvIQPAwkVZo&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [07-cross-validation.md](lessons/07-cross-validation.md) | 4.7 Cross-Validation | 921 | [video](https://www.youtube.com/watch?v=BIIZaVtUbf4&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [08-summary.md](lessons/08-summary.md) | 4.8 Summary | 367 | [video](https://www.youtube.com/watch?v=-v8XEQ2AHvQ&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR) |
| [09-explore-more.md](lessons/09-explore-more.md) | 4.9 Explore more | 135 | — |

~6,480 words ≈ 27 min of reading. Alexey's lecture notebook is in [notebooks/](notebooks/).

## What is where

```
cohort2026/
├── START_HERE.md                         ← this file
├── lessons/                              ← 9 written lessons + images/
├── notebooks/                            ← Alexey's lecture notebook + data-week-3.csv (Telco)
├── practice/                             ← your practice notebook, the commented walkthrough + data-week-3.csv
└── homework/
    ├── Homework4_2026.ipynb              ← scaffold: data prep, Q1–Q6, no answers
    ├── homework4_2026.md                 ← the official question text
    └── course_lead_scoring_2026.csv      ← the 2026 pinned dataset (5,000 leads, same file as HW3)
```

## Connections

- [Home](../../../00_Reference_Materials/Home.md) · [Resource Map](../../../00_Reference_Materials/Resource_Map_Cohort2026.md)
- [Playbook](../../../00_Reference_Materials/ML_Strategist_Playbook.md): *Hold-out vs k-fold cross-validation*, `cross_val_score` (no AUC card yet)
- Used by: [Midterm: hospital readmission](../../../00_Reference_Materials/projects/Midterm_Readmission.md)
- Used by: [Capstone 1: turbofan RUL](../../../00_Reference_Materials/projects/Capstone1_CMAPSS.md)

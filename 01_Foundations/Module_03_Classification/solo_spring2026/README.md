# Module 3 — Classification (Customer Churn)

**Zoomcamp ch.3 · started 2026-06-12 · v3 plan window: Jun 1–14**

First production **classifier** workflow: logistic regression, categorical encoding, and reasoning about feature importance.

## Dataset
`WA_Fn-UseC_-Telco-Customer-Churn.csv` — IBM Telco customer churn (from Alexey's `chapter-03-churn-prediction`).

- **Rows / cols:** 7043 × 21
- **Target:** `Churn` (Yes/No) → encode to 1/0
- **Base rate:** 26.5% churn (5174 No / 1869 Yes) — *imbalanced, so accuracy lies*
- **Known gotcha:** `TotalCharges` loads as `object` (string); 11 blank rows (tenure-0 customers) need coercion + fill

Source: <https://github.com/alexeygrigorev/mlbookcamp-code/tree/master/chapter-03-churn-prediction>

## Files
| File | Purpose |
|------|---------|
| `03_classification_churn.ipynb` | **Your scaffold** — workflow sections + strategic questions + empty cells. Code it yourself. |
| `practice/alexey_reference_03-churn.ipynb` | Alexey's full chapter solution. Peek only after attempting. |
| `practice/alexey_reference_04-metrics.ipynb` | Next chapter (ch.4 metrics) reference. |

## What this chapter is really about (the strategist view)
Not "how to call LogisticRegression" — that's syntax. It's:
1. **Why accuracy is misleading** on imbalanced data (always-predict-No already scores ~73.5%).
2. **Quantifying feature importance** before modelling — churn rate per group, **risk ratio**, mutual information, correlation.
3. **One-hot encoding** via `DictVectorizer` and why a linear model needs it.
4. **Interpreting coefficients** — reading the model's mind, sign by sign.

## ⚠️ sklearn-vs-lecture flag
sklearn's `LogisticRegression` applies **L2 regularization by default** (`C=1.0`); Alexey's hand-rolled numpy version doesn't. When numbers diverge, suspect this first. Internalize the **sklearn** headline; treat the numpy as intuition scaffolding. (Same pattern that bit HW2 Q4.)

## On completion
- Append Playbook cards: logistic regression, one-hot / DictVectorizer, mutual information, risk ratio.
- Update `_Tracking` + CLAUDE.md progress log.
- → ch.4 metrics (precision/recall, ROC-AUC).

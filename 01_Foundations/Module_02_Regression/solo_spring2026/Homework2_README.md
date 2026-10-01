# Homework 2 — Regression (Car Fuel Efficiency)

**Source:** [DataTalksClub / ml-zoomcamp / cohorts / 2025 / 02-regression](https://github.com/DataTalksClub/machine-learning-zoomcamp/blob/master/cohorts/2025/02-regression/homework.md)

**Dataset:** `car_fuel_efficiency.csv` — predict `fuel_efficiency_mpg`.
Source URL: <https://raw.githubusercontent.com/alexeygrigorev/datasets/master/car_fuel_efficiency.csv>

**Columns to use:**
`engine_displacement`, `horsepower`, `vehicle_weight`, `model_year`, `fuel_efficiency_mpg`

---

## EDA
Look at `fuel_efficiency_mpg` — does it have a long tail?

## Q1
There's one column with missing values. Which one?
Options: `engine_displacement`, `horsepower`, `vehicle_weight`, `model_year`

## Q2
What's the median (50% percentile) for `horsepower`?
Options: 49, 99, 149, 199

## Prepare & split
Shuffle (seed = 42), then split 60/20/20 into train/val/test. Use the lecture code.

## Q3
Two strategies for the missing column: fill with `0` vs. fill with **train-set mean**.
Train linear regression (no regularisation) on each, evaluate RMSE on val (`round(score, 2)`).
Which option wins?
Options: With 0 / With mean / Both equally good

## Q4
Regularised linear regression, fill NAs with `0`.
Try `r ∈ [0, 0.01, 0.1, 1, 5, 10, 100]`. Best RMSE on val (`round(score, 2)`).
Tie-break: pick the smallest `r`.
Options: 0, 0.01, 1, 10, 100

## Q5
Repeat the split with seeds `[0..9]`, fill NAs with `0`, no regularisation.
Compute `np.std` of the val RMSEs, `round(std, 3)`.
Options: 0.001, 0.006, 0.060, 0.600

## Q6
Seed `9`, combine train + val, fill NAs with `0`, train with `r = 0.001`.
RMSE on **test** set.
Options: 0.15, 0.515, 5.15, 51.5

---

**Submit:** <https://courses.datatalks.club/ml-zoomcamp-2025/homework/hw02>

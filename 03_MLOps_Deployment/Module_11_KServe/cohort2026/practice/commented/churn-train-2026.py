# NOT a lecture file: the 2026 variant of churn-train.py for a current KServe sklearn server.
# Tested (Oct 2026) against KServe 0.21.0's sklearnserver run locally with scikit-learn 1.5.2, outside
# Kubernetes; the cluster part (churn-service-2026.yaml) was NOT tested.
#
# Run it in an environment that matches the server image, e.g.
#   conda create -n kserve-train python=3.12 "scikit-learn=1.5.2" "pandas<3" joblib
#   conda activate kserve-train && python churn-train-2026.py      (from practice/commented/)
# Check the pin for YOUR KServe version in python/sklearnserver/pyproject.toml of that release.

import os

import joblib
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression

# GOAL: same data and cleaning as churn-train.py.
df = pd.read_csv('../data-week-3.csv')
df.columns = df.columns.str.lower().str.replace(' ', '_')

for c in df.select_dtypes(include=['object', 'string']).columns:
    df[c] = df[c].str.lower().str.replace(' ', '_')

df.churn = (df.churn == 'yes').astype(int)

numerical = ['tenure', 'monthlycharges']
categorical = ['contract']

# GOAL: a pipeline whose input is a DataFrame, because that is what the current server hands to .predict().
# WHY: current KServe (checked: 0.21) converts each dict in "instances" with pd.DataFrame(instance) and concatenates them.
#      DictVectorizer iterates over a DataFrame's column NAMES (strings) and fails with
#      "'str' object has no attribute 'items'". ColumnTransformer selects columns by name, so it works.
# PYTHON: ColumnTransformer([(name, transformer, columns)], remainder='passthrough') one-hot encodes
#         'contract' and passes the two numeric columns through unchanged.
#         handle_unknown='ignore' -> an unseen contract value becomes all zeros instead of an error.
preprocessor = ColumnTransformer(
    [('onehot', OneHotEncoder(handle_unknown='ignore'), categorical)],
    remainder='passthrough',
)

pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('model', LogisticRegression(C=1.0, solver='liblinear')),
])

# PYTHON: fit on a DataFrame (not a list of dicts) so the column names are remembered for prediction.
pipeline.fit(df[categorical + numerical], df.churn.values)

# WHY: one model file per directory: the server refuses a directory with two .joblib files.
os.makedirs('model_2026', exist_ok=True)
joblib.dump(pipeline, 'model_2026/model.joblib')

# GOAL: the request shape that works with this model on KServe 0.21: each instance is {column: [value]}.
#   {"instances": [{"contract": ["one_year"], "tenure": [34], "monthlycharges": [56.95]}, ...]}
# The lecture's {"contract": "one_year", ...} (scalars) fails in pandas: "If using all scalar values,
# you must pass an index".

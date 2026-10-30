# Commented copy of notebooks/code/churn/churn-train.py (lesson 11.3).
# Run it from practice/commented/:  python churn-train.py  -> writes model.joblib next to this file.
#
# 2026: the KServe sklearn server unpickles model.joblib with ITS OWN scikit-learn version
#       (KServe 0.21 ships scikit-learn 1.5.2, pandas < 3). Train in an environment with that version,
#       not in your pandas 3 / scikit-learn 1.9 notebook env: a 1.9 model served by 1.5.2 fails with
#       "'LogisticRegression' object has no attribute 'multi_class'". The repo's model.joblib (sklearn 1.0)
#       only half-works on 1.9 (predicts, but printing it fails on 'transform_input').
# 2026: this DictVectorizer pipeline worked with KServe 0.8, which passed the request rows as a list of
#       dicts. Current KServe turns dict rows into a pandas DataFrame first, and DictVectorizer cannot read
#       a DataFrame. churn-train-2026.py is the variant that works with today's server.

# PYTHON: joblib is scikit-learn's preferred pickler: it stores the fitted object (here a whole Pipeline) in one file.
import joblib

import pandas as pd
import numpy as np

# PYTHON: Pipeline chains steps; .fit() runs them in order, .predict() replays them on new data.
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression

# GOAL: load the Telco churn data (the same file as Modules 3-4).
# WHY: the lecture reads a GitHub URL; the local copy in practice/ is identical and works offline.
df = pd.read_csv('../data-week-3.csv')

# GOAL: the Module 3 cleaning, unchanged.
df.columns = df.columns.str.lower().str.replace(' ', '_')

# WHY: on pandas 3 text columns have dtype 'str', so the lecture's df.dtypes == 'object' finds NO columns.
#      Nothing gets lower-cased, churn == 'yes' never matches, y is all 0, and scikit-learn 1.9 stops with a
#      misleading "'liblinear' solver does not support multiclass classification" error.
#      select_dtypes(include=['object', 'string']) works on pandas 2 and 3.
categorical_columns = list(df.select_dtypes(include=['object', 'string']).columns)

for c in categorical_columns:
    df[c] = df[c].str.lower().str.replace(' ', '_')

df.totalcharges = pd.to_numeric(df.totalcharges, errors='coerce')
df.totalcharges = df.totalcharges.fillna(0)

df.churn = (df.churn == 'yes').astype(int)

# GOAL: a deliberately tiny model, 3 inputs only.
# WHY: the point of 11.3 is the deployment, not the model; three fields keep the JSON request readable.
numerical = ['tenure', 'monthlycharges']
categorical = ['contract']

# PYTHON: to_dict(orient='records') -> one {column: value} dict per customer, DictVectorizer's input format.
dicts = df[categorical + numerical].to_dict(orient='records')

# GOAL: put the vectorizer AND the model in one object.
# WHY: KServe's sklearn server loads exactly ONE file and calls .predict() on it. If the DictVectorizer were
#      saved separately, the server would have no way to one-hot encode the request. A Pipeline is the
#      "preprocessing travels with the model" pattern you will reuse for every deployed model.
pipeline = Pipeline([
    ('vectorizer', DictVectorizer(sparse=False)),
    ('model', LogisticRegression(C=1.0, solver='liblinear'))
])

# PYTHON: Pipeline.fit(X, y) = vectorizer.fit_transform(X), then model.fit(result, y).
pipeline.fit(dicts, df.churn.values)

# GOAL: write the artefact the InferenceService will download (storageUri in churn-service.yaml).
# WHY: the sklearn server looks for a single .joblib / .pkl / .pickle file in the model directory.
joblib.dump(pipeline, 'model.joblib')

#!/usr/bin/env python
# coding: utf-8
# Commented copy of 05-deployment/code/train.py (lesson 5.2: "turning the notebook into a script").
# The original is untouched in ../../notebooks/code/train.py.
# Only change vs the original: text columns are found with select_dtypes (pandas 3 fix, see below).
#
# Run it from practice/ (where data-week-3.csv lives):   python commented/train.py
# Output: model_C=1.0.bin in the CURRENT directory.

# GOAL: the whole Module 3+4 notebook as one script that ends in a saved model file.
# WHY:  a notebook is for exploring; a script can be re-run by anyone (or by a scheduler / CI job)
#       with one command and gives the same artifact every time. Deployment starts from an artifact.
import pickle

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score


# parameters

# GOAL: every knob at the top of the file, so changing a run means changing one line.
# PYTHON: f'model_C={C}.bin' is an f-string: {C} is replaced by the value of C -> 'model_C=1.0.bin'.
C = 1.0
n_splits = 5
output_file = f'model_C={C}.bin'


# data preparation

df = pd.read_csv('data-week-3.csv')

df.columns = df.columns.str.lower().str.replace(' ', '_')

# WHY: on pandas 3 text columns have dtype 'str', not 'object'. The original line
#      list(df.dtypes[df.dtypes == 'object'].index) selects NOTHING there, so nothing is lower-cased,
#      churn == 'yes' never matches, every label is 0 and LogisticRegression stops with
#      "only one class". select_dtypes with both names works on old and new pandas.
categorical_columns = list(df.select_dtypes(include=['object', 'string']).columns)

for c in categorical_columns:
    df[c] = df[c].str.lower().str.replace(' ', '_')

# WHY: 11 blank totalcharges (brand-new customers) -> NaN -> 0 (nothing billed yet).
df.totalcharges = pd.to_numeric(df.totalcharges, errors='coerce')
df.totalcharges = df.totalcharges.fillna(0)

df.churn = (df.churn == 'yes').astype(int)

# WHY: only an 80/20 split here. Model selection is done by K-fold CV on the 80%, the 20% test
#      set is scored once at the end. Same seed (random_state=1) as Module 4.
df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=1)


numerical = ['tenure', 'monthlycharges', 'totalcharges']

categorical = [
    'gender',
    'seniorcitizen',
    'partner',
    'dependents',
    'phoneservice',
    'multiplelines',
    'internetservice',
    'onlinesecurity',
    'onlinebackup',
    'deviceprotection',
    'techsupport',
    'streamingtv',
    'streamingmovies',
    'contract',
    'paperlessbilling',
    'paymentmethod',
]

# training

# GOAL: dataframe in -> fitted (dv, model) out. Same function as in Module 4.
# WHY:  the DictVectorizer is created INSIDE, so each CV fold learns its column layout from its own
#       training part only (no leakage from the validation fold).
def train(df_train, y_train, C=1.0):
    dicts = df_train[categorical + numerical].to_dict(orient='records')

    dv = DictVectorizer(sparse=False)
    X_train = dv.fit_transform(dicts)

    model = LogisticRegression(C=C, max_iter=1000)
    model.fit(X_train, y_train)

    return dv, model


# GOAL: dataframe in -> churn probabilities out (transform only, never fit).
def predict(df, dv, model):
    dicts = df[categorical + numerical].to_dict(orient='records')

    X = dv.transform(dicts)
    y_pred = model.predict_proba(X)[:, 1]

    return y_pred


# validation

print(f'doing validation with C={C}')

# GOAL: 5-fold CV on df_full_train, to report AUC mean +- std for this C.
kfold = KFold(n_splits=n_splits, shuffle=True, random_state=1)

scores = []

fold = 0

for train_idx, val_idx in kfold.split(df_full_train):
    df_train = df_full_train.iloc[train_idx]
    df_val = df_full_train.iloc[val_idx]

    y_train = df_train.churn.values
    y_val = df_val.churn.values

    dv, model = train(df_train, y_train, C=C)
    y_pred = predict(df_val, dv, model)

    auc = roc_auc_score(y_val, y_pred)
    scores.append(auc)

    # WHY: printing per fold is the script's "log": when you run it unattended, this is all you see.
    print(f'auc on fold {fold} is {auc}')
    fold = fold + 1


print('validation results:')
print('C=%s %.3f +- %.3f' % (C, np.mean(scores), np.std(scores)))


# training the final model

# GOAL: retrain on ALL of df_full_train and score once on the untouched test set.
print('training the final model')

dv, model = train(df_full_train, df_full_train.churn.values, C=1.0)
y_pred = predict(df_test, dv, model)

y_test = df_test.churn.values
auc = roc_auc_score(y_test, y_pred)

print(f'auc={auc}')


# Save the model

# GOAL: write the fitted objects to disk so another process (the web service) can load them.
# WHY:  BOTH objects are needed at prediction time: the dv knows the one-hot column layout,
#       the model knows the weights. Saving only the model would leave the service unable to
#       turn a customer dict into the right feature vector.
# PYTHON: 'wb' = write binary (pickle produces bytes, not text). The 'with' block closes the file
#         even if an error happens; pickle.dump((dv, model), f) stores the tuple as one object.
#         The workshop and HW5 instead save ONE sklearn Pipeline (DictVectorizer + model) - see
#         commented/workshop/train.py.
with open(output_file, 'wb') as f_out:
    pickle.dump((dv, model), f_out)

print(f'the model is saved to {output_file}')

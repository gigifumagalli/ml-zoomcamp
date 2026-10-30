#!/usr/bin/env python
# Commented copy of 05-deployment/workshop/train.py (the 2025 uv + FastAPI workshop).
# The original is untouched in ../../../notebooks/workshop/train.py.
# Changes vs the original: text columns found with select_dtypes (pandas 3 fix) and
# DictVectorizer(sparse=False) (scikit-learn 1.9 fix). Both explained where they happen.
#
# Run it from practice/:   python commented/workshop/train.py   -> writes model.bin in the CURRENT directory.
# It downloads the Telco CSV from GitHub (same data as data-week-3.csv), so it needs internet.

import pickle

import pandas as pd
import numpy as np
import sklearn


from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline


# GOAL: log the library versions that produced the artifact.
# WHY:  a pickle can only be trusted when loaded by the SAME scikit-learn version that wrote it.
#       Printing them is the cheap version of what HW5's train.py does properly: it writes the
#       versions and checksums into model_metadata.json next to pipeline.bin.
print(f'pandas=={pd.__version__}')
print(f'numpy=={np.__version__}')
print(f'sklearn=={sklearn.__version__}')


# GOAL: one function per stage (load / train / save), so the script reads like the pipeline it is.
def load_data():
    data_url = 'https://raw.githubusercontent.com/alexeygrigorev/mlbookcamp-code/master/chapter-03-churn-prediction/WA_Fn-UseC_-Telco-Customer-Churn.csv'

    df = pd.read_csv(data_url)

    df.columns = df.columns.str.lower().str.replace(' ', '_')

    # WHY: pandas 3 fix. The original df.dtypes == 'object' selects no column on pandas 3, so every
    #      churn label becomes 0 and LogisticRegression refuses to train ("only one class").
    categorical_columns = list(df.select_dtypes(include=['object', 'string']).columns)

    for c in categorical_columns:
        df[c] = df[c].str.lower().str.replace(' ', '_')

    df.totalcharges = pd.to_numeric(df.totalcharges, errors='coerce')
    df.totalcharges = df.totalcharges.fillna(0)

    df.churn = (df.churn == 'yes').astype(int)
    return df




def train_model(df):
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


    # WHY: no split and no CV here: the workshop is about deployment, so it trains the final model on
    #      ALL rows. Model selection was done in Modules 3-4; do not copy this shortcut into a project.
    y_train = df.churn
    train_dict = df[categorical + numerical].to_dict(orient='records')

    # GOAL: ONE object that goes from raw dicts to probabilities.
    # WHY:  the lecture saves (dv, model) and the service must call dv.transform then model.predict_proba,
    #       in the right order, with the right dv. A Pipeline glues them: fit() fits both, predict_proba()
    #       runs both. One artifact, one call, no way to pair the wrong dv with the wrong model.
    #       HW5's pipeline.bin is exactly this shape (DictVectorizer + liblinear LogisticRegression).
    # PYTHON: make_pipeline(step1, step2) names the steps automatically ('dictvectorizer', ...).
    # WHY (sparse=False): scikit-learn 1.9's DictVectorizer emits sparse matrices with 64-bit indices and
    #      liblinear refuses them at fit ("Only sparse matrices with 32-bit integer indices are accepted").
    #      The original DictVectorizer() works on 1.7/1.8 only. Dense output gives the same model here.
    pipeline = make_pipeline(
        DictVectorizer(sparse=False),
        LogisticRegression(solver='liblinear')
    )

    pipeline.fit(train_dict, y_train)

    return pipeline


def save_model(pipeline, output_file):
    # PYTHON: 'wb' = write binary; pickle serialises the whole fitted pipeline into bytes.
    with open(output_file, 'wb') as f_out:
        pickle.dump(pipeline, f_out)



df = load_data()
pipeline = train_model(df)
save_model(pipeline, 'model.bin')

print('Model saved to model.bin')

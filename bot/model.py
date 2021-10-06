from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer

import pandas as pd
import numpy as np


class ObesityDummyEncoder:
    """Manually encode following columns:
    Gender, family_history_with_overweight, FAVC, CAEC, SMOKE, SCC, CALC
    """
    def __init__(self):
        self.transform_matrix = {
            'male': 0,
            'female': 1,
            'no': 0,
            'yes': 1,
            'sometimes': 1,
            'frequently': 2,
            'always': 3
        }
        self.inverse_transform_matrix = {
            'Gender': {
                0: 'Male',
                1: 'Female'
            },
            'family_history_with_overweight': {
                0: 'no',
                1: 'yes'
            },
            'FAVC': {
                0: 'no',
                1: 'yes'
            },
            'SMOKE': {
                0: 'no',
                1: 'yes'
            },
            'CAEC': {
                0: 'no',
                1: 'Sometimes',
                2: 'Frequently',
                3: 'Always'
            },
            'SCC': {
                0: 'no',
                1: 'yes'
            },
            'CALC': {
                1: 'Sometimes',
                2: 'Frequently'
            }
        }

    def transfrom(self, x):
        """Transform string into integer. Design for pd.Series.apply"""
        return self.transform_matrix[x.lower()]

    def inverse_transform(self, x, column):
        return self.inverse_transform_matrix[column][x.lower()]


class Model:
    """
    Model for classifaction. We only implement random forest classifier.
    """
    def __init__(self, data_path=None):
        self.clr = RandomForestClassifier(n_jobs=-1)
        self.dpath = 'data/ObesityDataSet_raw_and_data_sinthetic.csv' \
                     if data_path is None else data_path
        self.encoder = ObesityDummyEncoder()
        self.lb= LabelBinarizer()

    def set_data(self, path):
        self.dpath = path

    def transform(self, subj: dict):
        """Transform new subject."""
        for i in ['Gender', 'family_history_with_overweight', 'FAVC',
                  'CAEC', 'SMOKE', 'SCC', 'CALC']:
            subj[i] = self.encoder.transfrom(subj[i])

        arr = self.lb.transform([subj['MTRANS']])[0][1:]
        for i in range(4):
            subj[f'MTRANS{i + 2}'] = arr[i]

        return np.array([subj['Gender'], subj['Age'],
                subj['family_history_with_overweight'],
                subj['FAVC'], subj['FCVC'], subj['NCP'], subj['CAEC'],
                subj['SMOKE'], subj['CH2O'], subj['SCC'], subj['FAF'],
                subj['TUE'], subj['CALC'], subj['MTRANS2'],
                subj['MTRANS3'], subj['MTRANS4'], subj['MTRANS5']]
                ).reshape(1, -1)

    def load(self):
        self.df = pd.read_csv(self.dpath)
        self.df = self.df.drop(['Height', 'Weight'], axis=1)  # useless

        self.df['Gender'] = self.df['Gender'].apply(self.encoder.transfrom)
        fhwo = 'family_history_with_overweight'
        self.df[fhwo] = self.df[fhwo].apply(self.encoder.transfrom)
        self.df['FAVC'] = self.df['FAVC'].apply(self.encoder.transfrom)
        self.df['CAEC'] = self.df['CAEC'].apply(self.encoder.transfrom)
        self.df['SMOKE'] = self.df['SMOKE'].apply(self.encoder.transfrom)
        self.df['SCC'] = self.df['SCC'].apply(self.encoder.transfrom)
        self.df['CALC'] = self.df['CALC'].apply(self.encoder.transfrom)

        mtrans = pd.DataFrame(self.lb.fit_transform(self.df.MTRANS),
                              columns=['MTRANS1', 'MTRANS2', 'MTRANS3',
                                       'MTRANS4', 'MTRANS5'])

        self.df = pd.concat([self.df.drop(columns='MTRANS'),
                            mtrans.iloc[:, 1:]],   # n-1 columns is enough
                            axis=1)

        self.results = self.df['NObeyesdad'].unique()

    def fit(self):
        X_train, X_test, y_train, y_test = train_test_split(
                self.df.drop(['NObeyesdad'], axis=1),
                self.df['NObeyesdad'], test_size=.3
                )
        self.clr.fit(X_train, y_train)

        del self.df  # we don't need it anymore

        return self.clr.score(X_test, y_test)

    def predict(self, X):
        return self.clr.predict(X)[0]

    def load_fit(self):
        self.load()
        return self.fit()

    def transform_predict(self, subj):
        return self.predict(self.transform(subj))

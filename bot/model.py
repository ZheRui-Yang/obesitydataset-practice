from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer

import pandas as pd


class ObesityDummyEncoder:

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
        return self.transform_matrix[x.lower()]

    def inverse_transform(self, x, column):
        return self.inverse_transform_matrix[column][x.lower()]


class Model:
    """
    Model for classifaction. We only implement random forest classifier.
    """
    def __init__(self, data_path=None):
        self.clr = RandomForestClassifier(n_estimators=100, n_jobs=-1)

    def set_data(self, path):
        self.dpath = path

    def load(self):
        self.df = pd.read_csv(self.dpath)
        self.df = self.df.drop(['Height', 'Weight'], axis=1)  # useless

        dummy_encoder = ObesityDummyEncoder()

        self.df['Gender'] = self.df['Gender'].apply(dummy_encoder.transfrom)
        fhwo = 'family_history_with_overweight'
        self.df[fhwo] = self.df[fhwo].apply(dummy_encoder.transfrom)
        self.df['FAVC'] = self.df['FAVC'].apply(dummy_encoder.transfrom)
        self.df['CAEC'] = self.df['CAEC'].apply(dummy_encoder.transfrom)
        self.df['SMOKE'] = self.df['SMOKE'].apply(dummy_encoder.transfrom)
        self.df['SCC'] = self.df['SCC'].apply(dummy_encoder.transfrom)
        self.df['CALC'] = self.df['CALC'].apply(dummy_encoder.transfrom)

        lb = LabelBinarizer()
        mtrans = pd.DataFrame(lb.fit_transform(self.df.MTRANS),
                              columns=['MTRANS1', 'MTRANS2', 'MTRANS3',
                                       'MTRANS4', 'MTRANS5'])

        self.df = pd.concat([self.df.drop(columns='MTRANS'),
                            mtrans.iloc[:, 1:]],   # n - 1 columns is enough
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
        trial = self.clt.predict(X)
        # TODO: finish this
        return {'foo': 'bar'}[trial]


if __name__ == "__main__":
    default_data_path = Path(
        '../data/ObesityDataSet_raw_and_data_sinthetic.csv').resolve()
    model = Model()
    model.set_data(default_data_path)
    model.load()
    print(model.fit())

from datetime import datetime
import re

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class Adaptor(BaseEstimator, TransformerMixin):
    """Take raw loan data from API, clean and transform it into pandas dataframe
    """
    def fit(self, X, y=None):
        return self

    def process_dates(self, X):

        for date_col in ['acceptD', 'expD', 'listD']:
            X[date_col] = X[date_col].apply(
                lambda x: datetime.strptime(x[:19], '%Y-%m-%dT%H:%M:%S')
            )

    def std_names(self, X):
        for loan in X:
            for key in loan.keys():
                if key[-1] != 'D':
                    new_key = '_'.join(re.findall('[A-Za-z][^A-Z]*', key)).lower()
                    loan[new_key] = loan.pop(key)

    def transform(self, X, y=None):
        # Convert to dataframe:
        self.std_names(X)
        df = pd.DataFrame(X)
        self.process_dates(df)
        return df

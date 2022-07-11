from typing import List

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

# Categorical variables encoding (the encoding of categorical
# variables that already have ordered levels from strings to numeric)


class Mapper(BaseEstimator, TransformerMixin):
    """
    Constructor

    Args:
        variables (List[str]): a list of variables to be recoded (specified by user)
        mappings (dict): a dictionary of mappings from old to new encoding

    Returns:
        void
    """

    def __init__(self, variables: List[str], mappings: dict):

        if not isinstance(variables, list):
            raise ValueError("variables should be a list")

        if not isinstance(mappings, dict):
            raise ValueError("mapping should be a dictionary")

        # set attributes at instantiation of class
        self.variables = variables
        self.mappings = mappings

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        """Fit
        Args:
            X (DataFrame): a input dataframe of features to train the transformer
            y (DataFrame): a input Series of response
             variable to train the transformer (optional)

        Returns:
            self
        """

        # need to have y as argument to make class compatible with sklearn pipeline

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Transform

        Args:
            X (DataFrame): a input dataframe of features to be transformed

        Returns:
            X (DataFrame): the transformed Dataframe of features
        """
        #  Make a copy of the input Dataframe of features to be transformed
        #  so we won't overwrite the original Dataframe that was passed as argument
        X = X.copy()

        # Perform recoding of the levels of var
        for feature in self.variables:
            X[feature] = X[feature].map(self.mappings)

        return X

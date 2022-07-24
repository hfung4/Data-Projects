import json
from pathlib import Path
from typing import List

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from survey_analysis.config.core import OUTPUTS_DIR, PIPELINE_DEBUG_DIR, config

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


# The Debug pipeline returns a .csv of the output dataframe at each particular step
# that can be used for further visualization/validation/debugging
class Debug(BaseEstimator, TransformerMixin):
    """
    Constructor

    Args:
        step_name str: the pipeline step whose output I am saving
        get_unique_levels bool: if True, output a json file
        that contains the unique level of each variable in the output dataframe

    Returns:
        void
    """

    def __init__(self, step_name: str, get_unique_levels=False):

        # set attributes at instantiation of class
        self.step_name = step_name
        self.get_unique_levels = get_unique_levels

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

        # save the output of this step of the pipeline as csv
        X.to_csv(Path(PIPELINE_DEBUG_DIR, f"{self.step_name}_output_debug.csv"))

        # outut the unique levels of each variable in the output dataframe in a json file
        if self.get_unique_levels:

            d_col_levels = {
                col_name: sorted(X[col_name].astype(str).unique().tolist())
                for col_name in X.columns.values
            }
            with open(
                Path(
                    OUTPUTS_DIR,
                    f"{self.step_name}_"
                    + config.app_config.processed_data_col_levels_file,
                ),
                "w",
            ) as f:
                f.write(json.dumps(d_col_levels))

        return X

import pickle
from pathlib import Path
from typing import Union

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from cr_analysis.config.core import PIPELINE_DEBUG_DIR, config


# This custom step saves the column names of its input dataframe as a binary .pkl file
class save_col_names(BaseEstimator, TransformerMixin):
    """
    Constructor

    Args:
        step_name: the name of the step
        prior to "save_col_names". I want to
        save the column names of that step

    Returns:
        void
    """

    def __init__(self):
        pass

    def fit(
        self, X, y=None
    ):  # need to have y as argument to make class compatible with sklearn pipeline
        """Fit

        Args:
            X (DataFrame): a input dataframe of features
            to train the transformer
            y (DataFrame): a input Series of response variable
            to train the transformer (optional)

        Returns:
            self
        """

        return self

    def transform(self, X):
        """Transform

        Args:
            X (DataFrame): a input dataframe of features to be transformed

        """

        # Make a copy of the input dataframe
        # so we won't overwrite the original Dataframe that was passed as argument
        X = X.copy()

        # Get feature names
        feature_names = X.columns.tolist

        # Save as pickle
        with open(
            Path(PIPELINE_DEBUG_DIR, config.model_config.SAVED_COL_NAME_FILE), "wb"
        ) as f:
            pickle.dump(feature_names, f)

        return X


# The data_pipeline_debug is a data pipeline that returns
# a .csv of the output dataframe at each particular step
# that can be used for further visualization/validation/debugging
# I construct data_pipeline_debug by inserting the custom
# Debug step between each steps of data_pipeline.
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

    def __init__(self, step_name: str):

        # set attributes at instantiation of class
        self.step_name = step_name

    def fit(self, X: Union[pd.DataFrame, np.ndarray], y: pd.Series = None):
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

    def transform(self, X: Union[pd.DataFrame, np.ndarray]) -> pd.DataFrame:
        """Transform

        Args:
            X (DataFrame or ndarray): a input dataframe of features to be transformed

        Returns:
            X (DataFrame): the transformed Dataframe of features
        """
        #  Make a copy of the input Dataframe of features
        # to be transformed
        #  so we won't overwrite the original Dataframe that
        # was passed as argument
        X = X.copy()

        # Input is not a dataframe (but instead a np.ndarray), the
        # input is from a sklearn or imblearn step
        # rather than a feature-engine step
        if not isinstance(X, pd.DataFrame):

            # Read the latest feature names that is saved
            with open(
                Path(PIPELINE_DEBUG_DIR, config.model_config.SAVED_COL_NAME_FILE), "rb"
            ) as f:
                list_ = pickle.load(f)
            saved_feature_names = list_()

            # Convert np.ndarray to dataframe
            X = pd.DataFrame(X, columns=saved_feature_names)

        # save the output of this step of the pipeline as csv
        X.to_csv(
            Path(PIPELINE_DEBUG_DIR, f"{self.step_name}_output_debug.csv"), index=False
        )

        return X

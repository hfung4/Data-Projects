import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from home_price_analysis.config.core import config


class area_type_step(BaseEstimator, TransformerMixin):
    """
    Constructor

    Args:
       void

    Returns:
        void
    """

    def __init__(self):
        pass

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        """Fit
        Args:
            X (DataFrame): a input dataframe of features to train the transformer
            y (DataFrame): a input Series of response
             variable to train the transformer (optional)

        Returns:
            self
        """
        # compute the top n area type
        self.topn = (
            X["area_type"]
            .value_counts(sort=True)
            .index[: config.model_config.AREA_TYPE_RETAIN]
        )

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

        # Perform variable processsing

        # Recode all instances whose values are not in "topn" to "Other"
        X["area_type"] = X["area_type"].where(X["area_type"].isin(self.topn), "Other")

        return X


class avail_step(BaseEstimator, TransformerMixin):
    """
    Constructor

    Args:
       void

    Returns:
        void
    """

    def __init__(self):
        pass

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

        # Perform variable processsing
        X["availability"] = (
            X["availability"]
            .apply(
                lambda x: "ready_to_move"
                if (x == "Ready To Move")
                else "not_ready_to_move"
            )
            .astype("category")
        )

        return X

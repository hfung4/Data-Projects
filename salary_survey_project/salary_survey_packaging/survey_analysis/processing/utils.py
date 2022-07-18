""" This module contains various helper functions for data processing and modelling"""

import pandas as pd


def parse_num_get_levels(df: pd.DataFrame, col: str):
    """
    parse_num_get_levels: this function takes a variable from a dataframe, and
    then parse the first integer in each value (e.g., 18-35 ====> get 18).
    The levels in the variable is then sorted based on the first integer and are used
    when converting the variable to an ordered categorical variable (from string variable)

    Args:
        df (pd.Dataframe): input dataframe
        col (str): name of the target column

    Returns:
        void
    """

    # Get ordered levels based on the first integer of each level (e.g. 18-35 ===> 18)
    ordered_levels = (
        df[col]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "levels"})
        # extract the first one (or more) digits
        .assign(num_levels=lambda x: x.levels.str.extract(r"(\d+)").astype(int))
        .sort_values("num_levels")
        .levels.tolist()
    )

    # create categorical type
    categorical_type = pd.api.types.CategoricalDtype(
        categories=ordered_levels, ordered=True
    )

    # convert col to ordered categorical type
    df[col] = df[col].astype(categorical_type)


def remove_outlier(
    df_in: pd.DataFrame, col: str, lwr_bound: int = None, upr_bound: int = None
) -> pd.DataFrame:
    """
    remove_outlier: remove outliers (based on a variable). All rows
    # with values (of the variable) that is outside of q1+/- 1.5*iqr is removed
    # users can also set the upper and lower bound of outlier removal

    Args:
        df_in (pd.Dataframe): input dataframe
        col (str): name of the target column
        lwr_bound(int): user defined lower bound of outlier removal
        uper_bound(int): user defined upper bound of outlier removal

    Returns:
        df_out: dataframe with outliers removed
    """
    # Get the interquantile range
    q1 = df_in[col].quantile(0.25)
    q3 = df_in[col].quantile(0.75)
    iqr = q3 - q1  # Interquartile range

    if lwr_bound is None:
        lwr_bound = q1 - 1.5 * iqr

    if upr_bound is None:
        upr_bound = q3 + 1.5 * iqr

    # Filter out outliers
    df_out = df_in.loc[(df_in[col] > lwr_bound) & (df_in[col] < upr_bound)]
    return df_out

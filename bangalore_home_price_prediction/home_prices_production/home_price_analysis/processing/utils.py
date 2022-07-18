""" This module contains various helper functions for data processing and modelling"""

import re
from collections import OrderedDict

import numpy as np
import pandas as pd

from home_price_analysis.config.core import config


def process_total_sqft(input_str: str) -> float:
    """
    This function processes the total_sqft column
    (perform unit conversion, reformats values
    and averages total_sqft ranges)
    Args:
        input_str (PosixPath): data path object to the raw data csv

    Returns:
        processed value for total_sqft (float)
    """

    # search to see if input string has "-"
    if re.search("-", input_str):
        # Get a list of the ranges
        str_list = input_str.split(" - ")
        # Convert the list from string to float
        num_list = np.array([float(i) for i in str_list])
        # Compute the average of the two ranges
        return num_list.mean()

    # search to see if input string has "Sq. Meter"
    elif re.search("Sq. Meter", input_str):
        pattern = r"Sq. Meter"
        # remove "Sq.Meter", convert from string to float, and then convert to sq-ft
        return config.model_config.SQFT_PER_SQ_METER * float(
            re.sub(pattern, "", input_str)
        )

    elif re.search("Sq. Yards", input_str):
        # search to see if input string has "Sq. Yards"
        pattern = r"Sq. Yards"
        # remove "Sq. Yards", convert from string to float, and then convert to sq-ft
        return config.model_config.SQFT_PER_SQ_YARD * float(
            re.sub(pattern, "", input_str)
        )

    else:
        return np.nan


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


def preprocessing_total_sqft(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function preprocesses the total_sqft variable

    Args:
        df (pd.DataFrame): input dataframe

    Returns:
        data (pd.DataFrame): output dataframe
    """

    data = df.copy()

    # find all of the non numeric characters (disregarding space)
    mask = data["total_sqft"].str.extract(r"([^0-9.])", expand=False)  # return a series

    # Get a subset of the total_sqft column that contains non-numeric characters
    sub_ser = data["total_sqft"].loc[mask.notnull()]

    # process total_sqft elements that contains non-numeric characters
    sub_ser = sub_ser.apply(lambda x: process_total_sqft(x))

    # replace elements in total_sqft with non-numeric characters with the processed data
    data.loc[list(sub_ser.index), "total_sqft"] = sub_ser

    # drop all NA in total_sqft, and then convert the column to float
    data["total_sqft"] = data.total_sqft.dropna().astype(float)

    # Remove outliers in total_sqft
    data = remove_outlier(data, "total_sqft")

    return data


def preprocessing_size(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function preprocesses the size variable

    Args:
        df (pd.DataFrame): input dataframe

    Returns:
        data (pd.DataFrame): output dataframe
    """

    data = df.copy()

    # size
    # drop NA
    data.dropna(subset="size", inplace=True)

    # Remove the "BNK" and "Bedroom" and only retain the numeric value. We
    # do this by extracting the first one or more digits and then cast column to float
    data["size"] = data["size"].str.extract(r"(\d+)").astype(int)

    # Remove outliers in size
    data = remove_outlier(data, "size")

    return data


def preprocessing_area_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function preprocesses the area_type variable.
    It will reformat all strings in the variable

    Args:
        df (pd.DataFrame): input dataframe

    Returns:
        data (pd.DataFrame): output dataframe
    """

    data = df.copy()
    data["area_type"] = data["area_type"].apply(
        lambda x: replace_all(x, OrderedDict([("  ", " "), (" ", "_"), ("-", "_")]))
    )
    return data


def replace_all(text: str, d) -> str:
    """
    This function replace all text using a OrderedDict mapping

    Args:
        text (str): input str
        d (OrderDict): mapping dictionary

    Returns:
        text: processed text
    """
    for i, j in d.items():
        text = text.replace(i, j)
    return text


def chain(start: pd.DataFrame, *funcs) -> pd.DataFrame:
    """
    This function chains mutliple functions

    Args:
        start (pd.DataFrame): input/starting dataframe
        *funcs: one or more function arguments

    Returns:
        res: processed Dataframe
    """
    res = start
    for func in funcs:
        res = func(res)
    return res

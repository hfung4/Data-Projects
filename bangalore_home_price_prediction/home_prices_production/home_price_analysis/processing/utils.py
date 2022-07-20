""" This module contains various helper functions for data processing and modelling"""

import re
from collections import OrderedDict

import numpy as np
import pandas as pd

from home_price_analysis.config.core import config


def reformat_total_sqft(input_str: str) -> float:
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
    sub_ser = sub_ser.apply(lambda x: reformat_total_sqft(x))

    # replace elements in total_sqft with non-numeric characters with the processed data
    data.loc[list(sub_ser.index), "total_sqft"] = sub_ser

    # drop all NA in total_sqft, and then convert the column to float
    data.dropna(subset="total_sqft", inplace=True)
    data["total_sqft"] = data["total_sqft"].astype(float)

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


def fct_lump_location(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function retains locations with  more than 10 observations,
    and lump all locations with less than or equal to 10 observations to "Other"

    Args:
        df (pd.DataFrame): input dataframe

    Returns:
        data (pd.DataFrame): output dataframe
    """

    data = df.copy()

    # drop NA in location
    df.dropna(subset=["location"], inplace=True)

    # strip away all white space at the front and end
    df["location"] = df["location"].apply(lambda x: x.strip())

    val_counts = df["location"].value_counts()
    # Get all locations with more than 10 observations
    keep_locations = val_counts.loc[val_counts > 10].index

    # Retain locations with more than 10 observations,
    # lump the rest to others
    data["location"] = data["location"].where(
        data["location"].isin(keep_locations), "Other"
    )

    return data


def filter_bath_bedroom(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function filters out houses with bathrooms
    that are more than two more than bedrooms

    Args:
        df (pd.DataFrame): input dataframe

    Returns:
        data (pd.DataFrame): output dataframe
    """
    data = df.copy()

    # drop NA in bath
    data.dropna(subset=["bath"], inplace=True)
    # keep only houses with bath that are less than # of bedrooms (size) + 2
    data = data.loc[data["bath"] < (data["size"] + 2), :]
    return data


def filter_price_per_sqft(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function filters out houses with low and high values
    (outlier) of price per total sqft, by location

    Args:
        df (pd.DataFrame): input dataframe

    Returns:
        df_out (pd.DataFrame): output dataframe
    """
    df_in = df.copy()

    # Check to see if price is in the input data
    # Since price is the outcome variable, this only
    # happens if I have train data and I am training the
    # pipeline. Otherwise, I have new/unknown data
    # I will just return the input data
    if "price" in df_in.columns:

        # Compute price per total sqft
        try:
            df_in["price_per_total_sqft"] = df_in["price"] / df_in["total_sqft"]
        except ZeroDivisionError:
            print("Cannot divide by zero for price_per_total_sqft!")

        # init empty output dataframe
        df_out = pd.DataFrame()

        # Get dataframe per location group
        for key, df_per_group in df_in.groupby("location"):
            # get group mean and std
            group_mean = np.mean(df_per_group["price_per_total_sqft"])
            group_std = np.std(df_per_group["price_per_total_sqft"])

            # if the absolute standardized price_per_total_sqft is less than 1 then keep
            df_reduced = df_per_group.loc[
                abs(((df_per_group["price_per_total_sqft"] - group_mean) / group_std))
                < 1.0,
                :,
            ]

            # populate df_out (row concat)
            df_out = pd.concat([df_out, df_reduced], ignore_index=True)

        return df_out

    else:
        df_out = df_in
        return df_out


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

# This module contains data cleaning and formating functions

from typing import Dict, List

import numpy as np
import pandas as pd

from cr_analysis.config.core import config


# This function performs mapping for multiple columns in the input dataframe
# and convert the resulting columns as numeric
def obj_to_cont(
    vars: List[str], df: pd.DataFrame, mapping: Dict[str, int]
) -> pd.DataFrame:
    data = df.copy()
    data[vars] = data[vars].replace(mapping)
    data[vars] = data[vars].apply(pd.to_numeric)

    return data


# This function performs feature engineering and selection for household-level variables
def feature_engineering_hh(df: pd.DataFrame) -> pd.DataFrame:
    # Create dataframe that contains only heads of households
    heads = df.loc[df["parentesco1"] == 1, :].copy()

    # Get the household level variables
    heads = heads[
        config.model_config.id_
        + config.model_config.hh_bool
        + config.model_config.hh_cont
        + config.model_config.hh_ordered
    ]

    # Drop redundant household-level variables
    heads = heads.drop(columns=config.model_config.redundant_household_vars)

    # Create a new variable called hhsize_diff: the difference between
    # household size and number of people living in the household
    heads["hhsize_diff"] = heads["tamviv"] - heads["hhsize"]

    # Create a new ordinal varibale called elec:
    # 0: noelec (no electricity)
    # 1: coopele (from cooperative)
    # 2: public public plant)
    # 3: planpri (private plant)

    conditions = [
        (heads["noelec"] == 1),
        (heads["coopele"] == 1),
        (heads["public"] == 1),
        (heads["planpri"] == 1),
        (
            heads["noelec"]
            != 1
            & (heads["coopele"] != 1)
            & (heads["public"] != 1)
            & (heads["planpri"] != 1)
        ),  # all categories is 0, so we set this to np.nan
    ]

    values = [0, 1, 2, 3, np.nan]
    heads["elec"] = np.select(conditions, values)

    # Create a new "elec_missing" flag
    heads["elec_missing"] = heads["elec"].isnull()

    # Drop redundant elec related variables
    # heads = heads.drop(columns=config.model_config.redundant_elec_vars)

    # Drop area2: house is in a rural zone.
    # This variable is highly correlated to area1,
    # which is a variable that indicates the house is
    # in a urban zone.
    heads = heads.drop(columns="area2")

    # Create new ordinal variables called walls, floor, and roof
    # There are three sets of boolean variables related to the conditions of
    # the walls, roof, and floor of the house (for each household): bad, regular and good
    # We can combine these sets boolean variables into
    # 3 ordinal variables called walls, floor, and roof

    heads["walls"] = np.argmax(
        np.array(heads[["epared1", "epared2", "epared3"]]), axis=1
    )
    heads = heads.drop(columns=["epared1", "epared2", "epared3"])

    # Create roof ordinal variable
    heads["roof"] = np.argmax(
        np.array(heads[["etecho1", "etecho2", "etecho3"]]), axis=1
    )
    heads = heads.drop(columns=["etecho1", "etecho2", "etecho3"])

    # Createa floor ordinal variable
    heads["floor"] = np.argmax(np.array(heads[["eviv1", "eviv2", "eviv3"]]), axis=1)

    heads = heads.drop(columns=["eviv1", "eviv2", "eviv3"])

    # Create a new variable called "house_structure_score"
    # Combine walls, roof, and floor to an overall metric called "house_structure_score"
    # that measures the overall condition of the house for each household.
    heads["house_structure_score"] = heads["walls"] + heads["roof"] + heads["floor"]

    # We will create another house-related variable called "poor_house_condition"
    # Each household will get a point if they have:
    # no toilet
    # no electricity
    # no floor
    # no water service
    # no ceiling

    # Get 1 point each for poor_house_condition if one of the above condition is True
    heads["poor_house_condition"] = (
        heads["sanitario1"]
        + (heads["elec"] == 0)
        + heads["pisonotiene"]
        + heads["abastaguano"]
        + (heads["cielorazo"] == 0)
    )

    # We create another variable called "amenities"
    # A household gets a point each for having a refrigerator, computer, tablet, or TV
    heads["amenities"] = (
        heads["refrig"] + heads["computer"] + (heads["v18q1"] > 0) + heads["television"]
    )

    # Create per capita features
    # We can create additional features by dividing certain number
    # of "household items" (e.g., number of phones, or number of tablets)
    # by the number of people living in the household (tamviv)
    # to get "per_capita_num_phones"
    heads["phones_per_capita"] = heads["qmobilephone"] / heads["tamviv"]
    heads["tablets_per_capita"] = heads["v18q1"] / heads["tamviv"]
    heads["rooms_per_capita"] = heads["rooms"] / heads["tamviv"]
    heads["rent_per_capita"] = heads["v2a1"] / heads["tamviv"]

    return heads


# This function performs feature engineering and selection for individual-level variables
def feature_engineering_ind(df: pd.DataFrame) -> pd.DataFrame:
    # Get data subset with individual-level variables only
    ind = df[
        config.model_config.id_
        + config.model_config.ind_bool
        + config.model_config.ind_ordered
    ].copy()

    # Drop redundant individual level variables
    ind = ind.drop(columns="male")  # have female already

    # Create an ordinal variable for the level of education
    ind["inst"] = np.argmax(
        np.array(ind[[c for c in ind if c.startswith("instl")]]), axis=1
    )

    # Create normalized variables
    ind["escolari_normalized_by_age"] = ind["escolari"] / ind["age"]
    ind["inst_normalized_by_age"] = ind["inst"] / ind["age"]

    # Create a new variable called "tech" that combines v18q (have tablet)
    # and mobilephone (have mobile phone)
    ind["tech"] = ind["v18q"] + ind["mobilephone"]

    return ind


# This is the main function for preprocessing the raw data
# and performing feature engineering and selection
def data_preprocessing(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()

    # Convert  "dependency", "edjefa", "edjefe" from string to numeric after
    # mapping "yes" to 1 and "no" to 0
    df = obj_to_cont(
        vars=["dependency", "edjefa", "edjefe"], df=df, mapping={"yes": 1, "no": 0}
    )

    # Handling missingness in v18q1 (number of tablets) and v2a1 (monthly rent payment)

    # Fill NA with 0
    df["v18q1"] = df["v18q1"].fillna(0)
    df.loc[df["tipovivi1"] == 1, "v2a1"] = 0

    # Handling missingness in rez_esc: years behind school

    # If individual is over 19 or younger than 7 and have NA rez_esc, we set it to 0
    df.loc[
        ((df["age"] > 19) | (df["age"] < 7)) & (df["rez_esc"].isnull()), "rez_esc"
    ] = 0
    # From the variable description, the maximum value
    # for this variable is 5. Therefore, any values above 5
    # should be set to 5
    df.loc[df["rez_esc"] > 5, "rez_esc"] = 5

    # Create missing flags for v2a1 and rez_esc
    df["v2a1_missing"] = df["v2a1"].isnull()
    df["rez_esc_missing"] = df["rez_esc"].isnull()

    # Dropped the squared variables as they are not needed
    df = df.drop(columns=config.model_config.sqr_)

    # Feature engineering and selection for household-level variables
    heads = feature_engineering_hh(df)

    # Feature engineering and selection of individual-level variables
    ind = feature_engineering_ind(df)

    # Aggregating individual-level variables to household-level
    # In order to incorporate the individual data into the household data,
    # we need to aggregate it for each household.
    # The simplest way to do this is to groupby the family id
    # idhogar and then agg the data.
    # The overall strategy is to use a set of aggregation
    # functions for each individual-level variable,
    # and then use model-based feature selection methods
    # to filter the most predictive features

    # Define custom agg function (range)

    # Find the range of the variable
    def range_(x):
        return x.max() - x.min()

    # Groupby idhogar (household id) and apply aggregation functions

    ind_to_drop = ["Id", "Target"]
    ind_agg = (
        ind.drop(columns=ind_to_drop)
        .groupby("idhogar")
        .agg(["min", "max", "sum", "count", "std", range_])
    )

    # Rename the columns
    new_col = []
    for c in ind_agg.columns.levels[0]:
        for stat in ind_agg.columns.levels[1]:
            new_col.append(f"{c}-{stat}")

    ind_agg.columns = new_col

    # Select the aggregated features
    ind_agg = ind_agg.loc[:, config.model_config.selected_ind_agg_features].copy()

    # Merge ind_agg back to the heads dataframe on the household id
    # to get the final interim dataset
    # Note that heads ONLY contains household-level variables,
    # and only contains heads of households only as rows
    # and the ind_agg dataframe contains aggregated
    # rows (each row is a household)
    interim = pd.merge(heads, ind_agg, on="idhogar", how="left")

    return interim

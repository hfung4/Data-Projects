# We will test the functions in the processing/utils module.

import pytest
import numpy as np
import pandas as pd
from survey_analysis.processing.utils import(
parse_num_get_levels,
remove_outlier
)

# Input dataframe for outlier test
@pytest.fixture()
def input_df():
    np.random.seed(1)
    data = pd.DataFrame({"A":np.arange(10000),
                         "B": 5 * np.random.randn(10000) + 50})
    return data


def test_parse_levels_type(input_df_age):
    # convert column "B" to categorical
    parse_num_get_levels(input_df_age,"B")
    # assert
    assert input_df_age["B"].dtype=="category"

def test_parse_levels_min_level(input_df_age):
    # convert column "B" to categorical
    parse_num_get_levels(input_df_age,"B")
    # assert
    assert input_df_age["B"].min()=="17 and under"

def test_parse_levels_max_level(input_df_age):
    # convert column "B" to categorical
    parse_num_get_levels(input_df_age,"B")
    # assert
    assert input_df_age["B"].max()=="80 and over"

def test_remove_outliers(input_df):
    df_res = remove_outlier(df_in = input_df, col="B")
    # assert
    assert df_res.shape[0]==9919




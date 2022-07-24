import re

import numpy as np

from survey_analysis.config.core import config
from survey_analysis.processing.data_manager import clean_reformat_data
from survey_analysis.processing.features import Mapper


# check to see if ALL currencies are USD
def test_clean_data_currency(raw_data):
    data = clean_reformat_data(raw_data)
    assert np.all(data.currency.values == data.currency.values[0])


# check min and max salary values
def test_clean_data_min_max_salary(raw_data):
    data = clean_reformat_data(raw_data)
    assert data.annual_salary.min() >= 5000
    assert data.annual_salary.max() == 195000


# check renamed variables
def test_clean_data_rename_cols(raw_data):
    data = clean_reformat_data(raw_data)
    assert np.all(
        np.isin(
            ["age_category", "overall_experience", "in_field_experience", "education"],
            data.columns.values,
        )
    )


# check state
def test_clean_datastate(raw_data):
    data = clean_reformat_data(raw_data)
    data = data.dropna(subset="state")  # drop all na

    # find elements in the state column that matches (state 1, state 2) pattern
    res = data["state"].apply(lambda x: bool(re.match(r"[A-Za-z]+,\s?[A-Za-z]+", x)))
    assert not res.any()  # all elements are NOT (state 1, state 2)


# Check the "Mapper" transformer (age_category)
def test_mapper_age(raw_data):

    # Init Mapper
    transformer = Mapper(
        variables=config.model_config.AGE_VARS,
        mappings=config.model_config.DICT_AGE_ORDERED_LEVELS,
    )
    # Get raw data
    data = clean_reformat_data(raw_data)
    assert data["age_category"].iat[0] == "25-34"

    # fit and transform data using the mapper
    recoded_age = transformer.fit_transform(data)
    assert recoded_age["age_category"].iat[0] == 2


# Check the "Mapper" transformer (overall_expereince)
def test_mapper_overall_experience(raw_data):

    # Init Mapper
    transformer = Mapper(
        variables=config.model_config.EXPERIENCE_VARS,
        mappings=config.model_config.DICT_EXPERIENCE_ORDERED_LEVELS,
    )
    # Get raw data
    data = clean_reformat_data(raw_data)
    assert data["overall_experience"].iat[0] == "5-7 years"

    # fit and transform data using the mapper
    recoded_overall_experience = transformer.fit_transform(data)
    assert recoded_overall_experience["overall_experience"].iat[0] == 2

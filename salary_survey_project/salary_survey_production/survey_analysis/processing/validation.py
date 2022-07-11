from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from survey_analysis.config.core import config
from survey_analysis.processing.data_manager import clean_reformat_data


def drop_na_inputs(*, input_data: pd.DataFrame) -> pd.DataFrame:
    """Check model inputs for na values and filter."""
    validated_data = input_data.copy()
    # Amongst the selected features in the new dataset, what are
    # the variables that have missing values (but have no missing
    # values in the original train data)
    new_vars_with_na = [
        var
        for var in config.model_config.features
        if var not in config.model_config.CATEGORICAL_VARS_WITH_NA_MISSING
        and validated_data[var].isnull().sum() > 0
    ]
    # The way we deal with these "new" variables in the new/unknown input data
    # with missing value is to drop the rows with missing values.
    validated_data.dropna(subset=new_vars_with_na, inplace=True)

    return validated_data


def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""

    # clean and reformat data
    input_data = clean_reformat_data(input_data, new_input_data=True)
    # get features subset
    relevant_data = input_data[config.model_config.features].copy()

    # drop NA for variables that DO NOT have missing values in train data but have
    # missing values in unknown/new input data
    validated_data = drop_na_inputs(input_data=relevant_data)

    errors = None

    # validate data types in the new data
    try:
        # replace numpy nans so that pydantic can validate
        multiple_survey_data_inputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors


class survey_data_input_schema(BaseModel):
    age_category: Optional[str]
    industry: Optional[str]
    state: Optional[str]
    city: Optional[str]
    overall_experience: Optional[str]
    in_field_experience: Optional[str]
    education: Optional[str]
    gender: Optional[str]
    race: Optional[str]


class multiple_survey_data_inputs(BaseModel):
    inputs: List[survey_data_input_schema]

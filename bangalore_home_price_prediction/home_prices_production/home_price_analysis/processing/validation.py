from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from home_price_analysis.config.core import config
from home_price_analysis.processing.data_manager import preprocess_data


def drop_na_inputs(*, input_data: pd.DataFrame) -> pd.DataFrame:
    """Check model inputs for na values and filter."""
    validated_data = input_data.copy()
    # Amongst the selected features in the new dataset, what are
    # the variables that have missing values (but have no missing
    # values in the original train data)
    new_vars_with_na = [
        var
        for var in config.model_config.FEATURES
        if var not in config.model_config.VARS_WITH_NA_MISSING
        and validated_data[var].isnull().sum() > 0
    ]
    # The way we deal with these "new" variables in the new/unknown input data
    # with missing value is to drop the rows with missing values.
    validated_data.dropna(subset=new_vars_with_na, inplace=True)

    return validated_data


def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""

    # get features subset
    relevant_data = input_data[config.model_config.FEATURES].copy()

    # drop NA for variables that DO NOT have missing values in train data but have
    # missing values in unknown/new input data
    validated_data = drop_na_inputs(input_data=relevant_data)

    errors = None

    # validate data types in the new data
    try:
        # replace numpy nans so that pydantic can validate
        multiple_data_inputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors


class home_price_data_input_schema(BaseModel):
    area_type: Optional[str]
    availability: Optional[str]
    location: Optional[str]
    size: Optional[int]
    total_sqft: Optional[float]
    bath: Optional[int]


class multiple_data_inputs(BaseModel):
    inputs: List[home_price_data_input_schema]

import numpy as np
import pandas as pd

from home_price_analysis import __version__ as _version
from home_price_analysis.config.core import config
from home_price_analysis.processing.data_manager import load_pipeline, preprocess_data
from home_price_analysis.processing.validation import validate_inputs

pipeline_file_name = f"{config.app_config.SAVED_PIPELINE_FILENAME}{_version}.pkl"
# load saved trained pipeline
_price_pipe = load_pipeline(file_name=pipeline_file_name)


def make_prediction(*, input_data: pd.DataFrame, raw_input: bool = True) -> dict:

    """Make a prediction using a saved model pipeline.
    Perform the following for the new/unknown input data (with features only, no price):
       - preprocess data
       - drop NAs for variables that have missing values in new/unknown data but
         no missing values in original train data
       - validate the data type of each selected feature in the new/unknown input data
    """

    # clean and reformat data, do this only if I have raw input data
    # and not data from a form from the UI
    if raw_input:
        pre_processed_data = preprocess_data(input_data)
    else:
        pre_processed_data = input_data

    validated_data, errors = validate_inputs(input_data=pre_processed_data)

    # Init the results dictionary
    results = {"predictions": None, "version": _version, "errors": errors}

    if not errors:
        # Make predictions of the validated data (pass it through salary pipeline for data
        # processing and then predict using the trained model
        predictions = _price_pipe.predict(
            X=validated_data[config.model_config.FEATURES]
        )

        results = {
            # salary predictions in original scale
            "predictions": [np.exp(pred) for pred in predictions],  # type: ignore
            "version": _version,
            "errors": errors,
        }

    return results

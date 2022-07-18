import numpy as np
import pandas as pd

from survey_analysis import __version__ as _version
from survey_analysis.config.core import config
from survey_analysis.processing.data_manager import load_pipeline
from survey_analysis.processing.validation import validate_inputs

pipeline_file_name = f"{config.app_config.saved_pipeline_filename}{_version}.pkl"
# load saved trained pipeline
_salary_pipe = load_pipeline(file_name=pipeline_file_name)


def make_prediction(*, input_data: pd.DataFrame) -> dict:

    """Make a prediction using a saved model pipeline.
    Perform the following for the new/unknown input data (with features only, no salary):
       - clean and reformat data
       - drop NAs for variables that have missing values in new/unknown data but
         no missing values in original train data
       - validate the data type of each selected feature in the new/unknown input data
    """
    validated_data, errors = validate_inputs(input_data=input_data)

    # Init the results dictionary
    results = {"predictions": None, "version": _version, "errors": errors}

    if not errors:
        # Make predictions of the validated data (pass it through salary pipeline for data
        # processing and then predict using the trained model
        predictions = _salary_pipe.predict(
            X=validated_data[config.model_config.features]
        )

        results = {
            # salary predictions in original scale
            "predictions": [np.exp(pred) for pred in predictions],  # type: ignore
            "version": _version,
            "errors": errors,
        }

    return results

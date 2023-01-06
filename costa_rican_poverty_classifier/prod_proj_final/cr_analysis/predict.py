import numpy as np
import pandas as pd

from cr_analysis import __version__ as _version
from cr_analysis.config.core import config
from cr_analysis.processing import preprocessing
from cr_analysis.processing.data_manager import load_pipeline

pipeline_file_name = f"{config.app_config.saved_pipeline_filename}{_version}.pkl"
# load saved trained pipeline
_costa_rica_data_pipe = load_pipeline(file_name=pipeline_file_name)


def make_prediction(*, input_data: pd.DataFrame, is_raw_data: bool = True) -> dict:

    """Make a prediction using a saved model pipeline.
    Perform the following for the new/unknown input data:
       - clean and wrange data with preprocessing functions
       - Make predictions using the persisted data pipeline
    """

    # The input data is raw and unlabeled data.
    # I need to preprocess it to get the interim data
    # before inputting to the fitted data pipeline
    if is_raw_data:
        print("Preprocessing raw data")
        # I need to insert a column called "Target" that only contains
        # NA so the preprocessing functions can parse
        input_data["Target"] = np.nan
        interim = preprocessing.data_preprocessing(input_data)
    else:
        # I am directly using interim data (already preprocessed)
        interim = input_data

    # save IDs
    test_ids = interim.loc[:, ["Id", "idhogar"]]

    # drop IDs
    data = interim.drop(["Id", "idhogar", "Target"], axis="columns")

    # Make predictions on the preprocessed data
    # (pass it through the data pipeline for data
    # processing and then predict using the trained model
    predictions = _costa_rica_data_pipe.predict(X=data)

    results = {
        # class predictions
        "predictions": predictions,  # type: ignore
        "version": _version,
        "test_ids": test_ids,
    }

    return results

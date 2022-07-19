import os
import typing as t
from pathlib import Path

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from home_price_analysis import __version__ as _version
from home_price_analysis.config.core import RAW_DATA_DIR, TRAINED_MODEL_DIR, config
from home_price_analysis.processing.utils import (
    chain,
    fct_lump_location,
    filter_bath_bedroom,
    filter_price_per_sqft,
    preprocessing_area_type,
    preprocessing_size,
    preprocessing_total_sqft,
)


# This function load the raw dataset
def load_dataset(*, file_name: str) -> pd.DataFrame:
    """
    load_dataset: this function loads the raw data

    Args:
        file_name(str): path the the raw data

    Returns:
        data(pd.DataFrame): raw dataframe
    """
    # If raw data directory does not exist, I will make one
    if not os.path.isdir(RAW_DATA_DIR):
        os.makedirs(RAW_DATA_DIR)

    # Import raw data
    try:
        data = pd.read_csv(Path(RAW_DATA_DIR, file_name))
    except ImportError:
        "Failed to import raw training data file."

    return data


def save_pipeline(*, pipeline_to_persist: object) -> object:
    """Persist the pipeline.x
    Saves the versioned model, and overwrites any previous
    saved models. This ensures that when the package is
    published, there is only one trained model that can be
    called, and we know exactly how it was built.
    """

    # Prepare versioned save file name
    save_file_name = f"{config.app_config.SAVED_PIPELINE_FILENAME}{_version}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name

    # remove all files in TRAINED_MODEL_DIR and replace any existing .pkl with
    # same name as current version of the pipeline so that we have only a single model
    # in our package.
    remove_old_pipelines(files_to_keep=[save_file_name])
    # persist model
    joblib.dump(pipeline_to_persist, save_path)

    return None


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function preprocesses the size and total_sqft columns (invovles dropping NA
    and removing outliers, so it is difficult to include in sklearn pipeline)
    This function will be applied on the train and test set from ShuffleSplit() separately

    Args:
        df (pd.DataFrame): input datafraome

    Returns:
        res (pd.DataFrame): output dataframe
    """
    data = df.copy()

    res = chain(
        data,
        preprocessing_size,
        preprocessing_total_sqft,
        preprocessing_area_type,
        fct_lump_location,
        filter_bath_bedroom,
        filter_price_per_sqft,
    )

    return res


def remove_old_pipelines(*, files_to_keep: t.List[str]) -> None:
    """
    Remove old model pipelines.
    This is to ensure there is a simple one-to-one
    mapping between the package version and the model
    version to be imported and used by other applications.
    """
    do_not_delete = files_to_keep + ["__init__.py"]

    for model_file in TRAINED_MODEL_DIR.iterdir():
        if model_file.name not in do_not_delete:
            # remove file
            model_file.unlink()


def load_pipeline(*, file_name: str) -> Pipeline:
    """Load a persisted pipeline."""

    file_path = TRAINED_MODEL_DIR / file_name
    trained_model = joblib.load(filename=file_path)
    return trained_model

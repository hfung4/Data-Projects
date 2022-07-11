import typing as t
from pathlib import Path

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from survey_analysis import __version__ as _version
from survey_analysis.config.core import RAW_DATA_DIR, TRAINED_MODEL_DIR, config
from survey_analysis.processing.utils import parse_num_get_levels, remove_outlier


# This function load the raw dataset
def load_dataset(*, file_name: str) -> pd.DataFrame:
    """
    load_dataset: this function loads the raw data

    Args:
        file_name(str): path the the raw data

    Returns:
        dataframe(pd.DataFrame): raw dataframe
    """
    return pd.read_csv(Path(RAW_DATA_DIR, file_name))


def clean_reformat_data(
    raw: pd.DataFrame, new_input_data: bool = False
) -> pd.DataFrame:
    """
    clean_reformat_data: this function perform data cleaning
    and reformating-- steps that could be
    done outside of data pipeline (wouldn't lead to data leakage)

    Args:
        raw(pd.DataFrame): raw dataframe
        new_input(bool): if input data is a new/unknown dataset
        with no salary column, then True

    Returns:
        transformed(pd.DataFrame): processed dataframe

    """

    # We will only focus on respondents (>83% of them) that are paid in USD
    transformed = raw.loc[raw["currency"] == "USD"].copy()

    # Convert timestamp to datetime
    transformed.loc[:, "timestamp"] = transformed.loc[:, "timestamp"].astype(
        "datetime64[ns]"
    )

    # state
    # Only take the first state in the response and ignore the rest
    transformed["state"] = transformed["state"].str.split(",").str[0]

    # overall_years_of_professional_experience
    transformed["overall_years_of_professional_experience"] = transformed[
        "overall_years_of_professional_experience"
    ].str.replace(" - ", "-")

    # cast overall_years_of_professional_experience as an ordered categorical variable
    parse_num_get_levels(transformed, "overall_years_of_professional_experience")

    # years_of_experience_in_field
    transformed["years_of_experience_in_field"] = transformed[
        "years_of_experience_in_field"
    ].str.replace(" - ", "-")

    # cast years_of_experience_in_field as an ordered categorical variable
    parse_num_get_levels(transformed, "years_of_experience_in_field")

    # age

    # Need to rename the "under 18" level to "17 or under" so it can be
    # parsed by the parse_num_get_levels() function
    transformed["how_old_are_you"] = transformed["how_old_are_you"].replace(
        to_replace="under 18", value="17 or under"
    )

    # cast how_old_are_you as an ordered categorical variable
    parse_num_get_levels(transformed, "how_old_are_you")

    # rename variables
    transformed = transformed.rename(
        columns={
            "how_old_are_you": "age_category",
            "overall_years_of_professional_experience": "overall_experience",
            "years_of_experience_in_field": "in_field_experience",
            "highest_level_of_education_completed": "education",
        },
        errors="raise",
    )

    # Remove outliers (annual salary)
    # We will not run this function if the dataset (new/unknown)
    # does not have the dependent variable-- "annual_salary"
    if not new_input_data:
        transformed = remove_outlier(
            df_in=transformed,
            col="annual_salary",
            lwr_bound=config.model_config.OUTLIER_LWR_BOUND,
        )

    return transformed


def save_pipeline(*, pipeline_to_persist: object) -> object:
    """Persist the pipeline.x
    Saves the versioned model, and overwrites any previous
    saved models. This ensures that when the package is
    published, there is only one trained model that can be
    called, and we know exactly how it was built.
    """

    # Prepare versioned save file name
    save_file_name = f"{config.app_config.saved_pipeline_filename}{_version}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name

    # remove all files in TRAINED_MODEL_DIR and replace any existing .pkl with
    # same name as current version of the pipeline so that we have only a single model
    # in our package.
    remove_old_pipelines(files_to_keep=[save_file_name])
    # persist model
    joblib.dump(pipeline_to_persist, save_path)

    return None


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

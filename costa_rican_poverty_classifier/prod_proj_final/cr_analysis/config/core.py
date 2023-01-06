from pathlib import Path
from typing import Dict, List

from pydantic import BaseModel
from strictyaml import YAML, load

import cr_analysis

# Project Directories
PACKAGE_ROOT = Path(cr_analysis.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "config.yml"
RAW_DATA_DIR = PACKAGE_ROOT / "datasets/raw"
INTERIM_DATA_DIR = PACKAGE_ROOT / "datasets/interim"
PROCESSED_DATA_DIR = PACKAGE_ROOT / "datasets/processed"
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained_models"
OUTPUTS_DIR = PACKAGE_ROOT / "outputs"
PIPELINE_DEBUG_DIR = PACKAGE_ROOT / "datasets/debug"


class AppConfig(BaseModel):
    """
    Application-level config.
    """

    package_name: str
    train_data_file: str
    test_data_file: str
    interim_data_file: str
    saved_pipeline_filename: str
    DEBUG_PIPELINE: bool


class ModelConfig(BaseModel):
    """
    All configuration relevant to model
    training and feature engineering.
    """

    # general
    DV: str
    POVERTY_MAPPING: Dict[int, str]
    TEST_SIZE: float
    NFOLDS: int
    RANDOM_STATE: int
    SCORING: str
    TOP_N_FEATURE_IMPORTANCE: int

    # Variable categories
    id_: List[str]
    ind_bool: List[str]
    ind_ordered: List[str]
    hh_bool: List[str]
    hh_ordered: List[str]
    hh_cont: List[str]
    sqr_: List[str]
    redundant_household_vars: List[str]
    redundant_elec_vars: List[str]
    selected_ind_agg_features: List[str]

    # hyperparameters
    IMPUTATION_METHOD: str
    DROP_NZV_TOL: float
    # OVERSAMPLING_STRATEGY: Dict[int, int]
    # UNDERSAMPLING_STRATEGY: Dict[int, int]
    FEATURE_SEL_MODEL_N_ESTIMATORS: int

    CLF__N_ESTIMATORS: int
    CLF__MAX_DEPTH: int
    CLF__MIN_SAMPLES_SPLIT: int
    CLF__MIN_SAMPLES_LEAF: int

    SAVED_COL_NAME_FILE: str


class Config(BaseModel):
    """Master config object."""

    app_config: AppConfig
    model_config: ModelConfig


# Functions ------------------------------------------------------


def find_config_file() -> Path:
    """Locate the configuration file."""
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f"Config not found at {CONFIG_FILE_PATH!r}")


def fetch_config_from_yaml(cfg_path=None) -> YAML:
    """Parse YAML containing the package configuration."""

    if not cfg_path:
        cfg_path = find_config_file()

    if cfg_path:
        with open(cfg_path, "r") as conf_file:
            parsed_config = load(
                conf_file.read()
            )  # use the load function from strictyaml
            return parsed_config
    raise OSError(f"Did not find config file at path: {cfg_path}")


def create_and_validate_config(parsed_config: YAML = None) -> Config:
    """Run validation on config values."""
    if parsed_config is None:
        parsed_config = fetch_config_from_yaml()

    # specify the data attribute from the strictyaml YAML type.
    _config = Config(
        app_config=AppConfig(**parsed_config.data),
        model_config=ModelConfig(**parsed_config.data),
    )

    return _config


config = create_and_validate_config()

from pathlib import Path
from typing import List

from pydantic import BaseModel
from strictyaml import YAML, load

import home_price_analysis

# Project Directories
PACKAGE_ROOT = Path(home_price_analysis.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "config.yml"
RAW_DATA_DIR = PACKAGE_ROOT / "datasets/raw"
PROCESSED_DATA_DIR = PACKAGE_ROOT / "datasets/processed"
TEST_DATA_DIR = PACKAGE_ROOT / "datasets/test"
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained_models"
FIGURES_DIR = PACKAGE_ROOT / "figures"


class AppConfig(BaseModel):
    """
    Application-level config.
    """

    PACKAGE_NAME: str
    RAW_DATA_FILE: str
    TEST_DATA_FILE: str
    SAVED_PIPELINE_FILENAME: str
    MODEL_PERF_PLOT_NAME: str


class ModelConfig(BaseModel):
    """
    All configuration relevant to model
    training and feature engineering.
    """

    # general
    OUTCOME_VARIABLE: str
    FEATURES: List[str]
    TEST_SIZE: float
    RANDOM_STATE: int

    # hyperparameters for gradient boosted tree

    # data processing and feature engineering
    AREA_TYPE_RETAIN: int
    SQFT_PER_SQ_METER: float
    SQFT_PER_SQ_YARD: float
    VARS_MISSING_IMPUTED: List[str]
    VARS_WITH_NA_MISSING: List[str]
    NOMINAL_VARS: List[str]
    CONTINUOUS_VARS: List[str]

    # model hyperparamters
    COLSAMPLE_BYTREE: float
    MAX_DEPTH: int
    SUBSAMPLE: float
    N_ESTIMATORS: int
    GAMMA: float
    LEARNING_RATE: float


class Config(BaseModel):
    """Master config object."""

    app_config: AppConfig
    model_config: ModelConfig


def find_config_file() -> Path:
    """Locate the configuration file."""
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f"Config not found at {CONFIG_FILE_PATH!r}")


def fetch_config_from_yaml(cfg_path: Path = None) -> YAML:
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

from pathlib import Path
from typing import Dict, List, Sequence, Union

from pydantic import BaseModel
from strictyaml import YAML, load

import tb_analysis

# Project Directories
PACKAGE_ROOT = Path(tb_analysis.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "config.yml"
DATA_DIR = ROOT/ "data"
IMAGES_DIR = ROOT/"outputs/figures"
TRAINED_MODEL_DIR = ROOT/"outputs/trained_models"

class AppConfig(BaseModel):
    """
    Application-level config.
    """

    data_file: str
    dict_file: str


class ModelConfig(BaseModel):
    """
    All configuration relevant to model
    training and feature engineering.
    """
    proto_cluster: Dict
    prototypes: List[str]
    clustering_inputs: Dict[str,List[str]]
    selected_features: List[str]

    num_feature_importance: int

    pouch_dt_params: Dict[str,Union[int,float]]
    box_dt_params: Dict[str,Union[int,float]]
    sachet_dt_params: Dict[str,Union[int,float]]
    merm_dt_params: Dict[str,Union[int,float]]

    test_size: float
    random_state: int


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
            parsed_config = load(conf_file.read()) # use the strictyaml.load()
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

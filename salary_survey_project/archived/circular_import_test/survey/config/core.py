from pathlib import Path
from typing import Dict, List, Sequence

from pydantic import BaseModel
from strictyaml import YAML, load

import survey

# Project Directories
PACKAGE_ROOT = Path(survey.__file__).absolute().parent
ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "config.yml"
RAW_DATASET_DIR = PACKAGE_ROOT / "datasets/raw"
RAW_DATASET_DIR = PACKAGE_ROOT / "datasets/processed"
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained_models"

# If I comment out #from survey.config.core import PACKAGE_ROOT
# in survey/__init__.py, then I can print out survey.num_of_houses
# otherwise, I will get circular import error
# However, survey.__file__ can be accessed in this file for all cases (with our without the
# PACKAGE_ROOT import in __init.py.
print(survey.num_of_houses)
print(survey.__file__)
#print(survey.__versions__)
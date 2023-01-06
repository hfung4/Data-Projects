# src/config.py
# Data path names and read yaml config

from pathlib import Path
import src
import yaml


# Project directories
PACKAGE_ROOT = Path(src.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = Path(PACKAGE_ROOT, "config.yml")
RAW_DATA_DIR = Path(ROOT, "data")
INTERIM_DATA_DIR = Path(ROOT, "data", "interim")
PROCESSED_DATA_DIR = Path(ROOT, "data", "processed")
OUTPUT_DIR = Path(ROOT, "outputs")
MODEL_DIR = Path(ROOT, "models")

# Read config yaml
conf = yaml.safe_load(CONFIG_FILE_PATH.read_text())

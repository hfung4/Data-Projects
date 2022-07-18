import re

import numpy as np

from home_price_analysis.config.core import config
from home_price_analysis.processing.utils import (
    preprocessing_area_type,
    preprocessing_size,
    preprocessing_total_sqft,
)

# from home_price_analysis.processing.features import Mapper


def test_preprocessing_total_sqft(train_set):
    data = preprocessing_total_sqft(train_set)
    assert data["total_sqft"].dtype == float
    assert data["total_sqft"].isnull().sum() == 0
    assert data["total_sqft"].max() < 3000


def test_preprocessing_size(train_set):
    data = preprocessing_size(train_set)
    assert data["size"].dtype == int
    assert data["size"].isnull().sum() == 0
    assert data["size"].max() < 30


def test_preprocessing_area_type(train_set):
    data = preprocessing_area_type(train_set)
    assert data["area_type"].dtype == "O"
    assert data["area_type"].value_counts().index[0] == "Super_built_up_Area"
    assert data["area_type"].value_counts().index[1] == "Built_up_Area"

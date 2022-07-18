import re

import numpy as np

from home_price_analysis.config.core import config
from home_price_analysis.processing.features import area_type_step, avail_step


# Test the area_type transformer
def test_area_type_step(train_set):

    # Get features and outcome variable
    X = train_set[config.model_config.FEATURES]
    y = train_set[config.model_config.OUTCOME_VARIABLE]

    # Init transformer
    tf = area_type_step()
    processed = tf.fit_transform(X, y)

    # only 3 levels
    assert len(processed["area_type"].value_counts().index) == 3
    assert processed["area_type"].value_counts().index[2] == "Other"


# Test the avail transformer
def test_avail_step(train_set):

    # Get features and outcome variable
    X = train_set[config.model_config.FEATURES]
    y = train_set[config.model_config.OUTCOME_VARIABLE]

    # Init transformer
    tf = avail_step()
    processed = tf.fit_transform(X, y)

    assert len(processed["availability"].value_counts().index) == 2  # only 2 levels
    assert processed["availability"].value_counts().index[0] == "ready_to_move"
    assert processed["availability"].value_counts().index[1] == "not_ready_to_move"

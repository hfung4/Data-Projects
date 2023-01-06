from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from cr_analysis.config.core import RAW_DATA_DIR, config


@pytest.fixture()
def get_test_data():
    # load test data
    return pd.read_csv(Path(RAW_DATA_DIR, config.app_config.test_data_file))


@pytest.fixture()
def get_raw_data():
    # rbind train and test data

    # load train data
    train = pd.read_csv(Path(RAW_DATA_DIR, config.app_config.train_data_file))
    # load test data
    test = pd.read_csv(Path(RAW_DATA_DIR, config.app_config.test_data_file))
    # row concat raw_train and raw_test
    test["Target"] = np.nan
    raw = pd.concat([train, test], ignore_index=True, axis="index")
    return raw

from pathlib import Path

import pandas as pd
import pytest
from sklearn.model_selection import ShuffleSplit

from home_price_analysis.config.core import TEST_DATA_DIR, config
from home_price_analysis.processing.data_manager import load_dataset


@pytest.fixture
def input_df_age():
    df_age = pd.DataFrame(
        {
            "A": [1, 2, 3, 4, 5],
            "B": ["18-35", "60-79", "36-59", "80 and over", "17 and under"],
        }
    )
    return df_age


@pytest.fixture()
def train_set():

    # load raw data
    raw = load_dataset(file_name=config.app_config.RAW_DATA_FILE)

    # Test train split
    # init the split object
    split = ShuffleSplit(
        n_splits=1,
        test_size=config.model_config.TEST_SIZE,
        random_state=config.model_config.RANDOM_STATE,
    )

    # Only 1 fold was done since set "n_splits" to 1.
    # We shuffle the overall dataset, and then draw 0.8 of the sample to the train set and 0.2 to the test set
    for train_index, _test_index in split.split(X=raw):
        # We only have one set of train and test index since we only have 1 fold
        train_set = raw.loc[train_index]

    return train_set


@pytest.fixture()
def test_data():
    # load test data
    return pd.read_csv(Path(TEST_DATA_DIR, config.app_config.TEST_DATA_FILE))

import pytest
import pandas as pd
from pathlib import Path
from survey_analysis.processing.data_manager import (
load_dataset
)
from survey_analysis.config.core import config, TEST_DATA_DIR


@pytest.fixture
def input_df_age():
    df_age= pd.DataFrame({"A": [1, 2, 3, 4, 5],
                          "B": ["18-35",
                                "60-79",
                                "36-59",
                                "80 and over",
                                "17 and under"]})
    return df_age


@pytest.fixture()
def raw_data():
    # load raw data
    return load_dataset(file_name=config.app_config.training_data_file)


@pytest.fixture()
def test_data():
    # load test data
    return pd.read_csv(Path(TEST_DATA_DIR,config.app_config.test_data_file))


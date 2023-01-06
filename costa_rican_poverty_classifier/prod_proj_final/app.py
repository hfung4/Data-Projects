from cr_analysis.predict import make_prediction
from pathlib import Path
from cr_analysis.config.core import config, RAW_DATA_DIR
import pandas as pd


if __name__ == "__main__":
    test_data = pd.read_csv(Path(RAW_DATA_DIR, config.app_config.test_data_file))
    make_prediction(input_data=test_data, is_raw_data=True)

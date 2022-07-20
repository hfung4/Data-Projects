from pathlib import Path
import pandas as pd
from home_price_analysis.config.core import TEST_DATA_DIR
from home_price_analysis.predict import make_prediction
from warnings import simplefilter

simplefilter(action="ignore", category=pd.errors.PerformanceWarning)


def main():
    # load pre-processed X from flat file
    X_preprocessed = pd.read_csv(Path("tests", "preprocessed.csv"))

    # Get input data from "form"
    area_type = "Super_built_up_Area"
    availability = "Not Ready to Move"
    location = "Devarachikkanahalli"
    size = 3
    total_sqft = 1250
    bath = 2

    d_input_data = {
        "area_type": [area_type],
        "availability": [availability],
        "location": [location],
        "size": [size],
        "total_sqft": [total_sqft],
        "bath": [bath],
    }

    df_input_data = pd.DataFrame.from_dict(d_input_data)

    result = make_prediction(input_data=df_input_data, raw_input=False)
    print(result["predictions"])


if __name__ == "__main__":
    main()

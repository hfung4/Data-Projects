import pandas as pd
from home_price_analysis.predict import make_prediction
from warnings import simplefilter

simplefilter(action="ignore", category=pd.errors.PerformanceWarning)


def predict(
    area_type: str,
    availability: str,
    location: str,
    size: int,
    total_sqft: float,
    bath: int,
) -> float:
    # Put input data to a dictionary
    d_input_data = {
        "area_type": [area_type],
        "availability": [availability],
        "location": [location],
        "size": [size],
        "total_sqft": [total_sqft],
        "bath": [bath],
    }
    # convert data dictionary to a pd.DataFrame with 1 row
    df_input_data = pd.DataFrame.from_dict(d_input_data)

    # Use ML model to get predicted home price
    # result is a dictionary of predicted price, error, and model version
    result = make_prediction(input_data=df_input_data, raw_input=False)

    return result["predictions"]

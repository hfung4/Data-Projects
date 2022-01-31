# common libraries
import pandas as pd

# type checking
from typing import Union,Dict

# sklearn
from sklearn.model_selection import train_test_split

from tb_analysis.config.core import config


########## Helper functions for preprocessing ##########

def process_prototype_preference(data: pd.DataFrame,
                                 p: str) -> pd.DataFrame:
    """
    This function performs processing (drop missing values, recasting of data types
    for the input variables that were used for clustering (feature preference for each prototype)
    Args:
        df (pd.DataFrame): input dataframe
        p (str): prototype name

    Returns:
        df (pd.DataFrame): output dataframe
    """

    # features and outcome variable
    features = config.model_config.clustering_inputs[p]
    dep_var = config.model_config.proto_cluster[p]

    # Get the columns that I need
    df = data.filter(items=features + [dep_var])

    # Remove rows with missing values
    df.dropna(inplace=True)

    # Get all float vars, and convert them to integer
    float_vars = [var for var in df.columns if df[var].dtype == "float64"]
    df[float_vars] = df[float_vars].astype("int64")

    return df


def test_harness(processed_dict: Dict[str,pd.DataFrame],
                 p: str) -> Dict[str, Union[pd.DataFrame, pd.Series]]:
    """
    This function is a wrapper for test-train split
    Args:
        processed_dict (Dict): a dictionarty of processed data for each prototype
        p (str): prototype name

    Returns:
        df (Dict): a dictionary of train and test data: X_train, X_test, y_train, and y_test
    """

    # make a copy of the processed data
    df_dict = processed_dict.copy()

    # Name of the outcome variable (cluster assignment for each prototype)
    outcome_var = p.lower() + '_ratenw'

    # Features dataframe
    X = df_dict[p].drop([outcome_var], axis=1)

    # Outcome variable
    y = processed_dict[p][outcome_var]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        random_state=config.model_config.random_state,
                                                        test_size=config.model_config.test_size)
    # Output
    return {"X_train": X_train, "X_test": X_test, "y_train": y_train, "y_test": y_test}

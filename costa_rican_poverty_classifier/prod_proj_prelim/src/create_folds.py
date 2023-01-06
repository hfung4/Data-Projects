# src/create_folds.py
import pandas as pd
from sklearn import model_selection
from pathlib import Path

# Custom modules
import src.config as config
from src.config import conf


def create_folds(df: pd.DataFrame) -> pd.DataFrame:
    """create_folds: segment train set into N folds, each with the same class distribution as
    the enture train set. Each fold is given a numeric label.

    Args:
        df (pd.DataFrame): train dataset

    Returns:
        pd.DataFrame: output train dataset with fold column that denotes each row to a fold
    """

    data = df.copy()  # make a copy of input dataframe

    # we create a new column called kfold and init it with -1
    data["kfold"] = -1

    # The next step is to shuffle the rows of the data
    # I comment the below code since shuffling is now done in StratifiedKFold()
    # data = data.sample(frac=1).reset_index(drop=True)

    # Initiate the StratifiedKFold class from model_selection module
    # Note that if label is continuous, we need to bin the label
    # since StratifiedKFold only applies to classification problems
    # Alternatively, use KFold for regression problems
    kf = model_selection.StratifiedKFold(
        n_splits=conf["NFOLDS"], shuffle=True, random_state=conf["RANDOM_STATE"]
    )

    # Fill the new KFold column
    for f, (t_, v_) in enumerate(kf.split(X=data, y=data.loc[:, conf["DV"]])):

        # v_is the val indices for each fold.
        # Populate the kfold column
        data.loc[v_, "kfold"] = f

        # Save data with the fold column as a pickle file to preserve data type
        data.to_pickle(Path(config.INTERIM_DATA_DIR, "interim_folds.pkl"))

    return data

# common libraries
import pandas as pd
# type checking
from typing import Dict
# sklearn
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
# config
from tb_analysis.config.core import config, TRAINED_MODEL_DIR
from tb_analysis import __version__ as _version
# persist model
import joblib

def gs_fit(train_test_dict: Dict,
            p: str,
            param_grid: Dict,
            scoring: str,
            cv: int,
            min_samples_leaf: int = 1,
            pruning_level : float = 0):
    """
   This is a wrapper function that performs decision tree training and optimization
    Args:
        train_test_dict(dict): input dictionary of train and test dataframe
        p(str): prototype
        param_grid (str): a grid of parameters to search
        scoring (str): performance metric of GridSearch CV
        cv: number of cross validation folds
        min_samples_leaf: min number of samples in a left
        pruning_level: pruning level (penalty term for model complexity)

    Returns:
        grid_search.best_estimator_: best estimator from GridSearchCV
    """

    # Get the train test data for the prototype
    train_test_data = train_test_dict[p]

    # Instantiate the grid search model
    grid_search = GridSearchCV(
        estimator=DecisionTreeClassifier(random_state=config.model_config.random_state,
                                         min_samples_leaf=min_samples_leaf,
                                         ccp_alpha = pruning_level),
        param_grid=param_grid,
        scoring=scoring,
        cv=cv,
        n_jobs=-1,  # n_jobs = -1 means use all processors
        verbose=1)  # show the process

    # Fit the grid search to the data
    grid_search.fit(train_test_data["X_train"], train_test_data["y_train"])

    print(f"*********The model has succesfully been fitted! *********")

    # persist model
    save_file_name = f"{p}_clf_gs_model_{_version}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name
    joblib.dump(grid_search, save_path)

    return grid_search





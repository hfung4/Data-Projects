"""
This module performs train test split, train the gradient
boosted tree model and persist the pipeline
"""
from warnings import simplefilter

import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import ShuffleSplit

from home_price_analysis.config.core import config
from home_price_analysis.pipeline import price_pipeline
from home_price_analysis.processing.data_manager import (
    load_dataset,
    preprocess_data,
    save_pipeline,
)
from home_price_analysis.processing.plotting import comparison_plot

simplefilter(action="ignore", category=pd.errors.PerformanceWarning)


def run_training():

    # import raw data
    raw = load_dataset(file_name=config.app_config.RAW_DATA_FILE)

    # preprocess the data
    pre_processed = preprocess_data(raw)

    # Test train split
    # init the split object
    split = ShuffleSplit(
        n_splits=1,
        test_size=config.model_config.TEST_SIZE,
        random_state=config.model_config.RANDOM_STATE,
    )

    # Only 1 fold was done since set "n_splits" to 1.
    # We shuffle the overall dataset, and then draw 0.8
    # of the sample to the train set and 0.2 to the test set
    for train_index, test_index in split.split(X=pre_processed):
        # We only have one set of train and test index since we only have 1 fold
        train_set = pre_processed.loc[train_index]
        test_set = pre_processed.loc[test_index]

    #!! Now we do preprocessing before split !!#
    # Perform data preprocessing for size and total_sqft
    # separately for the train and test set
    # train_set = preprocess_data(train_set)
    # test_set = preprocess_data(test_set)

    # separate out the features dataframe and outcome series
    X_train = train_set[config.model_config.FEATURES]
    X_test = test_set[config.model_config.FEATURES]
    # log transform the outcome variable
    y_train = np.log(train_set[config.model_config.OUTCOME_VARIABLE])
    y_test = np.log(test_set[config.model_config.OUTCOME_VARIABLE])

    # fit baseline model
    dummy_regr = DummyRegressor(strategy="median")
    dummy_regr.fit(X_train, y_train)

    # Get baseline performance
    y_pred_baseline = dummy_regr.predict(X_test)
    baseline_rmse = round(mean_squared_error(y_test, y_pred_baseline, squared=False), 2)
    baseline_r2 = round(r2_score(y_test, y_pred_baseline), 2)

    # fit pipeline
    price_pipeline.fit(X_train, y_train)

    # Get the test rmse and R2 score
    # (from validation set approach) of trained pipeline
    y_pred_xgb = price_pipeline.predict(X_test)
    xgb_rmse = round(mean_squared_error(y_test, y_pred_xgb, squared=False), 2)
    xgb_r2 = round(r2_score(y_test, y_pred_xgb), 2)

    # evaluate performance of model and generate a summary of performance
    comparison_plot(
        pipeline_metric=xgb_rmse, baseline_metric=baseline_rmse, metric_name="rmse"
    )
    comparison_plot(
        pipeline_metric=xgb_r2, baseline_metric=baseline_r2, metric_name="r2"
    )

    # Persist the trained pipeline
    save_pipeline(pipeline_to_persist=price_pipeline)


if __name__ == "__main__":
    run_training()

"""
This module performs train test split, train the gradient
boosted tree model and persist the pipeline
"""

import numpy as np
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

from survey_analysis.config.core import config
from survey_analysis.pipeline import salary_pipeline
from survey_analysis.processing.data_manager import (
    clean_reformat_data,
    load_dataset,
    save_pipeline,
)
from survey_analysis.processing.plotting import comparison_plot


def run_training():

    # import raw data
    raw = load_dataset(file_name=config.app_config.training_data_file)

    # clean and format data
    data = clean_reformat_data(raw)

    # Test train split
    X_train, X_test, y_train, y_test = train_test_split(
        data[config.model_config.features],  # features
        data[config.model_config.target],  # target
        test_size=config.model_config.TEST_SIZE,
        random_state=config.model_config.RANDOM_STATE,
    )

    # log transform the dependent variable
    y_train = np.log(y_train)
    y_test = np.log(y_test)

    # fit baseline model
    dummy_regr = DummyRegressor(strategy="median")
    dummy_regr.fit(X_train, y_train)

    # Get baseline performance
    y_pred_baseline = dummy_regr.predict(X_test)
    baseline_rmse = round(mean_squared_error(y_test, y_pred_baseline, squared=False), 2)

    # fit pipeline
    salary_pipeline.fit(X_train, y_train)

    # Get the test rmse (from validation set approach) of trained pipeline
    y_pred_gb = salary_pipeline.predict(X_test)
    gb_rmse = round(mean_squared_error(y_test, y_pred_gb, squared=False), 2)

    # evaluate performance of model and generate a summary of performance
    comparison_plot(pipeline_metric=gb_rmse, baseline_metric=baseline_rmse)

    # Persist the trained pipeline
    save_pipeline(pipeline_to_persist=salary_pipeline)


if __name__ == "__main__":
    run_training()

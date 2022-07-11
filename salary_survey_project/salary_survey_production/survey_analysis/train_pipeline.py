# This module performs train test split, train the gradient boosted tree model and persist the pipeline

import numpy as np
from survey_analysis.config.core import config
from survey_analysis.processing.data_manager import save_pipeline
from survey_analysis.evaluate_pipeline import comparison_plot
from survey_analysis.pipeline import salary_pipeline
from survey_analysis.processing.data_manager import (
    load_dataset,
    clean_reformat_data
)
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyRegressor



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
        random_state=config.model_config.RANDOM_STATE
    )

    # log transform the dependent variable
    y_train = np.log(y_train)
    y_test = np.log(y_test)

    # fit baseline model
    dummy_regr = DummyRegressor(strategy="median")
    dummy_regr.fit(X_train, y_train)

    # fit pipeline
    salary_pipeline.fit(X_train,y_train)

    # evaluate performance of model and generate a summary of performance
    comparison_plot(pipeline_to_evaluate=salary_pipeline,
                    baseline_model = dummy_regr,
                    X_test = X_test,
                    y_test= y_test)

    # Persist the trained pipeline
    save_pipeline(pipeline_to_persist=salary_pipeline)


if __name__ == "__main__":
    run_training()
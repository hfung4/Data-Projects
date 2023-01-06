"""
This module takes raw data, process it, split data
into train and validation sets, and peform imputation,up- and down-sampling,
feature selection, scaling, and modeling
with a tuned data pipeline (parameters are given in config.yml).
"""

from collections import OrderedDict
from pathlib import Path

import numpy as np
import pandas as pd

import cr_analysis.evaluate as eval
import cr_analysis.predict as predict
from cr_analysis.config.core import INTERIM_DATA_DIR, OUTPUTS_DIR, config
from cr_analysis.pipeline import data_pipeline, data_pipeline_debug
from cr_analysis.processing import preprocessing
from cr_analysis.processing.data_manager import create_dirs, load_dataset, save_pipeline


def run_training():

    # create directories
    create_dirs()

    # import raw data
    raw_train, raw_test = load_dataset(data_type="raw")
    # row concat raw_train and raw_test
    raw_test["Target"] = np.nan
    raw = pd.concat([raw_train, raw_test], ignore_index=True, axis="index")

    # clean and format data
    data = preprocessing.data_preprocessing(raw)

    # Save the interim data
    data.to_pickle(Path(INTERIM_DATA_DIR, config.app_config.interim_data_file))

    # Get poverty mapping dictionary
    poverty_mapping = config.model_config.POVERTY_MAPPING

    # Convert to ordered dict
    poverty_mapping = OrderedDict(sorted(poverty_mapping.items()))

    # Get feature names
    train_feature_names = data.columns.tolist()
    # Remove Target and the Id columns
    train_feature_names = [
        v for v in train_feature_names if v not in ["Target", "Id", "idhogar"]
    ]

    # Name of the dependent variable
    DV = config.model_config.DV

    # Rows in the interim dataframe that has non-null values for
    # the Target column are from the train dataset
    df_train = data.loc[data[DV].notnull(), :].copy()

    # X_train
    X_train = df_train.loc[:, train_feature_names].copy()
    # y_train
    y_train = df_train.loc[:, config.model_config.DV]

    # Rows in the interim dataframe that has null values for
    # the Target column are from the test (holdout) dataset
    X_test = data.loc[data[DV].isnull(), :]
    # Drop the DV column (which is filled with NA)
    # X_test = X_test.drop(DV, axis="columns")

    # Data pipeline
    if config.app_config.DEBUG_PIPELINE:
        pipeline = data_pipeline_debug
    else:
        pipeline = data_pipeline

    # Estimate the test score with CV, and plot the confusion matrix, ROC and PRC
    eval.evaluate(pipeline=pipeline, X_train=X_train, y_train=y_train)

    # Fit pipeline with the entire train set
    pipeline.fit(X_train, y_train)

    # Persist the trained pipeline (when not in DEBUG_PIPELINE mode)
    if not config.app_config.DEBUG_PIPELINE:
        save_pipeline(pipeline_to_persist=data_pipeline)

    # Feature importance of trained Random Forest model
    eval.plot_feature_importance(
        data_pipeline=pipeline,
        X_train=X_train,
        top_n=config.model_config.TOP_N_FEATURE_IMPORTANCE,
        out_path=Path(OUTPUTS_DIR, "feature_importance.png"),
    )

    # Make predictions on X_test using the trained pipeline
    res = predict.make_prediction(input_data=X_test, is_raw_data=False)
    # Create final predictions dataframe
    df_final_predictions = res["test_ids"].copy()
    df_final_predictions["predicted_poverty_level"] = res["predictions"]

    df_final_predictions.to_csv(
        Path(OUTPUTS_DIR, "final_x_test_predictions.csv"), index=False
    )


if __name__ == "__main__":
    run_training()

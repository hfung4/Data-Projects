import pandas as pd
import numpy as np

from pathlib import Path
from collections import OrderedDict

# Custom modules
import src.config as config
from src.config import conf
from src.create_folds import create_folds
from src.train import train
from src.evaluate import evaluate_model


def main():
    # Read interim data
    df = pd.read_pickle(Path(config.INTERIM_DATA_DIR, "interim.pkl"))

    # Get poverty mapping dictionary
    poverty_mapping = conf["POVERTY_MAPPING"]

    # Convert to ordered dict
    poverty_mapping = OrderedDict(sorted(poverty_mapping.items()))

    # Get feature names
    train_feature_names = df.columns.tolist()
    # Remove Target and the Id columns
    train_feature_names = [
        v for v in train_feature_names if v not in ["Target", "Id", "idhogar"]
    ]

    # Name of the dependent variable
    DV = conf["DV"]

    # Rows in the interim dataframe that has non-null values for the Target column are from the train dataset
    df_train = df.loc[df[DV].notnull(), :].copy()
    # Drop "Id" and "idhogar"
    df_train = df_train.drop(["Id", "idhogar"], axis="columns")

    # Rows in the interim dataframe that has null values for the Target column are from the test (holdout) dataset
    X_test = df.loc[df[DV].isnull(), train_feature_names].copy()
    # Save Id and idhogar for each row in X_test
    test_ids = df.loc[df[DV].isnull(), ["Id", "idhogar"]]

    # Test harness: Get train data with folds
    df_folds = create_folds(df_train)

    # Train model

    # row concat the validation set of each fold that is used to evaluate
    # the clean predictions. If we row concat y_val of each fold,
    # we should get the entire train dataset (ordered by fold)
    l_y_train = []

    # "clean" predictions
    l_y_train_pred = []
    # "clean" probability predictions
    l_y_train_pred_proba = []
    l_cv_scores = []

    for fold in range(conf["NFOLDS"]):
        y_preds_val, y_preds_val_proba, y_tr_orig, cv_score = train(
            df_folds=df_folds, fold=fold
        )

        l_y_train_pred.append(y_preds_val)
        l_y_train_pred_proba.append(y_preds_val_proba)
        l_y_train.append(y_tr_orig)
        l_cv_scores.append(cv_score)

    y_train_pred = np.concatenate(l_y_train_pred)
    y_train_pred_proba = np.concatenate(l_y_train_pred_proba)
    y_train = np.concatenate(l_y_train)

    # Evaluate
    if all(s > 1 for s in l_cv_scores):
        # if all scores in l_cv_scores is greater than 1, then print error message
        print("No CV scores calculated!")
    else:
        print(
            f"The mean cv score ({conf['SCORING']}) is {np.round(np.mean(l_cv_scores),3)}. The std-dev of the cv score is {np.round(np.std(l_cv_scores),3)}."
        )

    evaluate_model(y_train, y_train_pred, y_train_pred_proba)

    # If I am only using the entire train set to train model and use the trained model
    # to make predictions from X_test, set fold to None:
    final_predictions = train(df_folds=df_folds, X_test=X_test, fold=None)

    # Map each household predictions (household leves) to individuals
    # and save the final prediction as an csv
    df_final_predictions = test_ids.copy()
    df_final_predictions["predicted_poverty_level"] = final_predictions

    # Save individual level final prediction to csv
    df_final_predictions.to_csv(
        Path(config.OUTPUT_DIR, "final_predictions.csv"), index=False
    )

    print(
        f"Final predictions for each individual in the test set is available in {config.OUTPUT_DIR}/"
    )


if __name__ == "__main__":
    main()

# src/train.py

# REF: https://www.kaggle.com/code/abhishek/competition-part-2-feature-engineering/notebook


import pandas as pd
import argparse


"""imblearn"""
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

"""feature engine"""
from feature_engine.selection import DropConstantFeatures
from feature_engine.imputation import MeanMedianImputer

"""sklearn"""
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier

from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import MinMaxScaler

from sklearn.metrics import f1_score

# Custom modules
import src.config as config
from src.config import conf
import src.data_manager as dm
from src.evaluate import scoring_model

# To test, in terminal, run train as a module: python -m src.train
def train(df_folds: pd.DataFrame, X_test: pd.DataFrame = None, fold: int = None):
    """train: perform cross validation, process data, and train model

    Args:
        df_folds (pd.DataFrame): train dataset with folds column
        X_test (pd.DataFrame): test dataset (with no label)
        fold (int): fold number
    """
    # Get the train and validation set --------------------------------------

    if fold is not None:
        # Train set is where the value in kfold column is not
        # equal to the provided "fold" (input argument of this function)
        train_set = df_folds.loc[df_folds["kfold"] != fold].reset_index(drop=True)
        # Drop the kfold column
        train_set = train_set.drop("kfold", axis="columns")

        # Validation set is where kfold is equal to the provided fold
        valid_set = df_folds.loc[df_folds["kfold"] == fold].reset_index(drop=True)
        valid_set = valid_set.drop("kfold", axis="columns")
    # We are using the full train set to train model
    else:
        # Use the entire df_folds as train_set
        train_set = df_folds.copy().drop("kfold", axis="columns")

    # X_tr: drop the label column from the dataframe
    X_tr = train_set.drop(conf["DV"], axis="columns")
    y_tr = train_set.loc[:, conf["DV"]]

    if fold is not None:
        # X_val: drop the label from the dataframe
        X_val = valid_set.drop(conf["DV"], axis="columns")
        y_val = valid_set.loc[:, conf["DV"]]
    else:
        # Since we are using the full train set to train model, the
        # "validation set" would be the hold-out test set (X_test)
        # The test set is unlabeled since it is supposed to be new/unknown data
        X_val = X_test.copy()

    # Data processing -----------------------------------------
    # NOTE 1: if I have many data processing steps, it would be better to
    # specify them in a imblearn data pipeline.

    # NOTE 2: this project is in production. I will not do any parameters tuning; instead,
    # I will specify all hyperparameters of the data pipeline in config.yml

    # Imputation
    imputer = MeanMedianImputer(imputation_method=conf["IMPUTATION_METHOD"])
    X_tr = imputer.fit_transform(X_tr, y_tr)
    X_val = imputer.transform(X_val)

    # drop nzv
    drop_nzv = DropConstantFeatures(tol=conf["DROP_NZV_TOL"])
    X_tr = drop_nzv.fit_transform(X_tr, y_tr)
    X_val = drop_nzv.transform(X_val)

    # oversampling
    smote = SMOTE(
        sampling_strategy=conf["OVERSAMPLING_STRATEGY"],
        random_state=conf["RANDOM_STATE"],
    )

    # NOTE: I only apply resampling (for both over- and under- sampling) on the train set
    # I leave the validation and test set imbalanced
    # This is to avoid overfitting
    X_tr, y_tr = smote.fit_resample(X_tr, y_tr)

    # Undersampling
    undersampler = RandomUnderSampler(
        sampling_strategy=conf["UNDERSAMPLING_STRATEGY"],
        random_state=conf["RANDOM_STATE"],
    )
    X_tr, y_tr = undersampler.fit_resample(X_tr, y_tr)

    # Normalization
    scaler = MinMaxScaler()
    X_tr = scaler.fit_transform(X_tr, y_tr)
    X_val = scaler.transform(X_val)

    # Feature selection with model

    # Use ExtraTreesClassifier to perform feature selection
    sel_clf = ExtraTreesClassifier(
        n_estimators=conf["FEATURE_SEL_MODEL_N_ESTIMATORS"],
        random_state=conf["RANDOM_STATE"],
    )

    # Feature selector
    fs = SelectFromModel(estimator=sel_clf)
    X_tr = fs.fit_transform(X_tr, y_tr)
    X_val = fs.transform(X_val)

    # Train model
    clf = RandomForestClassifier(
        n_estimators=conf["CLF__N_ESTIMATORS"],
        max_depth=conf["CLF__MAX_DEPTH"],
        min_samples_split=conf["CLF__MIN_SAMPLES_SPLIT"],
        min_samples_leaf=conf["CLF__MIN_SAMPLES_LEAF"],
        random_state=conf["RANDOM_STATE"],
    )

    clf.fit(X_tr, y_tr)

    # If I am performing cross-validation, I will output "clean" predictions of each fold
    # If used the entire train set to train model (fold is None)
    # I will output the final predictions of test set (for submission)
    y_preds_val = clf.predict(X_val)
    # Get probability estimates of each class, needed to plot roc curve and pr curve
    y_preds_val_proba = clf.predict_proba(X_val)

    # Save model and processed data

    # Save model for each fold
    dm.save_model(clf=clf, fold=fold)
    # Save processed data for each fold
    dm.save_processed_data(fold=fold, X_tr=X_tr, y_tr=y_tr, X_val=X_val)

    if fold is not None:
        # Score model
        cv_score = scoring_model(y_val, y_preds_val, fold)

        # Return the predictions
        # I am outputing y_val, which is the original train data that is used
        # to evaluate the trained model of each fold
        return y_preds_val, y_preds_val_proba, y_val, cv_score
    else:
        # If I am training model with the entire train set, I will only make
        # inference on X_test and output the final predictions
        return y_preds_val

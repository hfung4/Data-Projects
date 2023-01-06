# src/evaluate.py

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import itertools
from collections import OrderedDict
from pathlib import Path
from typing import Union, Dict

"""metrics"""
from sklearn.metrics import (
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    average_precision_score,
    roc_curve,
    roc_auc_score,
)

import src.config as config
from src.config import conf


def plot_confusion_matrix(
    cm,
    classes,
    out_path,
    normalize=False,
    title="Confusion matrix",
    cmap=plt.cm.Oranges,
):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    Source: http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
    """
    if normalize:
        cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]

    plt.figure(figsize=(10, 10))
    plt.imshow(cm, interpolation="nearest", cmap=cmap)
    plt.title(title, size=24)
    plt.colorbar(aspect=4)
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45, size=14)
    plt.yticks(tick_marks, classes, size=14)

    fmt = ".2f" if normalize else "d"
    thresh = cm.max() / 2.0

    # Labeling the plot
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(
            j,
            i,
            format(cm[i, j], fmt),
            fontsize=20,
            horizontalalignment="center",
            color="white" if cm[i, j] > thresh else "black",
        )

    plt.grid(None)
    plt.tight_layout()
    plt.ylabel("True label", size=18)
    plt.xlabel("Predicted label", size=18)

    # Save
    plt.savefig(out_path)


def plot_multiclass_roc(
    y_val: pd.Series,
    y_scores: pd.Series,
    mapping: Dict,
    out_path: Union[str, Path],
    figsize: tuple[int, int] = (20, 8),
):
    """plot_multiclass_roc

    Args:
        y_val (pd.Series): true values of DV
        y_scores (pd.Series): probability estimation of DV
        mapping (Dict): mapping dictionary of numeric encoding of DV to its string encoding
        out_path (Union[str, Path]): output path of the saved PRC png figure
        figsize (tuple[int, int], optional): Size of PRC figure. Defaults to (20, 8).
    """

    # structures
    fpr = dict()
    tpr = dict()
    roc_auc = dict()

    # get dummy variables for y_val, one for each level
    y_val_dummies = pd.get_dummies(y_val, drop_first=False).values

    # Compute fpr and tpr for each class
    # Also compute the ROC_AUC for each class
    for k, v in mapping.items():
        fpr[v], tpr[v], _ = roc_curve(y_val_dummies[:, k - 1], y_scores[:, k - 1])
        roc_auc[v] = roc_auc_score(y_val_dummies[:, k - 1], y_scores[:, k - 1])

    # plot roc for each class
    fig, ax = plt.subplots(figsize=figsize)
    plt.style.use("fivethirtyeight")
    plt.rcParams["font.size"] = 12

    for _, v in mapping.items():
        ax.plot(
            fpr[v],
            tpr[v],
            label=f"ROC curve for class {v} (area = {round(roc_auc[v],2)})",
        )

    # plot settings
    ax.plot([0, 1], [0, 1], "k--")  # plot the 45 deg line

    ax.set_xlim([0.0, 1.0])  # set x and y limits
    ax.set_ylim([0.0, 1.05])

    ax.set_xlabel("False Positive Rate")  # set x and y labels and title
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROCs")

    ax.legend(loc="best")
    # plt.show()

    # Save plot
    plt.savefig(out_path)


def plot_multiclass_prc(
    y_val: pd.Series,
    y_scores: pd.Series,
    mapping: Dict,
    out_path: Union[str, Path],
    figsize: tuple[int, int] = (15, 8),
):
    """plot_multiclass_prc

    Args:
        y_val (pd.Series): true values of DV
        y_scores (pd.Series): probability estimation of DV
        mapping (Dict): mapping dictionary of numeric encoding of DV to its string encoding
        out_path (Union[str, Path]): output path of the saved PRC png figure
        figsize (tuple[int, int], optional): Size of PRC figure. Defaults to (15, 8).
    """

    # structures
    precisions = dict()
    recalls = dict()
    thresholds = dict()
    auprcs = dict()

    # get dummy variables for y_val, one for each level
    y_val_dummies = pd.get_dummies(y_val, drop_first=False).values

    # Compute precision, recall for each class
    # Also compute the AUPRC for each class
    for k, v in mapping.items():
        precisions[v], recalls[v], _ = precision_recall_curve(
            y_val_dummies[:, k - 1], y_scores[:, k - 1]
        )
        auprcs[v] = average_precision_score(y_val_dummies[:, k - 1], y_scores[:, k - 1])

    # plot precision and recall vs threshold for each class
    fig, ax = plt.subplots(figsize=figsize)
    plt.style.use("fivethirtyeight")
    plt.rcParams["font.size"] = 12

    for _, v in mapping.items():
        ax.plot(
            recalls[v],
            precisions[v],
            label=f"PRCfor class {v} (area = {round(auprcs[v],2)})",
        )

    # Plot settings
    ax.set_xlim([0.0, 1.0])  # set x and y limits
    ax.set_ylim([0.0, 1.05])

    ax.set_xlabel("Recall")  # set x and y labels and title
    ax.set_ylabel("Precision")
    ax.set_title("Precision and Recall Curves")

    ax.legend(loc="best")
    # plt.show()
    plt.savefig(out_path)


def scoring_model(y_val: pd.Series, y_preds_val: pd.Series, fold: int) -> float:

    """scoring_model: wrapper function for computing cv score of model

    Args:
        y_val (pd.Series): DV of validation set of each fold
        y_preds_val (pd.Series): prediction inferred from X of the validation set of each fold
        fold (int): fold number

    Returns:
        float: cv score
    """
    match conf["SCORING"]:
        case "f1_weighted":
            cv_score = f1_score(y_val, y_preds_val, average="weighted")
            print(f"Fold {fold} {conf['SCORING']}: {round(cv_score,3)}")

        case "f1_macro":
            cv_score = f1_score(y_val, y_preds_val, average="macro")
            print(f"Fold {fold} {conf['SCORING']}: {round(cv_score,3)}")

        case "average_precision":
            cv_score = average_precision_score(y_val, y_preds_val, average="macro")
            print(f"Fold {fold} {conf['SCORING']}: {round(cv_score,3)}")
        case _:
            cv_score = 999.0
            print(
                "Error: use only 'f1_weighted', 'f1_macro', or 'average_precision' in 'src/config.yml'"
            )
    return cv_score


def evaluate_model(
    y_train: pd.Series, y_train_pred: pd.Series, y_train_pred_proba: pd.Series
):
    """evaluate_model: plot confusion matrix heatmap, ROC and PRC

    Args:
        y_train (pd.Series): DV of the full train set (reordered by folds)
        y_train_pred (pd.Series): clean class predictions of each fold
        y_train_pred_proba (pd.Series): clean class probability predictions of each fold
    """

    # Convert poverty mapping to ordered dict
    poverty_mapping = conf["POVERTY_MAPPING"]
    poverty_mapping = OrderedDict(sorted(poverty_mapping.items()))

    l_poverty_classes = [v for v in conf["POVERTY_MAPPING"].values()]

    # Confusion matrix
    cm = confusion_matrix(y_train, y_train_pred)

    # Plot confusion matrix, without normalization
    plot_confusion_matrix(
        cm=cm,
        classes=l_poverty_classes,
        out_path=Path(config.OUTPUT_DIR, "confusion_matrix_no_normalization.png"),
        normalize=False,
        title="Poverty Confusion Matrix, no normalization",
    )
    # Plot confusion matrix, normalization
    plot_confusion_matrix(
        cm=cm,
        classes=l_poverty_classes,
        out_path=Path(config.OUTPUT_DIR, "confusion_matrix_normalization.png"),
        normalize=True,
        title="Poverty Confusion Matrix, normalization",
    )

    # ROC
    plot_multiclass_roc(
        y_val=y_train,
        y_scores=y_train_pred_proba,
        mapping=poverty_mapping,
        out_path=Path(config.OUTPUT_DIR, "roc.png"),
    )

    # PRC
    plot_multiclass_prc(
        y_val=y_train,
        y_scores=y_train_pred_proba,
        mapping=poverty_mapping,
        out_path=Path(config.OUTPUT_DIR, "prc.png"),
    )

    print("Model evaluation completed.")

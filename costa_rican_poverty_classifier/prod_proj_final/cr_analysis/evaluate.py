import itertools
from collections import OrderedDict
from pathlib import Path
from typing import Dict, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    f1_score,
    make_scorer,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import StratifiedKFold, cross_val_predict, cross_val_score

from cr_analysis.config.core import OUTPUTS_DIR, config


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
    plt.savefig(out_path, dpi=300, bbox_inches="tight")


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
        mapping (Dict): mapping dictionary of numeric encoding
        of DV to its string encoding
        out_path (Union[str, Path]): output path of
        the saved PRC png figure
        figsize (tuple[int, int], optional): Size of
        PRC figure. Defaults to (20, 8).
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
    plt.savefig(out_path, dpi=300, bbox_inches="tight")


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
        y_scores (pd.Series): probability
        estimation of DV
        mapping (Dict): mapping dictionary of
        numeric encoding of DV to its string encoding
        out_path (Union[str, Path]): output
        path of the saved PRC png figure
        figsize (tuple[int, int], optional): Size of
        PRC figure. Defaults to (15, 8).
    """

    # structures
    precisions = dict()
    recalls = dict()
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

    for k, v in mapping.items():
        ax.plot(
            recalls[v],
            precisions[v],
            label=f"PRC for class {v} (area = {round(auprcs[v],2)}"
            + f" vs prop of class: {round(y_val_dummies[:, k - 1].mean(),2)})",
        )
    # Plot settings
    ax.set_xlim([0.0, 1.0])  # set x and y limits
    ax.set_ylim([0.0, 1.05])

    ax.set_xlabel("Recall")  # set x and y labels and title
    ax.set_ylabel("Precision")
    ax.set_title("Precision and Recall Curves")

    ax.legend(loc="best")
    # plt.show()
    plt.savefig(out_path, dpi=300, bbox_inches="tight")


def evaluate(pipeline, X_train, y_train):
    # Init the StratifiedKFold object
    skf = StratifiedKFold(
        n_splits=config.model_config.NFOLDS,
        shuffle=True,
        random_state=config.model_config.RANDOM_STATE,
    )
    match config.model_config.SCORING:
        case "f1":
            scorer = make_scorer(f1_score, average="weighted")
        case "precision":
            scorer = make_scorer(precision_score, average="weighted")
        case "recall":
            scorer = make_scorer(recall_score, average="weighted")
        case _:
            scorer = make_scorer(f1_score, average="weighted")

    # Score the pipeline with CV (estimated test
    # scores for f1_score, precision, or recall)
    cv_scores = cross_val_score(
        estimator=pipeline,
        X=X_train,
        y=y_train,
        cv=skf,
        scoring=scorer,  # config.model_config.SCORING,
    )

    print(
        f"The mean cv score (weighted {config.model_config.SCORING} score)"
        + f"is {round(np.mean(cv_scores),2)} with standard"
        + f"deviation of {round(np.std(cv_scores),2)}."
    )

    # Plot confusion martrix, roc, and prc

    # Compute clean y_train estimated probabilities
    y_train_pred_scores = cross_val_predict(
        estimator=pipeline, X=X_train, y=y_train, cv=skf, method="predict_proba"
    )

    # Compute clean y_train predictions
    y_train_pred = cross_val_predict(
        estimator=pipeline, X=X_train, y=y_train, cv=skf, method="predict"
    )

    # Plot confusion matrix
    cm = confusion_matrix(y_train, y_train_pred)
    plot_confusion_matrix(
        cm=cm,
        classes=["extreme", "moderate", "vulnerable", "not vulnerable"],
        out_path=Path(OUTPUTS_DIR, "confusion_matrix.png"),
        normalize=True,
        title="Poverty Confusion Matrix",
    )

    # Get poverty mapping dictionary
    poverty_mapping = config.model_config.POVERTY_MAPPING
    # Convert to ordered dict
    poverty_mapping = OrderedDict(sorted(poverty_mapping.items()))

    # Plot ROC_AUC curve and ROC_AUC score
    plot_multiclass_roc(
        y_val=y_train,
        y_scores=y_train_pred_scores,
        mapping=poverty_mapping,
        out_path=Path(OUTPUTS_DIR, "roc.png"),
    )

    # Plot PRC curve and ROC_AUC score
    plot_multiclass_prc(
        y_val=y_train,
        y_scores=y_train_pred_scores,
        mapping=poverty_mapping,
        out_path=Path(OUTPUTS_DIR, "prc.png"),
    )


def plot_feature_importance(data_pipeline, X_train, top_n, out_path):
    # features dropped due to nzv
    dropped_features = data_pipeline.named_steps.drop_nzv.features_to_drop_

    # get features that remained after dropping those with nzv
    feature_names_post_nzv = [
        f for f in X_train.columns.values if f not in dropped_features
    ]

    # Get the boolean mask of features that are selected by SelectFrom Model
    mask = data_pipeline.named_steps.fs.get_support()

    # Get final list of features that are selected
    selected_features = list(itertools.compress(feature_names_post_nzv, mask))

    # Get fitted Random Forest model
    fitted_rf = data_pipeline.named_steps["clf"]

    # Get feature importances and put into a dataframe
    feature_results = pd.DataFrame(
        {"feature": selected_features, "importance": fitted_rf.feature_importances_}
    )

    # Plot feature importance

    # Plot styling
    plt.style.use("fivethirtyeight")
    plt.rcParams["font.size"] = 12

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1)

    (
        feature_results.sort_values("importance", ascending=False)
        .set_index("feature")
        .head(top_n)
        .plot.barh(
            ax=ax,
            color="k",
            alpha=0.7,
            title=f"Top {top_n} important features from random forest",
            ylabel="Normalized feature importance",
            xlabel="Features",
        )
    )
    plt.savefig(out_path, dpi=300, bbox_inches="tight")

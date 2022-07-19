import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from home_price_analysis import __version__ as _version
from home_price_analysis.config.core import FIGURES_DIR, config


def comparison_plot(pipeline_metric: float, baseline_metric: float, metric_name: str):
    """
    This function generates a comparison plot of the performance
    of a baseline model vs gradient boosting (measured by rmse)

    Args:
        pipeline_metric(float): estimated test rmse of gb
        baseline_metric(obj): estimated test rmse of baseline model
        metric_name: name of the metric

    Returns:
        void
    """

    # Generate bar plot that compares the rmse of baseline model to gradient boosting
    df_perf = pd.DataFrame(
        {
            "model name": ["baseline", "xgb"],
            "metric": [baseline_metric, pipeline_metric],
        }
    )

    # Plot
    figure = plt.figure(figsize=(10, 8))
    sns.set(font_scale=1.2)  # increase font of all elements

    ax = figure.add_subplot(1, 1, 1)
    sns.barplot(x="model name", y="metric", data=df_perf, ax=ax)
    ax.bar_label(ax.containers[0])  # add text of bar tip
    ax.set_ylabel(metric_name)
    ax.set_title(f"{metric_name} comparision of xgb and baseline model")

    # save plot
    save_file_name = (
        f"{metric_name}_{config.app_config.MODEL_PERF_PLOT_NAME}{_version}.png"
    )
    save_path = FIGURES_DIR / save_file_name
    plt.savefig(save_path)

    return None

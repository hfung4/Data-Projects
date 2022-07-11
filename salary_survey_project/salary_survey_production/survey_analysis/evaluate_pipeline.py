from sklearn.metrics import mean_squared_error
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from survey_analysis import __version__ as _version
from survey_analysis.config.core import (
    FIGURES_DIR,
    config)


def comparison_plot(pipeline_to_evaluate:object,
                    baseline_model:object,
                    X_test:pd.DataFrame,
                    y_test:pd.Series):
    '''
    This function generates a comparison plot of the performance of a baseline model vs gradient
    boosting (measured by rmse)

    Args:
        pipeline_to_evaluate(obj): trained pipeline
        baseline_model(obj): trained baseline regressor
        X_test(pd.DataFrame): Test data features
        y_test(pd.Series): Test data dependent variable

    Returns:
        void
   '''

    # Make predictions and get baseline performance\
    y_pred_baseline=baseline_model.predict(X_test)
    baseline_rmse = round(mean_squared_error(y_test,y_pred_baseline, squared=False),2)

    # Get the test rmse (from validation set approach) of trained pipeline
    y_pred_gb = pipeline_to_evaluate.predict(X_test)
    gb_rmse = round(mean_squared_error(y_test,y_pred_gb, squared=False),2)

    # Generate bar plot that compares the rmse of baseline model to gradient boosting
    df_perf=pd.DataFrame({
        "model name":["baseline","gradient boosting"],
        "rmse":[baseline_rmse, gb_rmse]
    })

    # Plot
    figure = plt.figure(figsize=(10,8))
    sns.set(font_scale=1.2) # increase font of all elements

    ax = figure.add_subplot(1,1,1)
    sns.barplot(x='model name', y='rmse', data=df_perf, ax=ax)
    ax.bar_label(ax.containers[0]) # add text of bar tip

    # save plot
    save_file_name = f"{config.app_config.model_perf_plot_filename}{_version}.png"
    save_path = FIGURES_DIR / save_file_name
    plt.savefig(save_path)










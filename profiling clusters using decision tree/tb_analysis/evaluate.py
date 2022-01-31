# common libraries
import pandas as pd
# type checking
from typing import Dict
# sklearn
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report,roc_auc_score
# plotting
import matplotlib.pyplot as plt
# config
from tb_analysis.config.core import config, IMAGES_DIR

def evaluate(gs,
         train_test_dict: Dict,
         p: str):
    """
   This is a wrapper function that performs decision tree training and optimization
    Args:
        gs: GridSearchCV object
        train_test_dict(dict): input dictionary of train and test dataframe
        p(str): prototype

    Returns:
        void
    """
    # Get train and test data
    train_test_data = train_test_dict[p]

    # Test predictions
    y_pred = gs.predict(train_test_data["X_test"])

    # Model evaluation (from CV)
    print("The tuned hyperparameters for the model are: {}".format(gs.best_params_))
    print("The best estimated test accuracy (fron CV): {}".format(gs.best_score_))
    print()
    print()
    print(f'''The test accuracy score of the optimized decision tree on test data) is: 
    {accuracy_score(train_test_data["y_test"], y_pred)}''')
    print()
    print("Classification Report (on test data)")
    print(classification_report(train_test_data["y_test"], y_pred))

    # Feature importance
    feature_importance(gs=gs,
                       train_test_data = train_test_data,
                       p=p)




def feature_importance(gs,
                       train_test_data: Dict,
                       p:str):
    """
      This is a wrapper function that outputs the relative importance of features in the decision tree
      using a table and a bar plot
       Args:
           gs: GridSearchCV object
           train_test_data(dict): input dictionary of train and test dataframe
           p(str): prototype

       Returns:
           void
       """

    # Get feature importance datafrarme
    feature_importance = pd.DataFrame({'feature': list(train_test_data["X_train"].columns),
                                 'importance': gs.best_estimator_.feature_importances_})

    # Show the top X most important
    top_n = config.model_config.num_feature_importance

    feature_importance = feature_importance.sort_values('importance', ascending = False).reset_index(drop=True)
    feature_importance.head(top_n)

    # Plotting
    fig = plt.figure(figsize=(10, 10))

    # Plot the 10 most important features in a horizontal bar chart
    feature_importance.loc[:top_n, :].plot(x='feature', y='importance',
                                       edgecolor='k',
                                       kind='barh', color='red');
    plt.xlabel('Relative Importance', size=20);
    plt.ylabel('')
    plt.title('Feature importance from' + p + ' decision tree', size=20)

    save_file_name = f"{p}_feature_importance.png"
    save_path = IMAGES_DIR / save_file_name
    plt.savefig(save_path)

    plt.show()
















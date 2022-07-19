"""Contains helper functions that are used for modelling. 
These functions will only be used in the research environment."""

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import cross_val_score

# define models to test
def get_models():
    # init list of models with associated names
    models, names = list(), list()

    # linear regression
    models.append(LinearRegression())
    names.append("linear_regression")

    # Random Forest Regressor
    models.append(RandomForestRegressor())
    names.append("random_forest")

    # Gradient Boosted Trees
    models.append(GradientBoostingRegressor())
    names.append("gradient_boosting")

    return models, names


# Evaluate a model with k-fold cross validation
def evaluate_model(X, y, model):
    scores = cross_val_score(estimator=model, X=X, y=y, cv=10, scoring="r2", n_jobs=-1)

    return scores

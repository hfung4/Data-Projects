# ==============================================================================
# Using repeated cross-sectional survey data from the Australian public service
# to predict employees' intent to leave
# ==============================================================================

import pandas as pd
import numpy as np
from sklearn.externals import joblib
from collections import Counter
from sklearn.preprocessing import StandardScaler
import helpers
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from imblearn.over_sampling import SMOTE
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import auc, roc_curve, roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier as XGBClassifier
import statsmodels.api as statmod
from sklearn.pipeline import Pipeline
import warnings

warnings.filterwarnings("ignore")

if __name__ == "__main__":

    # Import and Process data
    # ==================================================
    df_2019 = helpers.process_data(2019)
    df_2018 = helpers.process_data(2018)
    df_2017 = helpers.process_data(2017)
    df_2017['gender_Prefer not to say'] = 0
    df_2017 = df_2017.sort_index(axis=1)  # sort column by column names

    # Aggregating the repeated cross-sectional data
    data = pd.concat([df_2019, df_2018, df_2017], axis=0)

    # check for missing values
    print(data.isnull().sum())

    # For this notebook, I will only work with a much smaller subset of the dataset.
    # I will randomly sample 20 k respondents and perform analysis and modelling.
    data = data.sample(n=20000, random_state=10)

    # Exploratory Analysis
    # ==================================================
    items = pd.read_excel("data/aust_aps_items.xlsx", sheet_name="2019")
    practices = items.loc[items.Type == "mgmt_practice", "Factor"].unique().tolist()
    attitudes = items.loc[items.Type == "employee_attitudes", "Factor"].unique().tolist()
    attitudes.remove("intent_to_leave")

    print("The management practices are: {}".format(practices))
    print("")
    print("I have {} management practices.".format(len(practices)))

    print("The employee attitudes are: {}".format(attitudes))
    print("")
    print("I have {} employee attitudes.".format(len(attitudes)))

    print(data.intent_to_leave.value_counts(normalize=True))

    # Look at the probability distributions of several management practices and employee attitudes

    temp = np.array(practices).reshape(5, 3)
    fig, axes = plt.subplots(5, 3, figsize=(10, 8))
    for i in range(5):
        for j in range(3):
            sns.distplot(data[temp[i, j]], bins=100, hist=True, kde=False, ax=axes[i, j])
    plt.subplots_adjust(wspace=0.5, hspace=1)  # width and height space between plots
    plt.show()

    temp = np.array(attitudes).reshape(3, 2)
    fig, axes = plt.subplots(3, 2, figsize=(10, 8))
    for i in range(3):
        for j in range(2):
            sns.distplot(data[temp[i, j]], bins=100, hist=True, kde=False, ax=axes[i, j])
    plt.subplots_adjust(wspace=0.5, hspace=1)  # width and height space between plots
    plt.show()

    # Let's explore the Australia APS dataset and see if they follow the same pattern.
    temp = ["clear_obj", "skills_match", "fair_rwd", "autonomy",
            "promote_ethics", "mgr_fb", "pay_satisfaction", "safety",
            "wpi_o", "job_satisfaction"]
    temp = np.array(temp).reshape(5, 2)

    fig, axes = plt.subplots(5, 2, figsize=(10, 8))
    for i in range(5):
        for j in range(2):
            sns.barplot(y="intent_to_leave", x=temp[i, j], data=data, ax=axes[i, j])
    plt.subplots_adjust(wspace=0.5, hspace=1)  # width and height space between plots
    plt.show()

    temp2 = [col for col in practices if col not in temp]
    temp2.append("intrinsic_motivation")
    temp2 = np.array(temp2).reshape(4, 2)

    fig, axes = plt.subplots(4, 2, figsize=(10, 10))
    for i in range(4):
        for j in range(2):
            sns.boxplot(x="intent_to_leave", y=temp2[i, j], data=data, ax=axes[i, j])
    plt.subplots_adjust(wspace=0.5, hspace=1)  # width and height space between plots
    plt.show()

    # Correlation between variables
    # ==================================================
    helpers.correlation_analysis(data[practices], "output/correlation_practices.csv")
    helpers.correlation_analysis(data[attitudes], "output/correlation_attitudes.csv")

    # Predictive Modelling
    # ==================================================
    X = data.drop("intent_to_leave", axis=1)  # drop intent_to_leave
    X.drop(attitudes, axis=1, inplace=True)  # drop employee attitudes
    feature_names = list(X.columns.values)  # save the feature names
    X = np.array(X)

    y = data["intent_to_leave"].astype(int)
    y = np.array(y)

    # Train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=10)

    # Baseline guess
    # since 0 is the most frequent class, my naive guess is 0 for all respondents
    baseline_guess = np.zeros(len(y_test))

    print("The accuracy score of my baseline model is {}".format(round(accuracy_score(baseline_guess, y_test), 2)))
    print("")
    print("The classification report of my baseline model:")
    print(classification_report(baseline_guess, y_test))

    # Generate Synthetic samples to ameliorate imbalanced classe
    execute = True
    if execute:
        sm = SMOTE()  # init the smote model
        X_train, y_train = sm.fit_sample(X_train, y_train)  # fit the model to train data
        Counter(y_train)  # The classes are now balanced by upsampling the minority class 1

    # Logistic Regression
    # ==================================================
    pipe_lr = Pipeline([('clf', LogisticRegression(penalty='l1',
                                                   solver='liblinear',
                                                   random_state=10))])  # pipeline for logreg

    grid_params_lr = {'clf__C': [0.1, 0.5, 1, 5, 10]}  # variance of model decreases as C increase

    execute = False
    if execute:
        # init GridSearch object
        gs_lr = GridSearchCV(estimator=pipe_lr,
                             param_grid=grid_params_lr,
                             scoring='f1',
                             cv=5,
                             n_jobs=-1,
                             verbose=2)
        gs_lr.fit(X_train, y_train)  # fit model
        print("The best parameters are: {}".format(gs_lr.best_params_))

        joblib.dump(gs_lr, 'saved_models/gs_lr.pkl')  # save GridSearchCV object

    # load model
    gs_lr = joblib.load('saved_models/gs_lr.pkl')

    y_pred_lr = gs_lr.predict(X_test)

    print(classification_report(y_pred_lr, y_test))

    '''        
    Compared with the baseline guess, the f1 score for class 0 reduced slightly, 
    but the precision, recall, and f1-score of class 1 is no longer zero (though still low).
    On the whole, logistic regression is an improvement on our baseline.
    '''

    logreg = gs_lr.best_estimator_.named_steps["clf"]  # get the best logreg model
    params = np.append(logreg.intercept_, logreg.coef_)
    feature_names.insert(0, "constant")

    df_coeff = pd.DataFrame(list(zip(feature_names, params)), columns=["features", "coeff"])
    print(df_coeff.sort_values(by="coeff"))

    '''
    Surprisingly, autonomy and fair_rwd are have coefficients that were regularized to close to 0.  
    However, the effect sizes of clear objective and skills match are large (similar to what we see 
    in other survey datasets).
    '''

    # Random Forest Classifier
    # ==================================================

    pipe_rf = Pipeline([('scl', StandardScaler()),
                        ('clf', RandomForestClassifier(random_state=10))])

    grid_params_rf = {
        "clf__n_estimators": [200, 800, 1000],
        "clf__max_depth": [10, 15, 20, 50, 80],
        "clf__min_samples_split": [2, 5],  # [2, 5, 10]
        "clf__min_samples_leaf": [1, 2, 4]  # [1, 2, 4]
    }

    execute = False
    if execute:
        # init GridSearch object
        gs_rf = GridSearchCV(estimator=pipe_rf,
                             param_grid=grid_params_rf,
                             scoring='f1',
                             cv=5,
                             n_jobs=-1,
                             verbose=2)
        gs_rf.fit(X_train, y_train)  # fit model
        print("The best parameters are: {}".format(gs_rf.best_params_))

        joblib.dump(gs_rf, 'saved_models/gs_rf.pkl')  # save GridSearchCV object

    # load model
    gs_rf = joblib.load('saved_models/gs_rf.pkl')

    y_pred_rf = gs_rf.predict(X_test)

    print("The accuracy of the tuned Random Forest model (on test data) is {}".format(
        accuracy_score(y_pred_rf, y_test)))

    y_pred_rf = gs_rf.predict(X_test)

    print("The accuracy of the tuned Random Forest model (on test data) is {}".format(
        accuracy_score(y_pred_rf, y_test)))

    print(classification_report(y_pred_rf, y_test))

    best_rf_model = gs_rf.best_estimator_.named_steps['clf']

    # Random Forest Feature Importance
    # ==================================================

    feature_importance = pd.DataFrame({'feature': feature_names[1:],
                                       'importance': gs_rf.best_estimator_.named_steps['clf'].feature_importances_})

    # Show the top 10 most important
    feature_importance = feature_importance.sort_values('importance', ascending=False).reset_index(drop=True)

    fig = plt.figure(figsize=(20, 20))
    # Plot the 10 most important features in a horizontal bar chart
    feature_importance.plot(x='feature', y='importance',
                            edgecolor='k',
                            kind='barh', color='red');
    plt.xlabel('Relative Importance', size=10);
    plt.ylabel('')
    plt.title('Feature Importances from Random Forest', size=15);
    plt.show()

    # XGBoost Classifier
    # ==================================================

    pipe_xgb = Pipeline([('scl', StandardScaler()),
                         ('clf', XGBClassifier(objective="binary:logistic", learning_rate=0.05, random_state=10))])

    grid_params_xgb = {
        "clf__n_estimators": [100, 1000],
        "clf__max_depth": [2, 6],
        "clf__min_child_weight": [1, 3, 5],
        "clf__gamma": [0.1, 0.5],
        "clf__subsample": [0.4, 0.8],
        "clf__colsample_bytree": [0.2, 0.8]
    }

    execute = False
    if execute:
        # init GridSearch object
        gs_xgb = GridSearchCV(estimator=pipe_xgb,
                              param_grid=grid_params_xgb,
                              scoring='f1',
                              cv=5,
                              n_jobs=-1,
                              verbose=2)
        gs_xgb.fit(X_train, y_train)  # fit model
        print("The best parameters are: {}".format(gs_xgb.best_params_))
        joblib.dump(gs_rf, 'saved_models/gs_xgb.pkl')  # save GridSearchCV object

    # load model
    gs_xgb = joblib.load('saved_models/gs_xgb.pkl')

    y_pred_xgb = gs_xgb.predict(X_test)

    print("The accuracy of the tuned XGBoostClassifer model (on test data) is {}".format(
        accuracy_score(y_pred_xgb, y_test)))

    print(classification_report(y_pred_xgb, y_test))

    # AUC-ROC for the Random Forest Classifier
    # ==================================================

    y_prob_rf = gs_rf.predict_proba(X_test)  # get probability score for class= 0 and class= 1

    # FPR: Fallout = false positive rate = FP/total number of negative events that are predicted by the model
    # TPR: true positive rate:  TPR = Recall = TP/total number of positive events that is predicted by the model
    FPR, TPR, thresholds = roc_curve(y_test, y_prob_rf[:, 1])  # use prob score for class 1

    ROC_AUC = auc(FPR, TPR)  # AUC area under the curve

    print("The area under the curve (AUC) is: {}".format(ROC_AUC))
    # Alternatively, use roc_auc_score from sklearn.  The inputs are y_test, and
    # probability score of the larger label.
    print("ROC_AUC score is: {}".format(roc_auc_score(y_test, y_prob_rf[:, 1])))

    plt.figure(figsize=[6, 6])
    plt.plot(FPR, TPR, label='ROC curve(area = %0.2f)' % ROC_AUC, linewidth=4)  # plot FPR and TPR
    plt.plot([0, 1], [0, 1], 'k--', linewidth=4)  # 45 deg line
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=15)
    plt.ylabel('True Positive Rate', fontsize=15)
    plt.title('ROC for Random Forest Classifier', fontsize=18)
    plt.show()

    # Statistical Inference with Logistic Regression
    # ==================================================

    # Investigate the hetrogeneous effects of management practices
    # on intent to leave for employees' with different levels of
    # intrinsic motivation.

    # a list of top 6 important feature from the Random Forest classifier
    important_features = list(feature_importance.iloc[:6, 0])

    temp = important_features.copy()
    temp.append("intrinsic_motivation")

    X = data[temp]
    X = helpers.gen_interaction(X, important_features, "intrinsic_motivation")
    feat_interact_names = list(X.columns.values)  # save the feature names

    y = data["intent_to_leave"]

    # Regress intent_to_leave on "important features" and their interaction with intrinsic motivation
    X = statmod.add_constant(X)  # add constant

    # Logit model
    logit_mod = statmod.Logit(y, X)
    logit_res = logit_mod.fit()

    print(logit_res.summary())

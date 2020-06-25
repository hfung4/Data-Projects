#! /usr/bin/env python

import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import chi2
import helpers
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, recall_score, precision_score
from sklearn.metrics import f1_score, confusion_matrix, classification_report
import warnings

warnings.filterwarnings("ignore")


if __name__ == "__main__":

    # Import data
    # ==================================================

    nfr = pd.read_csv("processed_data/nfr_processed.csv")
    nfr = nfr.loc[nfr["labels"] != "F", :]  # keep only non-functional requirements
    nfr = nfr.reset_index(drop=True)

    class_count = nfr.groupby("labels").trigrams.count()  # number of requirements in each class
    class_count = class_count.reset_index()

    class_count.sort_values(by="trigrams", ascending=False, inplace=True)

    fig = plt.figure(figsize=(8, 6))
    sns.barplot(x="labels", y="trigrams", data=class_count)
    plt.ylabel('count')


    # Vector Representation of the Requirement Texts
    # ==================================================

    '''
    As before, we want to represent the requirements with a vector of tfidf weights.
    This time, we will also set some of the parameters of TfidfVectorizer
        - sublinear_tf: is set to True to use a logarithmic form for frequency.
        - min_df: the minimum numbers of documents a word must be present in to be kept
        - norm: set to l2 so that all feature vectors have a euclidian norm of 1
        - ngram_range is set to (1, 3) to indicate that we want to consider unigrams, bigrams, and trigrams.
    '''
    tfidf = TfidfVectorizer(sublinear_tf=True, min_df=1, norm="l2", ngram_range=(1, 2))
    features = tfidf.fit_transform(nfr.trigrams).toarray()
    labels_num = nfr.labels_num
    label_dict = {"LF": 1, "O": 2, "PE": 3, "SE": 4, "US": 5, "others": 6}  # mapping of labels and label_num



    # Chi-sq test to find the most relevant term (feature)
    # for each class
    # ======================================================

    '''
    - One common feature selection method that is used with text data is the Chi-Square feature selection.
    - The χ2 test is used in statistics to test the independence of two RVs.
    - In our case, we compute the chi-square score for each feature (term) and its corresponding class 
      and use it to test whether the occurrence of a specific term and the occurrence of a specific class 
      are independent.
    - For each term t (feature) in a corpus with 370 documents (my sample), we estimate its chi-sq 
      score with a specific class c.
    - For each feature (term), a high χ2 score indicates that the null hypothesis H0 
      (independence between the term and class) is rejected.
    - Thus, a high chi-sq score means that there IS dependence between term's frequency 
      and class c. I should include this term (feature) in my classifier.
    '''

    # Compute χ² (chi-squared) statistic for each class/feature combination.
    features_chi2 = chi2(features, labels_num == 1)

    num_most_important = 5
    for labels, cat_id in sorted(label_dict.items()):
        # I use labels_num == cat_id to create a boolean series where True means label_num of a row is equal to cat_id
        features_chi2 = chi2(features, labels_num == cat_id)

        # The indices of each of the 6357 features, sorted by least important (lowest chi-sq score) to the most important
        # (highest chi-sq score)
        # NOTE: np.argsort() return an array of index with the index of the element with the smallest value appearing first
        # np.argsort([3,1,2]) ---> array([1, 2, 0])
        indices = np.argsort(features_chi2[0])
        feature_names = np.array(tfidf.get_feature_names())[indices]  # least important term to the most important term

        unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
        unigram_str = '\n'.join(unigrams[-num_most_important:])
        bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
        bigram_str = '\n'.join(bigrams[-num_most_important:])

        print("############### '{} ###############':".format(labels))
        print("## Most correlated unigrams ##")
        print(unigram_str)
        print("")
        print("## Most correlated bigrams ##")
        print(bigram_str)
        print("")


    # Modelling
    # =====================
    '''
    - As before, I will first split the data into train and test datasets.
    - I will try 3 estimators: SVC, RandomForestClassifier, and AdaboostClassifier.
    - I will create a pipeline with the following steps:
        - tfidfvectorizer: represent each requirements with the tfidf weights of its tokens
        - TruncatedSVD: pick the most important features
        - clf: train classifier
    - For each estimator, I will use GridSearchCV to find its optimal hyperparameters based 
      on its estimated test f1-score (marcro).
    '''
    # Test harness
    X = nfr["trigrams"]
    y = nfr['labels_num'].values

    # Train test split with stratified sampling for evaluation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=10)

    # Classifiers
    models = {
        'SVC': SVC(random_state=10),
        'RandomForestClassifier': RandomForestClassifier(random_state=10),
        'AdaBoostClassifier': AdaBoostClassifier(random_state=10)
    }

    # Parameters for GridSearchCV
    params = {

        'SVC': {
            "clf__C": [1, 10, 100, 1000],  # [1,10,100,1000]
            "clf__gamma": [1, 0.1, 0.001, 0.0001],  # [1,0.1,0.001,0.0001]
        },

        'RandomForestClassifier': {
            "clf__n_estimators": [200, 400, 800, 1000, 1200],  # [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800]
            "clf__max_depth": [10, 30, 50, 80, 100],  # [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None]
            "clf__min_samples_split": [2, 5, 10],  # [2, 5, 10]
            "clf__min_samples_leaf": [1, 2, 4]  # [1, 2, 4]
        },

        'AdaBoostClassifier': {
            "clf__n_estimators": [100, 500, 800, 1000],  # [100, 500, 800, 1000]
            "clf__learning_rate": [0.01, 0.05, 0.1, 0.5, 1]  # [0.01,0.05,0.1,0.5,1]
        }
    }


    gscvs = []

    for name in models.keys():
        # Pipeline
        pipeline = Pipeline([('tfidf', tfidf),  # compute for each term t in doc d its tf-idf weight
                             ('lsa', TruncatedSVD(n_components=100, n_iter=10, random_state=10)),
                             # pick only 100 features
                             ('clf', models[name])])  # classifier

        est_params = params[name]  # parameters for that model

        # Define the GridSearchCV object for that model
        gscv = GridSearchCV(estimator=pipeline,
                            param_grid=est_params,
                            cv=5,
                            verbose=2,
                            n_jobs=-1,
                            scoring="f1_macro")

        # Train the GridSearchCV object
        gscv.fit(X_train, y_train)

        print("The best parameters are: {}".format(gscv.best_params_))
        print("")
        print("The best f1-macro score (on CV) are: {}".format(gscv.best_score_))

        gscvs.append(gscv)


    # Get the metrics of each model
    model_name, acc_score_list, precision_score_list, recall_score_list, f1_score_list = [], [], [], [], []
    for i, name in enumerate(models.keys()):
        # Get predictions
        y_pred = gscvs[i].predict(X_test)

        # model name
        model_name.append(name)

        # Model performance
        acc_score_list.append(accuracy_score(y_test, y_pred))
        # compute precision of each class and take average
        precision_score_list.append(precision_score(y_test, y_pred, average='macro'))
        recall_score_list.append(recall_score(y_test, y_pred, average='macro'))
        f1_score_list.append(f1_score(y_test, y_pred, average='macro'))

        # dataset and word vector representation columns
        datasets = ["nfr", "nfr", "nfr"]
        wv_types = ["tfidf", "tfidf", "tfidf"]

        # Organize metrics (on test dataset) for each model in a DataFrame
        model_comparison_df = pd.DataFrame(
            list(zip(datasets, wv_types, model_name, acc_score_list, precision_score_list,
                     recall_score_list, f1_score_list)),
            columns=['dataset', 'wv_type', 'model_name', 'accuracy_score',
                     'precision_score', 'recall_score', 'f1_score'])

        # sort by f1_score
        model_comparison_df = model_comparison_df.sort_values(by='f1_score', ascending=False)


    # Plots
    # =====================
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="model_name", y="f1_score", data=model_comparison_df, axes=ax)
    ax.set_title('nfr dataset (multiclass non-functional requirements classification)')
    plt.savefig("outputs/multi_class_classification_results_traditional.jpeg")


    # Model Evaluation
    # =====================

    model = gscvs[0]
    y_pred = model.predict(X_test)
    conf_mat = confusion_matrix(y_test, y_pred)

    # Heatmap for the confusion matrix
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.heatmap(conf_mat, annot=True, fmt='d', xticklabels=list(label_dict.keys()),
                yticklabels=list(label_dict.keys()))
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.savefig("outputs/multi_class_classification_svc_cm.jpeg")

    print(classification_report(y_test, y_pred, target_names=list(label_dict.keys())))


    # Outputs
    # =====================
    model_comparison_df.to_csv("outputs/multiclass_results_traditional.csv", index=False)











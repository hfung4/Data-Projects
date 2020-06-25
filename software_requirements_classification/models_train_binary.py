#! /usr/bin/env python

'''data'''
import pandas as pd
import numpy as np
import re
import pprint
import helpers
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.model_selection import train_test_split
from gensim.models import KeyedVectors
import warnings

warnings.filterwarnings("ignore")


# Clean some of the wierd ",,,,," in labels
def clean_labels(df):
    df["labels"] = df["labels"].map(lambda x: re.sub(",|\"", "", str(x)))
    df['labels'] = df['labels'].astype(str)


# counts of the levels of factor variables
def level_counts(df):
    # count of each level
    count = df["labels"].value_counts(dropna=False)
    # percentage of each level
    percent = round(df["labels"].value_counts(dropna=False, normalize=True) * 100, 3)

    # put it into a DataFrame
    return pd.concat([count, percent], axis=1, keys=["count", "percentage"])



def get_sentence_embeddings(doc):
    # only keep tokens in each sentence if they are a vocab in googlew2v
    tokens_in_embedding= [t for t in doc if t in googlew2v]
    sent_embedding = np.average([googlew2v[token] for token in tokens_in_embedding], axis=0)
    return sent_embedding


if __name__ == "__main__":

    # Import data
    # ==================================================
    # read the SecReq datasets
    CPN = pd.read_csv("data/CPN.csv", sep=";", names=["text", "labels"])
    GPS = pd.read_csv("data/GPS.csv", sep=";", names=["text", "labels"])
    ePurse = pd.read_csv("data/ePurse_selective.csv", sep=";", names=["text", "labels"])
    # read the nfr dataset
    nfr = pd.read_csv("data/nfr.csv")

    # Process data (labels)
    # ==================================================

    # A list of datasets
    datasets = [("CPN", CPN), ("GPS", GPS), ("ePurse", ePurse), ("nfr", nfr)]

    # Some basic cleaning
    for df in datasets[:-1]:
        clean_labels(df[1])

    # Check for imbalanced classes
    for df in datasets:
        print("{}:".format(df[0]))
        pprint.pprint(level_counts(df[1]))
        print("\n")

    # Drop rows with nan and "xyz" as labels

    # highly imbalanced: 80% nonsec, 20% sec
    CPN = CPN.loc[(CPN["labels"] == "sec") | (CPN["labels"] == "nonsec"), :]
    # imbalanced: 67 % nonsec, 32 % sec
    GPS = GPS.loc[(GPS["labels"] == "sec") | (GPS["labels"] == "nonsec"), :]
    # imbalanced: 66% nonsec, 33% sec
    ePurse = ePurse.loc[(ePurse["labels"] == "sec") | (ePurse["labels"] == "nonsec"), :]

    '''For the nfr dataset, there are some labels with very little samples.  
    I can try to group all classes with less than 7% to a single "other" class"'''
    temp = level_counts(nfr)
    # A list of classes that I want to group as "others"
    others = list(temp[temp.percentage < 5].index)
    nfr.loc[nfr.labels.isin(others), "labels"] = "others"

    '''Combine CPN, GPS, ePurse datasets into a single SeqReq dataset.  
    We will perform binary classification on this dataset'''
    SecReq = pd.concat([CPN, GPS, ePurse], axis=0)
    SecReq = SecReq.sample(frac=1).reset_index(drop=True)

    # Process data (requirement texts)
    # ==================================================

    # Process text
    helpers.process_text(SecReq)
    helpers.process_text(nfr)

    # Phrase modelling
    ''' ** Learn combinations of tokens that together represents meaningful multi-word phrases 
     ("United States", "happy hour") '''

    # Train Phraser model, get bigrams
    model_filepath = "models/secreq_bigrams_model"  # bigram model file path for SecReq
    helpers.get_bigrams(SecReq, model_filepath, True)

    model_filepath = "models/nfr_bigrams_model"  # bigram model file path for nfr
    helpers.get_bigrams(nfr, model_filepath, True)

    # Train Phraser model, get trigrams
    model_filepath = "models/secreq_trigrams_model"  # bigram model file path for SecReq
    helpers.get_trigrams(SecReq, model_filepath, True)

    model_filepath = "models/nfr_trigrams_model"  # bigram model file path for nfr
    helpers.get_trigrams(nfr, model_filepath, True)

    # Create a variant of the nfr dataset in which there are only two classes:
    # # functional (F) and non-functional (NF)
    nfr_binary = nfr.copy()
    nfr_binary["labels"].replace(["others", "US", "SE", "O", "PE", "LF"], "NF", inplace=True)

    # encode the labels to numeric value
    helpers.encode_label(SecReq)
    helpers.encode_label(nfr)
    helpers.encode_label(nfr_binary)

    secreq_texts = SecReq['trigrams'].astype('str')
    nfr_texts = nfr_binary_texts = nfr['trigrams'].astype('str')

    # Binary Classification for the SecReq dataset
    # ==================================================
    '''    
    Pipeline for modelling:
    - Convert the transformed text (with trigrams) to a matrix of tf-idf weights (features).
    - The matrix would contain the tf-idf scores of each token t in each of the document in the corpus.
    - Perform TruncatedSVD to reduce the number of features-- this is important since our sample size 
      is small, a large feature set will lead to overfitting.
    - Modelling: use SVC, RandomForest and Adaboost
    - Tune hyperparameters with GridSearchCV
    '''

    # Test harness
    X = secreq_texts
    y = SecReq['labels_num'].values

    # Train test split with stratified sampling for evaluation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=10)

    # Classifiers
    models = {
        'SVC': SVC(random_state=10),
        'RandomForestClassifier': RandomForestClassifier(random_state=10),
        'AdaBoostClassifier': AdaBoostClassifier(random_state=10)
    }

    # Parameters for GridSearchCV
    # Use a dictionary of dictionaries to set the param grid for each of the models
    '''
    SVC:
    C = the regularization parameter, penalize model complexity
    gamma = kernel coefficient for ‘rbf’ 

    Random Forest:
    n_estimators = number of trees in the foreset
    max_features = max number of features considered for splitting a node
    max_depth = max number of levels in each decision tree
    min_samples_split = min number of data points placed in a node before the node is split
    min_samples_leaf = min number of data points allowed in a leaf node

    AdaBoost:
    n_estimators = number of estimators in the boosted ensemble to use.
    learning_rate= Learning rate shrinks the contribution of each classifier by learning_rate. 
    '''

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

    # Modelling
    df_secreq_tfidf = helpers.models_training("SecReq", "tfidf", X_train, y_train,
                                              X_test, y_test, models, params, True)

    print(df_secreq_tfidf)


    # Binary Classification for the nfr_binary dataset
    # ==================================================

    # Test harness
    X = nfr_binary_texts
    y = nfr_binary['labels_num'].values

    # Train test split with stratified sampling for evaluation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=10)

    # Modelling
    df_nfr_binary_tfidf = helpers.models_training("nfr_binary", "tfidf", X_train, y_train,
                                          X_test, y_test, models, params, True)

    print(df_nfr_binary_tfidf)


    # Load pre-trained Word Embeddings
    # =======================================

    # The vectors is loaded from an existing file on disk in the original Google’s word2vec C format as
    # a KeyedVectors instance
    googlew2v = KeyedVectors.load_word2vec_format('embeddings/GoogleNews-vectors-negative300.bin.gz',
                                                  binary=True)  # C bin format

    # Convert the transformed requirements from each dataset a list of lists of tokens
    nfr_docs = nfr.trigrams.tolist()
    secreq_docs = SecReq.trigrams.tolist()

    # Get the sentence embeddings of each of the 625 requirements in the nfr dataset
    # For each requirements, I get the 300x1 word embedding for each token, and then take the average
    # to get a 300x1 sentence embedding
    sent_embeddings_nfr = [get_sentence_embeddings(doc) for doc in nfr_docs]
    sent_embeddings_nfr = np.concatenate(sent_embeddings_nfr, axis=0)
    sent_embeddings_nfr = sent_embeddings_nfr.reshape((625, 300))

    sent_embeddings_secreq = [get_sentence_embeddings(doc) for doc in
                              secreq_docs]  # a list of 471 ndarrays of 300 elements
    sent_embeddings_secreq = np.concatenate(sent_embeddings_secreq, axis=0)  # an ndarray of 471x300=141300 elements
    sent_embeddings_secreq = sent_embeddings_secreq.reshape((471, 300))


    # Binary Classification for the SecReq dataset
    # (with pre-trained word embeddings)
    # ============================================

    # Test harness
    X = sent_embeddings_secreq
    y = SecReq['labels_num'].values

    # Train test split with stratified sampling for evaluation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=10)

    df_secreq_wv = helpers.models_training("SecReq", "pre_trained_wv", X_train, y_train,
                                   X_test, y_test, models, params, True)


    # Binary Classification for the nfr dataset
    # (with pre-trained word embeddings)
    # ===========================================

    # Test harness
    X = sent_embeddings_nfr
    y = nfr_binary['labels_num'].values

    # Train test split with stratified sampling for evaluation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=10)

    df_nfr_binary_wv = helpers.models_training("nfr_binary", "pre_trained_wv", X_train, y_train, X_test,
                                       y_test, models, params, True)



    # Results
    # =========================

    binary_results = pd.concat([df_secreq_tfidf, df_nfr_binary_tfidf, df_secreq_wv, df_nfr_binary_wv], axis=0)

    secreq_binary_results = binary_results[binary_results.dataset == "SecReq"]
    nfr_binary_results = binary_results[binary_results.dataset == "nfr_binary"]

    # Plots
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    sns.barplot(x="model_name", y="f1_score", hue="wv_type", data=secreq_binary_results, ax=axes[0])
    sns.barplot(x="model_name", y="f1_score", hue="wv_type", data=nfr_binary_results, ax=axes[1])

    axes[0].title.set_text('SeqReq Dataset')
    axes[1].title.set_text('nfr binary Dataset')

    plt.savefig("outputs/binary_classification_results_traditional.jpeg")

    # Save results tables
    binary_results.to_csv("outputs/binary_classification_results_traditional.csv", index=False)
    SecReq.to_csv("processed_data/SecReq_processed.csv", index=False)
    nfr.to_csv("processed_data/nfr_processed.csv", index=False)
    nfr_binary.to_csv("processed_data/nfr_binary_processed.csv", index=False)




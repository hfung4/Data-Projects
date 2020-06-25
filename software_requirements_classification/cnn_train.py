#! /usr/bin/env python


import pandas as pd
import numpy as np
import re
import helpers
import matplotlib.pyplot as plt
import seaborn as sns
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical
from keras.models import Sequential, Model
from keras.layers import Embedding, Flatten, Dense, Input, Conv1D, Conv2D, MaxPooling1D, MaxPooling2D, GlobalMaxPooling1D
from keras.layers import Dropout, concatenate
from keras.layers.core import Reshape
from keras.callbacks import EarlyStopping
from keras.optimizers import SGD, RMSprop, Adam
from keras import regularizers
from gensim.models import Word2Vec
from gensim.models.keyedvectors import KeyedVectors
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import precision_score, recall_score, f1_score, auc, roc_curve
from sklearn.model_selection import train_test_split
import warnings

warnings.filterwarnings("ignore")

'''
In general, pre-trained word embeddings are particularly useful on problems 
where there is very little training data (otherwise, I should train my word-embeddings 
on the corpus). This is suitable to requirement classification since we usually don't 
have a large set of labelled data. The labelling of software requirements need to be 
done manually by individual with domain expertise; thus even at Logapps, we only had a 
train dataset (labelled by trained interns in the previous summers) of about 5000 samples.
'''

if __name__ == "__main__":

    # Import processed data
    # ==================================================
    SecReq = pd.read_csv("processed_data/SecReq_processed.csv")
    nfr = pd.read_csv("processed_data/nfr_processed.csv")
    nfr_binary = pd.read_csv("processed_data/nfr_binary_processed.csv")


    # Process text
    # ==================================================

    '''
    We no longer need to identify bigrams and trigrams using Phrase models 
    ourselves since we are using CNN models. We can define filters of size 2 and 3 
    (bigrams and trigrams) and during training, CNN will automatically (using backpropogation) 
    extract/identify features (two or three word phrases) that are informative in predicting 
    the class of the requirements.
    '''
    # remove all functional class, I am only interested in classifying non-functional
    # requirements to their subtypes
    nfr = nfr.loc[nfr.labels!="F", :]

    SecReq = SecReq[["text", "labels_num"]]
    nfr = nfr[["text", "labels_num"]]
    nfr_binary = nfr_binary[["text", "labels_num"]]

    # Load KeyedVectors for the Google News word embeddings
    # Contains 3 million 300-D word embeddings trained from 100 billion words

    # Load pretrained model (since intermediate data is not included, the model cannot be refined with additional data)
    # The vectors is loaded from an existing file on disk in the original Google’s word2vec C format as
    # a KeyedVectors instance
    word_vectors = KeyedVectors.load_word2vec_format('embeddings/GoogleNews-vectors-negative300.bin.gz',
                                                     binary=True)  # C bin format


    # Binary Classification with SecReq Dataset
    # ==================================================

    # Process the text and build the embedding matrix
    texts = SecReq["text"]
    labels = SecReq["labels_num"]

    X_train, X_val, y_train, y_val, embedding_matrix = helpers.keras_processing(texts, labels,
                                                                                1000, 75,
                                                                                word_vectors)


    # Modelling

    '''
    As per Kim Yoon's "Convolutional Neural Networks for Sentence Classification", 
    we will only use conv layer to extract features using filter_size 1,2 and 3.
    The size of the filter is (filter_size, embeding_dim). If filter_size = 1, I 
    will only extract unigram features; and if filter_size=2, I will extract bigrams features.
    I will use 1-max pooling to get the max value of the feature map of each filter.
    Thus, if I have 6 filters, I will get a 6x1 vector after the 1-max pooling.
    Finally, I will have a fully connected layer and softmax layer.
    '''

    # Settings
    sequence_length = X_train.shape[1]  # number of words in each doc
    filter_sizes = [1, 2]  # filter size for conv layer 1, and for conv layer 2  (consider unigrams and bigrams)
    num_filters = 128  # number of filters for each conv layer
    drop = 0.5  # probability of dropping neurons

    vocabulary_size = embedding_matrix.shape[0]
    embedding_dim = embedding_matrix.shape[1]

    # Embedding Layer
    embedding_layer = Embedding(vocabulary_size,
                                embedding_dim,
                                weights=[embedding_matrix],
                                trainable=False)

    # Build Model

    # The input to the embeddings layer for each doc is bascially an array of word index of length "sequence_length",
    # the length of each doc
    inputs = Input(shape=(sequence_length,))
    # Emedding layer:
    # Input: word index of shape (75,)
    # output: a 3D tensor of shape (samples, sequence_length, embedding_dim) = (samples, 75, 300)
    embedding = embedding_layer(inputs)
    # reshape the output of the embedding layer to shape (75, 300, 1 )
    reshape = Reshape((sequence_length, embedding_dim, 1))(embedding)

    # conv layer 1 (use filter window size 1: extract unigrams)
    # input is the "reshaped" embedding matrix
    conv_0 = Conv2D(num_filters,  # number of filters (50)
                    (filter_sizes[0], embedding_dim),  # shape of the filter
                    activation='relu',  # activation function
                    # Regularizers allow you to apply penalties on layer parameters or layer activity during optimization.
                    # These penalties are summed into the loss function that the network optimizes.
                    kernel_regularizer=regularizers.l2(0.01))(reshape)

    # conv layer 2 (use filter window size 2: extract bigrams)
    # input is the "reshaped" embedding matrix
    conv_1 = Conv2D(num_filters,
                    (filter_sizes[1], embedding_dim),
                    activation='relu',
                    kernel_regularizer=regularizers.l2(0.01))(reshape)

    # Apply max pooling to the activation maps (100 of them) for EACH conv layer
    # sequence_length - filter_sizes[0] + 1 is the length of Each feature map
    maxpool_0 = MaxPooling2D((sequence_length - filter_sizes[0] + 1, 1), strides=(1, 1))(conv_0)  # size of 1x100
    maxpool_1 = MaxPooling2D((sequence_length - filter_sizes[1] + 1, 1), strides=(1, 1))(conv_1)

    # I get a feature from each of the 1-max pooling layer, so I have 2 features in total
    # I concat the features to get a 2 feature vector of size 2x100
    merged_tensor = concatenate([maxpool_0, maxpool_1], axis=1)
    flatten = Flatten()(merged_tensor)

    dropout = Dropout(drop)(flatten)
    output = Dense(2, activation='sigmoid', kernel_regularizer=regularizers.l2(0.01))(dropout)

    # Creates a model class with takes a Keras.Input object and the outputs of the model as argument
    model = Model(inputs, output)

    # Train Model
    # compile and train the network
    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy',
                  metrics=['acc'])

    # Use early stopping
    # callbacks = [EarlyStopping(monitor='val_loss')]

    history = model.fit(X_train, y_train,
                        epochs=30,
                        batch_size=64,
                        validation_data=(X_val, y_val))

    # Plot model performance over epochs
    train_acc = history.history["acc"]  # train accuracy of each of the 10 train epoch
    validation_acc = history.history["val_acc"]
    train_loss = history.history["loss"]
    validation_loss = history.history["val_loss"]
    epochs = range(1, len(train_acc) + 1, 1)

    fig, axes = plt.subplots(1, 2, figsize=(10, 6))
    axes[0].plot(epochs, train_acc, 'bo', label="Training acc")
    axes[0].plot(epochs, validation_acc, 'b', label="Validation acc")
    axes[0].set_title("Training and validation accuracy")
    axes[0].set_ylabel("accuracy")
    axes[0].set_xlabel("epoch")

    axes[1].plot(epochs, train_loss, 'bo', label="Training loss")
    axes[1].plot(epochs, validation_loss, 'b', label="Validation loss")
    axes[1].set_title("Training and validation loss")
    axes[1].set_ylabel("loss")
    axes[1].set_xlabel("epoch")

    # Results

    # Empty lists of model name and model performance metrics
    model_name, acc_score_list, precision_score_list, recall_score_list, f1_score_list = [], [], [], [], []

    # make predictions
    y_pred = model.predict(X_val)
    # Get the predicted class by taking the max probability
    y_pred_classes = np.argmax(y_pred, axis=1)
    # Get the predicted classes of y_val
    y_val_classes = [np.argmax(y, axis=None, out=None) for y in y_val]
    y_val_classes = np.asarray(y_val_classes)

    # Update model performance lists

    # Model performance
    acc_score_list.append(accuracy_score(y_val_classes, y_pred_classes))
    # compute precision of each class and take average
    precision_score_list.append(precision_score(y_val_classes, y_pred_classes))
    recall_score_list.append(recall_score(y_val_classes, y_pred_classes))
    f1_score_list.append(f1_score(y_val_classes, y_pred_classes))
    # model name
    model_name.append("CNN (SeqReq)")


    # Binary Classification with nfr_binary Dataset
    # ==================================================
    texts = nfr_binary["text"]
    labels = nfr_binary["labels_num"]

    X_train, X_val, y_train, y_val, embedding_matrix = helpers.keras_processing(texts,
                                                                                labels,
                                                                                1000,
                                                                                75,
                                                                                word_vectors)

    # Modelling
    sequence_length = X_train.shape[1]  # number of words in each doc
    filter_sizes = [1, 2]  # filter size for conv layer 1, and for conv layer 2  (consider unigrams and bigrams)
    num_filters = 64  # number of filters for each conv layer
    drop = 0.5  # probability of dropping neurons

    vocabulary_size = embedding_matrix.shape[0]
    embedding_dim = embedding_matrix.shape[1]

    embedding_layer = Embedding(vocabulary_size,
                                embedding_dim,
                                weights=[embedding_matrix],
                                trainable=False)


    inputs = Input(shape=(sequence_length,))
    embedding = embedding_layer(inputs)
    reshape = Reshape((sequence_length, embedding_dim, 1))(embedding)
    conv_0 = Conv2D(num_filters,
                    (filter_sizes[0], embedding_dim),
                    activation='relu',
                    kernel_regularizer=regularizers.l2(0.01))(reshape)
    conv_1 = Conv2D(num_filters,
                    (filter_sizes[1], embedding_dim),
                    activation='relu',
                    kernel_regularizer=regularizers.l2(0.01))(reshape)
    maxpool_0 = MaxPooling2D((sequence_length - filter_sizes[0] + 1, 1), strides=(1, 1))(conv_0)  # size of 1x100
    maxpool_1 = MaxPooling2D((sequence_length - filter_sizes[1] + 1, 1), strides=(1, 1))(conv_1)
    merged_tensor = concatenate([maxpool_0, maxpool_1], axis=1)
    flatten = Flatten()(merged_tensor)
    dropout = Dropout(drop)(flatten)
    output = Dense(2, activation='sigmoid', kernel_regularizer=regularizers.l2(0.01))(dropout)

    # Creates a model class with takes a Keras.Input object and the outputs of the model as argument
    model = Model(inputs, output)

    # Train Model

    # compile and train the network
    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    # Use early stopping
    # callbacks = [EarlyStopping(monitor='val_loss')]

    history = model.fit(X_train, y_train,
                        epochs=100,
                        batch_size=64,
                        validation_data=(X_val, y_val),
                        verbose=0)

    # Plot model performance over epochs
    train_acc = history.history["acc"]  # train accuracy of each of the 10 train epoch
    validation_acc = history.history["val_acc"]
    train_loss = history.history["loss"]
    validation_loss = history.history["val_loss"]
    epochs = range(1, len(train_acc) + 1, 1)

    fig, axes = plt.subplots(1, 2, figsize=(10, 6))
    axes[0].plot(epochs, train_acc, 'bo', label="Training acc")
    axes[0].plot(epochs, validation_acc, 'b', label="Validation acc")
    axes[0].set_title("Training and validation accuracy")
    axes[0].set_ylabel("accuracy")
    axes[0].set_xlabel("epoch")

    axes[1].plot(epochs, train_loss, 'bo', label="Training loss")
    axes[1].plot(epochs, validation_loss, 'b', label="Validation loss")
    axes[1].set_title("Training and validation loss")
    axes[1].set_ylabel("loss")
    axes[1].set_xlabel("epoch")


    # Results

    # make predictions
    y_pred = model.predict(X_val)
    # Get the predicted class by taking the max probability
    y_pred_classes = np.argmax(y_pred, axis=1)
    # Get the predicted classes of y_val
    y_val_classes = [np.argmax(y, axis=None, out=None) for y in y_val]
    y_val_classes = np.asarray(y_val_classes)

    # Update model performance lists

    # Model performance
    acc_score_list.append(accuracy_score(y_val_classes, y_pred_classes))
    # compute precision of each class and take average
    precision_score_list.append(precision_score(y_val_classes, y_pred_classes))
    recall_score_list.append(recall_score(y_val_classes, y_pred_classes))
    f1_score_list.append(f1_score(y_val_classes, y_pred_classes))
    # model name
    model_name.append("CNN (nfr_binary)")


    # Multiclass classification with nfr_binary Dataset
    # ==================================================

    texts = nfr["text"]
    labels = nfr["labels_num"] - 1  # shift all labels_num to the left

    X_train, X_val, y_train, y_val, embedding_matrix = helpers.keras_processing(texts,
                                                                                labels,
                                                                                1000,
                                                                                75,
                                                                                word_vectors)

    # Modelling
    sequence_length = X_train.shape[1]  # number of words in each doc
    filter_sizes = [1, 2]  # filter size for conv layer 1, and for conv layer 2  (consider unigrams and bigrams)
    num_filters = 64  # number of filters for each conv layer
    drop = 0.5  # probability of dropping neurons

    vocabulary_size = embedding_matrix.shape[0]
    embedding_dim = embedding_matrix.shape[1]

    embedding_layer = Embedding(vocabulary_size,
                                embedding_dim,
                                weights=[embedding_matrix],
                                trainable=False)

    inputs = Input(shape=(sequence_length,))
    embedding = embedding_layer(inputs)
    reshape = Reshape((sequence_length, embedding_dim, 1))(embedding)
    conv_0 = Conv2D(num_filters,
                    (filter_sizes[0], embedding_dim),
                    activation='relu',
                    kernel_regularizer=regularizers.l2(0.01))(reshape)
    conv_1 = Conv2D(num_filters,
                    (filter_sizes[1], embedding_dim),
                    activation='relu',
                    kernel_regularizer=regularizers.l2(0.01))(reshape)
    maxpool_0 = MaxPooling2D((sequence_length - filter_sizes[0] + 1, 1), strides=(1, 1))(conv_0)  # size of 1x100
    maxpool_1 = MaxPooling2D((sequence_length - filter_sizes[1] + 1, 1), strides=(1, 1))(conv_1)
    merged_tensor = concatenate([maxpool_0, maxpool_1], axis=1)
    flatten = Flatten()(merged_tensor)
    dropout = Dropout(drop)(flatten)
    output = Dense(6, activation='softmax', kernel_regularizer=regularizers.l2(0.01))(dropout)

    # Creates a model class with takes a Keras.Input object and the outputs of the model as argument
    model = Model(inputs, output)

    # Train Model

    # compile and train the network
    model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    # Use early stopping
    # callbacks = [EarlyStopping(monitor='val_loss')]

    history = model.fit(X_train, y_train,
                        epochs=140,
                        batch_size=128,
                        validation_data=(X_val, y_val),
                        verbose=0)

    # Plot

    # Plot model performance over epochs
    train_acc = history.history["acc"]  # train accuracy of each of the 10 train epoch
    validation_acc = history.history["val_acc"]
    train_loss = history.history["loss"]
    validation_loss = history.history["val_loss"]
    epochs = range(1, len(train_acc) + 1, 1)

    fig, axes = plt.subplots(1, 2, figsize=(10, 6))
    axes[0].plot(epochs, train_acc, 'bo', label="Training acc")
    axes[0].plot(epochs, validation_acc, 'b', label="Validation acc")
    axes[0].set_title("Training and validation accuracy")
    axes[0].set_ylabel("accuracy")
    axes[0].set_xlabel("epoch")

    axes[1].plot(epochs, train_loss, 'bo', label="Training loss")
    axes[1].plot(epochs, validation_loss, 'b', label="Validation loss")
    axes[1].set_title("Training and validation loss")
    axes[1].set_ylabel("loss")
    axes[1].set_xlabel("epoch")


    # Results

    # make predictions
    y_pred = model.predict(X_val)
    # Get the predicted class by taking the max probability
    y_pred_classes = np.argmax(y_pred, axis=1)
    # Get the predicted classes of y_val
    y_val_classes = [np.argmax(y, axis=None, out=None) for y in y_val]
    y_val_classes = np.asarray(y_val_classes)

    # Update model performance lists
    acc = accuracy_score(y_val_classes, y_pred_classes)
    precision = precision_score(y_val_classes, y_pred_classes, average="macro")
    recall = recall_score(y_val_classes, y_pred_classes, average="macro")
    f1 = f1_score(y_val_classes, y_pred_classes, average="macro")

    # Model performance
    acc_score_list.append(acc)
    # compute precision of each class and take average
    precision_score_list.append(precision)
    recall_score_list.append(recall)
    f1_score_list.append(f1)
    # model name
    model_name.append("CNN (nfr_multiclass)")

    # Confusion Matrix
    conf_mat = confusion_matrix(y_val_classes, y_pred_classes)

    label_dict = {"LF": 0, "O": 1, "PE": 2, "SE": 3, "US": 4, "others": 5}  # mapping of labels and label_num

    fig, ax = plt.subplots(figsize=(10, 10))

    sns.heatmap(conf_mat, annot=True, fmt='d', xticklabels=list(label_dict.keys()), yticklabels=list(label_dict.keys()))
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.savefig("outputs/multi_class_classification_cnn_cm.jpeg")

    print(classification_report(y_val_classes, y_pred_classes, target_names=list(label_dict.keys())))


    # Model Comparison
    # ===========================

    binary_results_trad = pd.read_csv("outputs/binary_classification_results_traditional.csv")
    multiclass_results_trad = pd.read_csv("outputs/multiclass_results_traditional.csv")

    binary_results_cnn = pd.DataFrame({"dataset": ["SecReq", "nfr_binary"],
                                       "wv_type": ["pre_trained_wv", "pre_trained_wv"],
                                       "model_name": ["CNN", "CNN"],
                                       "accuracy_score": [acc_score_list[0], acc_score_list[1]],
                                       "precision_score": [precision_score_list[0], precision_score_list[1]],
                                       "recall_score": [recall_score_list[0], recall_score_list[1]],
                                       "f1_score": [f1_score_list[0], f1_score_list[1]]})

    multiclass_results_cnn = pd.DataFrame({"dataset": ["nfr"],
                                           "wv_type": ["pre_trained_wv"],
                                           "model_name": ["CNN"],
                                           "accuracy_score": [acc_score_list[2]],
                                           "precision_score": [precision_score_list[2]],
                                           "recall_score": [recall_score_list[2]],
                                           "f1_score": [f1_score_list[2]]})

    # Binary Classification Results
    binary_results_all = pd.concat([binary_results_trad, binary_results_cnn], axis=0)
    binary_results_all = binary_results_all.groupby(['dataset'], sort=False).apply(lambda x: x.sort_values(["f1_score"],
                                                                                                           ascending=False))
    binary_results_all.to_csv("outputs/final_model_comparison/binary_classification_results.csv", index=False)

    # Plots- Binary classification model comparisions
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    p1 = sns.barplot(x="model_name", y="f1_score", data=binary_results_all[binary_results_all.dataset == "SecReq"],
                     ax=axes[0])
    p2 = sns.barplot(x="model_name", y="f1_score", data=binary_results_all[binary_results_all.dataset == "nfr_binary"],
                     ax=axes[1])

    axes[0].title.set_text('SeqReq Dataset')
    axes[1].title.set_text('nfr binary Dataset')

    p1.set_xticklabels(p1.get_xticklabels(), rotation=45)
    p2.set_xticklabels(p2.get_xticklabels(), rotation=45)

    plt.savefig("outputs/final_model_comparison/binary_classification_results_all.jpeg")


    # Multiclass Classification Results

    multiclass_results_all = pd.concat([multiclass_results_trad, multiclass_results_cnn], axis=0)
    multiclass_results_all = multiclass_results_all.sort_values("f1_score", ascending=False)
    multiclass_results_all.to_csv("outputs/final_model_comparison/multiclass_classification_results.csv",
                                  index=False)

    # Plots- Multiclass classification model comparisions
    fig, axes = plt.subplots(1, 1, figsize=(16, 8))
    p1 = sns.barplot(x="model_name", y="f1_score", data=multiclass_results_all,
                     ax=axes)
    axes.title.set_text('nfr Dataset')
    p1.set_xticklabels(p1.get_xticklabels(), rotation=45)

    plt.savefig("outputs/final_model_comparison/multiclass_classification_results_all.jpeg")









import re
import numpy as np
import pandas as pd
from gensim.models.phrases import Phrases, Phraser
from keras.utils import to_categorical
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import spacy
from sklearn.preprocessing import LabelEncoder
import pickle
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, recall_score, precision_score
from sklearn.metrics import roc_auc_score, f1_score, roc_curve, auc, confusion_matrix

# load spaCy
nlp = spacy.load('en_core_web_sm')

''' This function clean strings and put it in lower caps. '''


def clean_str(df):
    # Regex pattern for only alphanumeric, hyphenated text with 3 or more chars
    pattern = re.compile(r"[A-Za-z0-9\-]{3,50}")
    df["processed_text"] = df["text"].str.findall(pattern).str.join(' ')

    return df


''' This function detract words like "aren't" to "are not" '''
# Contraction map
c_dict = {
    "ain't": "am not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "i'd": "I would",
    "i'd've": "I would have",
    "i'll": "I will",
    "i'll've": "I will have",
    "i'm": "I am",
    "i've": "I have",
    "isn't": "is not",
    "it'd": "it had",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so is",
    "that'd": "that would",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there had",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we had",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'alls": "you alls",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you had",
    "you'd've": "you would have",
    "you'll": "you you will",
    "you'll've": "you you will have",
    "you're": "you are",
    "you've": "you have"
}

c_re = re.compile('(%s)' % '|'.join(c_dict.keys()))


def expandContractions(text, c_re=c_re):
    def replace(match):
        return c_dict[match.group(0)]

    return c_re.sub(replace, text)


''' This function takes each token in doc and convert them the lowercase and lemmatize.  
Then it converts each lemmatized token into a string. The output of this function is a set 
lists of lemmatized strings. '''


def lemmatize_pipe(doc):
    lemma_list = [str(tok.lemma_).lower() for tok in doc
                  if tok.is_alpha and tok.text.lower() not in nlp.Defaults.stop_words]
    return lemma_list


'''Processing texts as a stream is usually more efficient than processing them one-by-one. 
This can be done by calling a nlp language pipe, which internally divides the data into batches and then applying functions
such as "lemmatize" to each data batch. By doing so, I can reduce the number of Python function calls and thus improve 
computation time.'''


def preprocess_pipe(texts):
    preproc_pipe = []
    # Define a nlp.pipe object.  The inputs are texts (DataFrame column) and batch size.
    for doc in nlp.pipe(texts, batch_size=20):  # nlp.pipe streams a sequence of spaCy document objects.
        preproc_pipe.append(lemmatize_pipe(doc))  # Apply lemmatize_pipe() to each spaCy document object
    return preproc_pipe


''' This function uses the above functions: clean_str(), expandContractions(), and preprocess_pipe()
to clean each sentence, perform decontraction and lemmatization and remove stopwords'''


def process_text(df):
    # clean text: drop all texts except for alphanumeric chars and hyphenated text with 3 or more chars
    clean_str(df)
    # decontract words like "aren't" to "are not"
    df["processed_text"] = df["processed_text"].map(lambda x: expandContractions(x))
    # stream texts in batches, and apply lemmatization to each batch
    df["processed_text"] = preprocess_pipe(df["processed_text"])


''' This function trains a first order phrase model and apply it to processed sentences'''


def get_bigrams(df, bigram_model_filepath, TRAIN):
    if TRAIN:  # train phrase model
        # Train the phrase model using the processed sentences (a list of list of strings)
        sentences_unigrams = df["processed_text"].tolist()
        bigram_phrase_model = Phrases(sentences_unigrams)
        # Use the Phraser function to turn the phrase model into a "Phraser" object,
        # which is optimized for speed and memory use
        bigram_phrase_model = Phraser(bigram_phrase_model)
        # Save the model for future use
        bigram_phrase_model.save(bigram_model_filepath)
    else:
        # Load the trained model from disk
        bigram_phrase_model = Phraser.load(bigram_model_filepath)

    # Get the first-order transofmred data
    df["bigrams"] = df["processed_text"].map(lambda x: bigram_phrase_model[x])


''' This function trains a second order phrase model and apply it to sentences with bigrams'''


def get_trigrams(df, trigram_model_filepath, TRAIN):
    if TRAIN:  # train phrase model
        # Train the phrase model using the bigram sentences (a list of list of strings)
        sentences_bigrams = df["bigrams"].tolist()
        trigram_phrase_model = Phrases(sentences_bigrams)
        # Use the Phraser function to turn the phrase model into a "Phraser" object,
        # which is optimized for speed and memory use
        trigram_phrase_model = Phraser(trigram_phrase_model)
        # Save the model for future use
        trigram_phrase_model.save(trigram_model_filepath)
    else:
        # Load the trained model from disk
        trigram_phrase_model = Phraser.load(trigram_model_filepath)

    # Get the second-order transformed data
    df["trigrams"] = df["bigrams"].map(lambda x: trigram_phrase_model[x])


'''This function encodes the categorical labels'''


# Encode the labels
def encode_label(df):
    le = LabelEncoder()
    df['labels_num'] = le.fit_transform(df['labels'])


'''This function define the pipline for each model, and perform GridSearchCV to find the optimal hyperparameters
for each model'''


def fit_assess_pipeline(X_train, y_train, models, params, dataset_name, wv_type):
    '''
    Fits the list of models with the training data one at a time and obtain
    the "best" test error (from CV) for each model
    '''
    gscvs = []  # a list of trained GridSearchCV objects

    for name in models.keys():

        # Define pipeline
        if wv_type == "tfidf":
            # compute for each term t in doc d its tf-idf weight
            pipeline = Pipeline([('tfidf', TfidfVectorizer()),
                                 ('lsa', TruncatedSVD(n_components=100, n_iter=10, random_state=10)),
                                 # pick only 100 features
                                 ('clf', models[name])])  # classifier
        else:
            pipeline = Pipeline([('clf', models[name])])  # classifier

        est_params = params[name]  # parameters for that model

        # Define the GridSearchCV object for that model
        gscv = GridSearchCV(estimator=pipeline,
                            param_grid=est_params,
                            cv=5,
                            verbose=2,
                            n_jobs=-1)

        # Train the GridSearchCV object
        gscv.fit(X_train, y_train)

        print("The best parameters are: {}".format(gscv.best_params_))
        print("")
        print("The best accuracy score (on CV) are: {}".format(gscv.best_score_))

        # save GridSerchCV object
        model_path = "models/" + dataset_name + "_" + wv_type + "_" + name + ".sav"
        with open(model_path, 'wb') as f:  # write binary (file mode)
            pickle.dump(gscv, f)

        gscvs.append(gscv)

    return gscvs


'''Function to get the scores for each model in a df'''


def model_score(GsCV, models, X_test, y_test, dataset_name, wv_type):
    model_name, acc_score_list, precision_score_list, recall_score_list, f1_score_list = [], [], [], [], []

    for i, name in enumerate(models.keys()):
        # Get predictions
        y_pred = GsCV[i].predict(X_test)

        # model name
        model_name.append(name)

        # Model performance
        acc_score_list.append(accuracy_score(y_test, y_pred))
        # compute precision of each class and take average
        precision_score_list.append(precision_score(y_test, y_pred, average='macro'))
        recall_score_list.append(recall_score(y_test, y_pred, average='macro'))
        f1_score_list.append(f1_score(y_test, y_pred, average='macro'))

    # Organize metrics (on test dataset) for each model in a DataFrame
    model_comparison_df = pd.DataFrame(list(zip(model_name, acc_score_list, precision_score_list,
                                                recall_score_list, f1_score_list)),
                                       columns=['model_name', 'accuracy_score', 'precision_score', 'recall_score',
                                                'f1_score'])

    # sort by f1_score
    model_comparison_df = model_comparison_df.sort_values(by='f1_score', ascending=False)

    model_comparison_df["dataset"] = dataset_name
    model_comparison_df["wv_type"] = wv_type
    model_comparison_df = model_comparison_df[["dataset", "wv_type", 'model_name', 'accuracy_score',
                                               'precision_score', 'recall_score', 'f1_score']]

    return model_comparison_df


'''Function to perform GridSearchCV and evaluate the models with the "best" hyperparameters on the testd dataset'''


def models_training(dataset_name, wv_type, X_train, y_train, X_test, y_test, models, params, TRAIN):
    if TRAIN:
        GsCVs = fit_assess_pipeline(X_train, y_train, models, params, dataset_name, wv_type)
    else:
        GsCVs = []
        for name in models.keys():
            # load trained GridSearchCV object from disk
            model_path = "models/" + dataset_name + "_" + wv_type + "_" + name + ".sav"
            with open(model_path, 'rb') as f:
                GsCVs.append(pickle.load(f))

    model_comparison_df = model_score(GsCVs, models, X_test, y_test, dataset_name, wv_type)
    return model_comparison_df


'''This function performs text processing, builds the word index, and creates the test harness and embedding matrix '''


def keras_processing(texts, labels, max_words, maxlen):
    # one-hot encode ("categorical encode") the labels
    labels = to_categorical(labels)  # an array of array[0,1]
    # Convert labels to an array
    labels = np.asarray(labels)

    max_words = max_words  # considers only the top 1000 words in the train dataset
    maxlen = maxlen  # cut the requirement after maxlen words

    # init the keras tokenizer, configured to only take into account the 10000 most common words
    # take lowercase and filter out non alphanumeric symbols
    tokenizer = Tokenizer(num_words=max_words,
                          filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
                          lower=True)

    tokenizer.fit_on_texts(texts)  # builds the word index
    sequences = tokenizer.texts_to_sequences(texts)  # turn strings into lists of integer indices (one list per doc)
    word_index = tokenizer.word_index  # get the word index that the tokenizer computed
    print("Found {} unique tokens.".format(len(word_index)))

    # Turn sequences-- lists of integers (word indices) into a 2D integer tensor of shape
    # (number of train observations, maxlen of each doc)
    data = pad_sequences(sequences, maxlen=maxlen)
    # print(data)

    print("")
    print("The shape of the data tensor is:".format(data.shape))
    print("")
    print("The shape of the label tensor is: {}".format(labels.shape))

    # Split the data into test and train set
    X_train, X_val, y_train, y_val = train_test_split(data, labels, stratify=labels, test_size=0.2,
                                                      random_state=10)

    # Build an Embedding Matrix that I can load to the Embedding layer

    # Embedding layer: a dictionary that mpas integer word indices to dense vector representations,
    # it takes a word index, looks up the index in an internal dictionary, and outputs its associated word vectors.

    # Embedding matrix is a matrix of shape (max_words= 10000, embedding dim = 300). Each entry i
    # contains a 100-D word vector of the word of index i in the reference word index (built during tokenization).
    # Note that Index 0 is a placeholder.

    embedding_dim = 300  # dimension of the word embeddings (word vectors)

    # I will use vocabulary_size to determine the size of the embedding matrix (number of rows)
    # +1 since index 0 of the embedding matrix is only a placeholder
    vocabulary_size = min(len(word_index) + 1, (max_words))

    # Initialize the embedding matrix
    embedding_matrix = np.zeros((vocabulary_size, embedding_dim))

    # Populate the embedding matrix with embedding vector from word2vec for each vocabulary in the word_index
    for word, i in word_index.items():
        if i >= max_words:  # only get at most 1000 word vectors
            continue
        try:
            embedding_vector = word_vectors[word]  # get the word embedding from word2vec
            embedding_matrix[i] = embedding_vector  # fill the ith row of the embedding matrix with the word vector
        except KeyError:  # word not found in word2vec will be zeros
            embedding_matrix[i] = np.zeros(embedding_dim)

    return X_train, X_val, y_train, y_val, embedding_matrix

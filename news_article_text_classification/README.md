

**News Headlines Multi-class Classification Project**



- In this project, I will process labelled news headlines, explore the text data, perform topic modelling, and then build predictive models to classify news headlines into different domains: Business, SciTech, Sports, World.



- In this data project, I performed the following:
  - Processed headline text data: tokenize, lemmatize, removed non-alphanumeric characters and stopwords, find bigrams and trigrams
  - Explored the headline text data.
  - Performed topic modelling with LDA
  - Developed a word embedding model and a t-SNE representation of the word embeddings
  - Performed modelling using textcat (CNN) in spaCY
  - Get the tf-idf representation of the headlines and performed dimension reduction.
  - Compared the performance of the following statistical learning methods:
    - SVD, Random Forest, Adaboost, KNN, Gaussian Naive Bayes
  - Optimized the models through hyperparameters tuning for SVD and Random Forest
  - Selected the "best" model based on highest f1-score (on test data)
  - Plotted the ROC of SVD and computed the confusion matrix.
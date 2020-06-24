# Binary and Multi-class Classification of Software Requirements with Word Embeddings



### Background

- This project is a reproduction of a data project/feasibility study that I did at Logapps, LLC.  
- The objective of my work at Logapps was to introduce statistical learning methods and deep learning with word embeddings to MARINE. a web-based application that assists requirement engineers to process and analysis software requirements.
- Currently, MARINE detects duplicated requirements (through measuring the syntactic similarity of pairs of requirements) and ambiguous requirements that do not conform to IEEE standards through keywords matching.
- Below are improvements to the new version of MARINE that I explored during my time at Logapps:

  - Compare requirements by computing their semantic similarity using word embeddings (a quantitative representation of documents that captures the semantic relationships between words and sentences).
  - Automating the classification of software requirements.  This classification tasks involves automatically categorize software requirements to the following classes:
    - 1) Non-functional (NFRs) and functional requirements (FRs).  This is a binary classification problem.
    - 2) Different types of NFRs: for example security, performance, and scalability.  This is a multi-class classification problem since the NFR types are  mutually exclusive.
- In short, FRs are requirements related to the features and use cases of a software product; while NFRs are related to how the software/system should achieve its objectives.
- By automating software requirements classification, requirement engineers can be spared from the tedious and exhausting task of manually labelling thousands of software requirements.  In addition, it will reduce the domain-knowledge needed from requirement engineers.




### Motivation of the project

- I wanted to answer the following questions from my data project at Logapps:

  - (Q1) Can pre-trained word embeddings improve the performance of traditional statistical learning approaches?

  - (Q2) Does CNN outperform SVC, Random Forest, and Adaboost models?  At what cost (training time)?

- To this end, I trained and compared the performance of the following classifiers:
  - "Traditional" statistical learning approaches such as SVC, Random Forest, and Gradient Boosted Trees with 1) tf-idf and 2) word embeddings representations of the requirements.
  - CNN with word embeddings.



### Datasets 

- At Logapps I had a labelled software requirement dataset from 3 different government agencies, with sample size of about 5000 samples.  However, since I no longer have access to these datasets, to reproduce my work at Logapps, I will have to use two smaller benchmark datasets instead.

  - The SecReq dataset that contains software requirements from three industries/domains: CPN, ePurse, GPS.  Each requirement is labelled security-related or non-security-related.

  - The NFR dataset that contains software requirements labelled functional or non-functional, as well as nine-different subtypes of NFRs.

    

### Workflow

- Clean, tokenize, lemmatize, and removed stop-words/non-alphanumeric symbols from the software requirements.
- Find bigrams and trigrams by training and applying Gensim phraser models to the software requirements.

- Use two different vector representations of the software requirements: tfidf and pre-trained word embeddings (on Google News 100 billion words corpora).
  
- Due to the small sample size of the benchmark datasets (and my dataset at Logapps), I want to know if I can apply transfer learning to compensate for this weakness.  In other words, can my model benefit from word embeddings that were trained on a much larger corpus?  To find out the benefits of using pre-trained word embeddings, I will train models using requirements that were represented by tf-idf weights, and requirements that were represented by pre-train word embeddings.
  
- Solve the following classification problems:
  - Binary classification (security related and non-security related) in the SecReq dataset.
  - Binary classification (functional vs non-functional) in the NFR dataset.
  - Multi-class classification in the NFR dataset.

- For each of these problems:

  - I train and optimize a SVC, Random Forest, and a Adaboost model with tf-idf and word embeddings to represent the software requirements.
  - I trained a CNN model with word embeddings.

- I  compare the performance of each of these models and answer the following questions:

  - (Q1) Can pre-trained word embeddings improve the performance of traditional statistical learning approaches?
  - (Q2) Does CNN outperform SVC, Random Forest, and Adaboost models?  At what cost (training time)?

  

  ## Results

- CNN with pre-trained word embeddings outperforms SVC, Random Forest and Adaboost classifiers in 2 out of the 3 classification tasks.
- For larger datasets, perhaps the performance difference would be wider.  One distinct advantage of CNN is that it automatically identify features that are informative in making predictions; thus, we don't have to learn the bigrams and trigrams engineer these features ourselves.
- All models require hyperparameters tuning, some more than others.
- SVC is a simple and the fastest model to train.  I would go with SVC in this case since its performance is almost as good as CNN and Adaboost.
- Pre-trained word embeddings compensate for the small amount of train data-- note that for the multiclass classification problem, I have less than 400 train observations to train my CNN! 
<br>




**Binary Classification: Model Comparison**



![binaryResultTable](https://github.com/hfung4/Data-Projects/blob/master/software_requirements_classification/outputs/final_model_comparison/binary_results_table.jpeg)
![binaryResultPlot](https://github.com/hfung4/Data-Projects/blob/master/software_requirements_classification/outputs/final_model_comparison/binary_classification_results_all.jpeg)







**Multiclass Classification: Model Comparison**


![multiclassResultTable](https://github.com/hfung4/Data-Projects/blob/master/software_requirements_classification/outputs/final_model_comparison/multiclass_results_table.jpeg)
![multiclassResultPlot](https://github.com/hfung4/Data-Projects/blob/master/software_requirements_classification/outputs/final_model_comparison/multiclass_classification_results_all.jpeg)


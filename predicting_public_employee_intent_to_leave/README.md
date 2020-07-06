# The intent to leave of public employees in the Australian Public Service

### Background

- I was a Research Data Analyst at Johns Hopkins University between September 2018-August 2020. There, I investigated the effects of management practices on employee attitudes (ex: job satisfaction, intrinsic motivation, and intent to leave). I built linear regression models to test four hypotheses using repeated cross-sectional data from six large public employee surveys across different years. 
- Using the public employee survey data, I also built predictive models to predict employees' intent to leave using their perception of the workplace environment and management practices. I will mainly focus on replicating this part of my work in this notebook.
- A measurement model that relates survey items to latent constructs (for management practices and employee attitudes) was specified based on organization behaviour theories, and information from reports/codebook from some (but not all) of the public employee surveys. 
- The measurement model was verified using confirmatory factor analysis (CFA) in STATA. Note that I will not replicate the CFA in this notebook; instead I will only use the results from CFA to develop my latent constructs from item scores.

<br>

### Objective of this notebook

- The objective of this notebook is to replicate some of my work as a Research Data Analyst at Johns Hopkins University. 
- In this notebook, I will use only one of the six public survey datasets-- the Australia Public Employee Survey (APS) to do the following:
  - First, I want to demonstrate that data on employee attitudes and management practices from public employee surveys is informative in predicting employees' intent to leave.
  - Second, I want to test the hypothesis that individuals reporting higher levels of intrinsic motivation see a differentially greater effect of supportive management practices on their intention to leave an agency. In other words, more intrinsically motivated individuals are more sensitive to management practice in assessing whether they wish to leave their positions than their less intrinsically motivated coworkers, all else equal. This suggests that unsupportive management practices may induce adverse selection out of an agency, with the more intrinsically motivated differentially likely to exit, and the less intrinsically motivated differentially likely to remain.

<br>



### Datasets 

- For this notebook, I will only use one of the six large public employee survey datasets: the Australian Public Employee Survey (APS) from 2017 to 2019.   Unfortunately, the data does not track individuals over-time, so I only have multiple cross-sectional data and thus cannot perform panel data analysis.
- In addition, I will only randomly sample 20000 from the APS dataset (2 million samples).  This is done to reduce the model training time (I do not have access to computational resources when I run this project from home).

<br>

### Workflow

- Import, process, clean, and merge datasets.

- Perform univariate and bivariate exploratory analysis.

- Compute correlation between variables (management practices and employee attitudes).

- Perform modelling (predict intent to leave with management practices and demographic variables):

  - Logistic Regression
  - Random Forest
  - XGBoost

- Tune hyperparameters for each model

- Assess each model with confusion matrix and AUC score.

- Perform statistical inference with regression models

  - Regress intent to leave with selected management practices and their interaction with intrinsic motivation.

    <br>

  ## Results

- Random Forest and XGBoost classifiers have the best performance.  Both models have higher recall score than precision scores compared to logistic regression. All models outperforms the baseline guess.

-  I might be interested in a model with higher recall scores since false-negatives is a concern. The cost of failing to identifying actual leavers or misclassifying a stayer as a leaver is high-- the human resource team will not be able to set the correct headcount/budget for recruitment at the start of year.

- For well-being, personal development, creativity, and resources, their effects on employees' intent to leave is "higher" (reduces intent to leave) for employees for higher scores in intrinsic motivation. In other words, many important supportive management practices matters more for employees with higher levels of intrinsic motivation.

- This suggests that unsupportive management practices may induce adverse selection out of an agency, with the more intrinsically motivated differentially likely to exit, and the less intrinsically motivated differentially likely to remain.

- The inverse is also true; these results suggest supportive management practices are differentially likely to retain more intrinsically motivated employees, as seen in their stated intent to leave the organization.

'''''''''''''''''
Helper functions
'''''''''''''''''
import pandas as pd
import numpy as np

''' This function computes the missing percentage of each row or column. '''


def missing_percentage(df, column):
    if (column):  # missing value in each column
        total = df.isnull().sum().sort_values(ascending=False)
        percent = round(df.isnull().sum().sort_values(ascending=False) / len(df) * 100, 2)
        return pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
    else:  # missing value in each row
        total = df.isnull().sum(axis=1).sort_values(ascending=False)
        percent = round(df.isnull().sum(axis=1).sort_values(ascending=False) / len(df.columns) * 100, 2)
        return pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])


'''This function aggregate the item scores associated with each feature(take their mean) 
   to get the score for the feature (ex: WPI_challenge) '''


def aggregate_col(df, feature, items):
    df[feature] = df[items].mean(axis=1, skipna=True)  # get item means and set it as the feature score
    return df


''' This function performs initial data processing'''


def process_data(year):
    '''Import a file that specifies latent constructs within the dataset and their associated measured variables
    This mapping is the ouptut of a measurement model was verified by a confirmatory factor analysis (CFA)
    performed in STATA. '''
    items = pd.read_excel("data/aust_aps_items.xlsx", encoding="latin-1", sheet_name=str(year))
    items.dropna(inplace=True)  # drop all rows with NA
    # Import the survey data
    file_name = "data/raw_data_" + str(year) + ".csv"
    raw = pd.read_csv(file_name, encoding="latin-1")
    # rename column names
    raw.rename(columns={'AS': 'org_size',
                        'q1': 'gender',
                        'q2@': 'age'}, inplace=True)

    '''I don't need ALL the items in the survey data, I will only keep the items that 
    relates to the latent constructs.'''
    keep = ["age", "gender", "org_size"] + list(items["Q_Num"])
    unique_keep = list(set(keep))
    unique_keep.sort()
    df = raw.loc[:, unique_keep]

    ''' Data Processing
    - Recode all items into numeric scores using pre-defined dictionaries in the helper file
    - Deal with items with reversed coding
    - Look at proportion of missing data for each item
    - Remove respondents with more than 20% missing response'''

    # Map levels to numeric values
    map_agree = {"Strongly disagree": 1, "Disagree": 2, "Neither agree nor disagree": 3, "Agree": 4,
                 "Strongly agree": 5}

    map_satisfy = {"Very dissatisfied": 1, "Dissatisfied": 2, "Neither satisfied or dissatisfied": 3, "Satisfied": 4,
                   "Very satisfied": 5}

    map_often = {"Never": 1, "Rarely": 2, "Sometimes": 3, "Often": 4, "Always": 5}

    map_often_rev = {"Never": 5, "Rarely": 4, "Sometimes": 3, "Often": 2, "Always": 1}

    map_somewhat = {"Not at all": 1, "Hardly at all": 2, "Somewhat": 3, "Quite a lot": 4, "To a very great extent": 5}

    map_leaving = {"I want to stay working for my agency for at least the next three years": 0,
                   "I want to stay working for my agency for the next one to two years": 0,
                   "I want to leave my agency within the next 12 months but feel it will be unlikely in the current environment": 1,
                   "I want to leave my agency within the next 12 months": 1,
                   "I want to leave my agency as soon as possible": 1}

    # Specify items that I need to recode
    if year == 2019:
        cols_to_move = ['age', 'gender', 'org_size', 'q38', 'q43a', 'q43b', 'q43c', 'q43d', 'q43f', 'q46']
        rc_agree = 10
        rc_satisfy = 'q38'
        rc_often_rev = 'q43a'
        rc_often = ["q43b", "q43c", "q43d", "q43f"]
        rc_leaving = "q46"
    elif year == 2018:
        cols_to_move = ['age', 'gender', 'org_size', 'q33', 'q38a', 'q38b', 'q38c', 'q38d', 'q38f', 'q41']
        rc_agree = 10
        rc_satisfy = 'q33'
        rc_often_rev = 'q38a'
        rc_often = ["q38b", "q38c", "q38d", "q38f"]
        rc_leaving = "q41"
    else:
        cols_to_move = ['age', 'gender', 'org_size', 'q41f', 'q41b', 'q41a', 'q41d', 'q36', 'q34h', 'q34e', 'q48']
        rc_agree = 11
        rc_satisfy = 'q36'
        rc_often_rev = 'q41a'
        rc_often = ["q41b", "q41d", "q41f"]
        rc_leaving = "q48"
        rc_somewhat = ["q34h", "q34e"]

        # Reorder columns
    new_cols = [col for col in list(df.columns) if col not in cols_to_move]
    new_cols = cols_to_move + new_cols
    df = df[new_cols]

    # recode all columns with "Strongly disagree"...."Strongly agree" to numerical scores
    df.iloc[:, rc_agree:] = df.iloc[:, rc_agree:].replace(map_agree)
    # recode satisfy
    df[rc_satisfy] = df[rc_satisfy].replace(map_satisfy)
    # recode often
    df[rc_often_rev] = df[rc_often_rev].replace(map_often_rev)
    df.loc[:, rc_often] = df.loc[:, rc_often].replace(map_often)
    # recode leaving
    df[rc_leaving] = df[rc_leaving].replace(map_leaving)

    if year == 2017:
        # recode somewhat
        df.loc[:, rc_somewhat] = df.loc[:, rc_somewhat].replace(map_somewhat)

    # replace blank cells with NaN
    df = df.replace(r'^\s*$', np.nan, regex=True)

    # missing value count and percentage of each column
    print("")
    print("********************")
    print("The missing value count and percentage of each item:")
    print(missing_percentage(df, True).sort_values(by="Percent", ascending=False)[:10])

    # missing value count and percentage of each column
    row_missing_count = missing_percentage(df, False)
    # Only keep respondents with missing values less than 20%
    keep_row = row_missing_count[row_missing_count["Percent"] < 20]

    # percentage of respondents retained
    print("")
    print("********************")
    print("I kept {} % of respondent with missing value less than 20%".format(
        int(len(keep_row) / len(row_missing_count) * 100)))

    df = df.loc[keep_row.index, :]
    df = df.sort_index(ascending=True)

    # one-hot encode age and org_size
    df = pd.get_dummies(df, columns=["age", "org_size", "gender"],
                        drop_first=True)  # drop the first level out of k level

    # print df shape
    print("")
    print("********************")
    print("The shape of the Dataframe for all selected items is:{}".format(df.shape))

    '''Aggregating items scores to compute the construct scores
    - Use item dataframe to build mapping tuples
    - For simplicity, I will take the mean of items scores according to the tuples 
      to compute the score for each construct.
    - In my project, I computed the scores for the latent construct using the measurement 
      model and the factor loading estimated from CFA. '''

    df_items = items[["Q_Num", "Factor"]]  # get a DataFrame with only Q_Num and Factor
    features = list(df_items.Factor.unique())  # get a list of features

    agg_map = []
    for i in range(len(features)):
        agg_map.append((features[i], [q for q in df_items[df_items.Factor == features[i]]["Q_Num"]]))

    for i in agg_map:
        aggregate_col(df, i[0], i[1])

    df.drop(list(items["Q_Num"]), axis=1, inplace=True)

    '''After computing the construct scores for each respondent by taking the mean of his/her associated items scores 
    (excluding NA), some constructs will still contain NA scores because: 
        1) the construct comprise of only 1 item and some respondents have missing values for that item, 
        2) all associated items of the construct for a respondent are NA
    That said, all missing values are 1 % or lower.  Thus, I will remove respondent with NA score '''
    print("")
    print("********************")
    print(missing_percentage(df, True).sort_values(by="Percent", ascending=False).head(10))

    before = df.shape
    df.dropna(inplace=True)
    after = df.shape
    print("")
    print("********************")
    print("I lose {} % of data after the removal of NA respondents".format(abs((after[0] - before[0]) / before[0])))

    # create a year column
    df["year"] = year

    df = df.sort_index(axis=1)  # sort column by column names

    return df


'''This function that takes 1) df, 2) column, and return the count of each level of that factor '''


def percent_value_counts(df, feature):
    count = df.loc[:, feature].value_counts(dropna=False)  # count is a Series
    percent = round(df.loc[:, feature].value_counts(dropna=False, normalize=True) * 100, 2)
    # Put the series count and percent in an output DataFrame
    return pd.concat([count, percent], axis=1, keys=["count", "percent"])


'''This function creates correlation matrix and outputs variables with correlation that is higher than 0.5'''


def correlation_analysis(df, file_name):
    # Generate a "mask" for the upper triangle
    mask = np.zeros_like(df.corr(), dtype=np.bool)
    corr = df.corr(method='spearman')  # correlation matrix

    # Look at highly correlated features pairs
    highly_corr = corr.abs()[corr > 0.5]
    unstacked = highly_corr.unstack().sort_values(ascending=False).drop_duplicates()
    unstacked.dropna(inplace=True)  # Drop all NA
    unstacked = unstacked[unstacked != 1]  # remove all diagonal elements in the cor matrix with corr = 1

    unstacked = unstacked.reset_index()
    unstacked.columns = ["Var1", "Var2", "Corr"]

    top_corr_features = unstacked.sort_values(by="Corr", ascending=False)
    # Output to csv
    top_corr_features.to_csv(file_name, index=False)


'''This function generates interaction terms by performing multiplication of two columns in a DataFrame'''


def gen_interaction(df, x, y):  # x is a list of feature names, y is a single feature name
    out = df.copy()
    for feature in x:
        values = out[feature] * out[y]
        out[feature + "_" + y] = values
    return out

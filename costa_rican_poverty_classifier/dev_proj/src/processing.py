"""data"""
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np
from itertools import repeat
from collections import Counter

"""stats"""
import scipy.stats as stats

"""visualization"""
import matplotlib.pyplot as plt
import seaborn as sns

"""type checking"""
from typing import Union
from typing import List, Dict, Tuple

num_type = Union[int, float, complex]


def one_hot_encoding(df: pd.DataFrame, vars: List[str]) -> pd.DataFrame:
    """
    one_hot_encoding:
    Given an input dataframe and a categorical variable,
    one-hot encode the variable, drop the original variable,
    and merge the one-hot encoded columns to the
    input dataframe.

    Args:
        df (pd.DataFrame): input dataframe
        vars (List[str]): a list of names of the categorical variable
    Returns:
        data (pd.DataFrame): output dataframe
    """

    # Make a copy of the input dataframe
    data = df.copy()

    for var in vars:
        # Get the one-hot encoded dataframe
        df_ohe = pd.get_dummies(data[var], prefix=var, drop_first=False)

        # Convert all columns in df_ohe to small caps, and replace
        # all whitespace to "_", and remove all non-alphanumeric characters
        # except for "_"
        df_ohe.columns = (
            df_ohe.columns.str.replace(" ", "_", regex=True)
            .str.replace("[^a-zA-Z0-9_]", "", regex=True)
            .str.lower()
        )

        # Drop the original variable in the input dataframe
        data.drop(var, axis="columns", inplace=True)

        # Join the one-hot encoded dataframe to the input datarame
        data = data.join(df_ohe)
        # df.columns = df.columns.str.replace(" ", "")

    return data


def get_num_cat_vars(df: pd.DataFrame) -> Tuple[List, List]:
    """
    get_num_cat_vars:
    Given an input dataframe and a categorical variable,
    one-hot encode the variable, drop the original variable,
    and merge the one-hot encoded columns to the
    input dataframe.

    Args:
        df (pd.DataFrame): input dataframe
    Returns:
        cat_vars(List): a list of categorical variable names
        num_vars(List): a list of numeric variable names
    """

    # Make a copy of the input dataframe
    data = df.copy()

    # Get categorical variables in the dataframe
    cat_vars = [var for var in data.columns if data[var].dtype == "O"]

    # Get numeric variables in the dataframe (even those that are integers but
    # are actually ordinal)
    num_vars = data.select_dtypes(include=np.number).columns.values.tolist()

    return cat_vars, num_vars


def int_to_ordinal_type(df: pd.DataFrame, ordinal_vars: List[str]) -> pd.DataFrame:
    """
    int_to_ordinal_type:
    Given an input dataframe and a list of ordinal variables
    that are currently of the integer type, convert the integer
    column to a ordered categorical column.

    Args:
        df (pd.DataFrame): input dataframe
        ordinal_vars(List[str]): a list of ordinal variables that are currently of integer type
    Returns:
        data(pd.DataFrame): output dataframe
    """

    data = df.copy()

    for var in ordinal_vars:
        # Create the ordered categorical type
        categorical_type = pd.CategoricalDtype(
            categories=sorted(df[var].unique()), ordered=True
        )
        data[var] = data[var].astype(categorical_type)

    return data


def label_encoding(data: pd.DataFrame, nominal: List) -> Union[pd.DataFrame, Dict]:
    """_summary_

    Args:
        data (pd.DataFrame): input dataframe
        nominal (List): a list of nominal variables I want to label-encode

    Returns:
        df (pd.DataFrame): output DataFrame
        mapping_dict: mapping dictionary from integer encoding to the original string encoding
    """

    # make a copy of the input dataframe
    df = data.copy()

    # Convert input variables to the category dtype
    df[nominal] = df[nominal].astype("category")

    # For each column, recode level using their cat.codes
    # Create a dictionary that maps cat.codes (integer encoding) to the original string encoding

    mapping_dict = dict()  # init mapping_dict

    for var in nominal:
        # create mapping dictionary
        mapping_dict[var] = dict(zip(df[var].cat.codes, df[var]))
        # Remove mapping of np.nan to -1 from the mapping_dict (if it exist in mapping_dict)
        mapping_dict[var].pop(-1, None)

        # Recode levels
        df[var] = df[var].cat.codes
        # Convert to -1 back to NaN (NOTE: cat.code of np.NaN is -1)
        # So that null values are preserved after the label encoding
        df[var] = df[var].replace({-1: np.nan})

    return df, mapping_dict


def fct_lump(
    df: pd.DataFrame, var: str, n_retain: int, rare_label: str = "Other"
) -> pd.DataFrame:
    """
    fct_lump:
    Given an input dataframe and a column, compute the top n levels
    with the most observations (most common levels) to retain. n is
    an input to the function that is specified by the user.
    Relabel the levels of the column-- retain the top n levels,
    and lump the rest of the labels (recode them) to "Other" (or any other
    "rare_label" that is specified by the user).

    Args:
        df(pd.DataFrame): input dataframe
        var(str): column name
        n_retain(int): number of most common levels to retain
        rare_label(str): label for the combined rare levels
    Returns:
        data(pd.DataFrame): output dataframe
    """
    # make a copy of the input dataframe
    data = df.copy()

    # compute the top n levels in a column to retain
    top_n = data[var].value_counts().index[:n_retain]

    # recode column-- retain the top n levels, and recode the rest of the levels to "Other"
    data[var] = data[var].where(data[var].isin(top_n), rare_label)

    return data


def extent_missingness(df: pd.DataFrame, vars=None):
    """
    extent_missingness:
    Given an input dataframe, compute the proportion of missing values or all
    variables in the dataframe (if no vars is given), or the porportion
    of missing values of a set of variables in the dataframe (given in the list vars).

    Args:
        df(pd.DataFrame): input dataframe
        vars(List[str]): a list of variables I want to find missingness for
    Returns:
        (pd.DataFrame): output dataframe of proportion of missing values of variables
    """

    # make a copy of the input dataframe
    data = df.copy()

    if vars is not None:
        # Missingness of a user-specified set of variables
        return data.loc[:, vars].isna().mean().sort_values(ascending=False)
    else:
        # Missingness of all variables in the input dataframe
        return data.isna().mean().sort_values(ascending=False)


def remove_outliers_iqr(
    df: pd.DataFrame,
    vars: List[str],
    lwr: Dict[str, num_type] = None,
    upr: Dict[str, num_type] = None,
    plotting: bool = False,
    figsize: Tuple[int, int] = (10, 5),
    prt_bounds: bool = False,
) -> pd.DataFrame:
    """remove_outliers_iqr:

    NOTE: only used for continuous variables!
    Given an input dataframe and a list of continuous variables,
    remove outliers that are outside of the interquantile range.
    Optionally, for each variable, generate a plot of the distribution
    before-and-after outlier removal for the variable.

    Args:
        df (pd.DataFrame): input dataframe
        vars (List[str]): a list of continuous columns
        lwr (Dict[str, num_type], optional): user defined lower bound of values to keep. Defaults to None.
        upr (Dict[str, num_type], optional):  user defined upper bound of values to keep. Defaults to None.
        plotting (bool, optional): option flag for plotting distribution of variables. Defaults to False.
        figsize (Tuple[int, int], optional): figure size. Defaults to (10, 5).
        prt_bounds (bool, optional): print out upr and lwr bounds of included values. Defaults to False.

    Returns:
        pd.DataFrame: output dataframe
    """
    # make a copy of the input dataframe
    data = df.copy()

    # Initialize dictionary with None values
    if lwr is None:
        lwr = dict(zip(vars, repeat(None)))

    if upr is None:
        upr = dict(zip(vars, repeat(None)))

    # init a list of numeric columns
    l_numeric_cols = []

    for var in vars:

        # Check to see if the column is numeric
        if not is_numeric_dtype(data[var]):
            print(
                f"Skipped: {var} is not numeric, so we cannot remove outliers based on iqr criterion."
            )
            continue

        # append var to l_numeric_cols if iteration is not skipped
        l_numeric_cols.append(var)

        # The 25th and 75th percentile (1st and 3rd quartile)
        q1 = data[var].describe()["25%"]
        q3 = data[var].describe()["75%"]

        # IQR
        iqr = q3 - q1

        # Upper and lower bound of values to keep
        if lwr[var] is None:
            lower_bound = q1 - 3 * iqr
        else:
            # use user-specified lower bound
            lower_bound = lwr[var]

        if upr[var] is None:
            upper_bound = q3 + 3 * iqr
        else:
            # use user-specified lower bound
            upper_bound = upr[var]

        # Remove outliers (only keep observations within IQR, or within user-defined bounds)
        if prt_bounds:
            print(f"{var}: keep values between {lower_bound} and {upper_bound}")
        df_out = data.loc[(data[var] < upper_bound) & (data[var] > lower_bound), :]

    # Plot distribution of variable before and after you remove the outliers
    if plotting:

        # If we are only processing one variable
        if len(vars) == 1:
            v = vars[0]  # get the single variable

            # Plot distribution of var before outliers removal
            fig, axes = plt.subplots(1, 2, figsize=figsize)
            axes[0].hist(data[v], bins=30, color="k", alpha=0.5)
            axes[0].set_title(f"Distribution of {v} before outliers removal")

            # Distribution of var after outliers removal
            axes[1].hist(df_out[v], bins=30, color="blue", alpha=0.5)
            axes[1].set_title(f"Distribution of {v} after outliers removal")

            # adjust whitespace between subplots
            plt.subplots_adjust(wspace=0.5, hspace=0.5)

        else:
            # There are 2 or more variables that I processed and removed outliers
            fig, axes = plt.subplots(len(l_numeric_cols), 2, figsize=figsize)

            for i, v in enumerate(l_numeric_cols):
                # Distribution of var before outliers removal
                axes[i, 0].hist(data[v], bins=30, color="k", alpha=0.5)
                axes[i, 0].set_title(f"Distribution of {v} before outliers removal")

                # Distribution of var after outliers removal
                axes[i, 1].hist(df_out[v], bins=30, color="blue", alpha=0.5)
                axes[i, 1].set_title(f"Distribution of {v} after outliers removal")

            # adjust whitespace between subplots
            plt.subplots_adjust(wspace=0.5, hspace=0.5)

    return df_out


def remove_collinear_features(
    df: pd.DataFrame,
    DV: str,
    threshold: num_type,
    drop_collinear: bool = True,
    print_collinear: bool = False,
    custom_drop: List[str] = [],
) -> pd.DataFrame:
    """remove_collinear_features:

    There are a number of methods for removing collinear features, such as using the
    Variance Inflation Factor. Here, We will use a simpler metric, and remove features
    that have a correlation coefficient above a certain threshold with each other.

    This function removes the collinear continuous features based on a threshold we select for the
    correlation coefficients by removing one of the two features that are compared. It also prints
    the correlations that it removes so we can see the effect of adjusting the threshold.
    We will use a threshold of 0.6 which removes one of a pair of features if the correlation
    coefficient between the features exceeds this value.

    Args:
        df (pd.DataFrame): input dataframe
        DV (str): dependent variable
        threshold (num_type):  threshold of correlation above which we will drop one of the variable
        drop_collinear (bool, optional):drop one of the collinear variables if True, otherwise return the original df
        print_collinear (bool): print collinear pairs. Defaults to True.
        print_collinear (bool, optional): print collinear pairs. Defaults to False.
        custom_drop (List[str], optional): custom list of variables to drop from the dataframe in addition to the collinear ones. Defaults to [].

    Returns:
        df_out (pd.DataFrame): output dataframe
        df_collinear_pairs (pd.DataFrame): a dataframe of collinear pairs and their correlation
    """
    # make a copy of the input dataframe
    data = df.copy()

    # save the dependent variable
    y = data[DV]
    # handle features only
    df_out = data.drop(columns=[DV])

    # Calculate the correlation matrix
    corr_matrix = df_out.corr()
    iters = range(len(corr_matrix.columns) - 1)
    # Init a list of columns to be dropped
    drop_cols = []
    # Init a list of tuples that contains 1) collinear col_1,
    # 2) collinear col_2, and 3) correlation between them
    collinear_pairs = []

    # Iterate through the correlation matrix and compare correlations
    # If I have k features, corr_matrix has shape (kxk)
    for i in iters:  # iterate from 0 to k-1
        for j in range(i):  # iterate from 0 to k-1
            item = corr_matrix.iloc[j : (j + 1), (i + 1) : (i + 2)]
            col = item.columns
            row = item.index
            val = abs(item.values)

            # If correlation exceeds the threshold
            if val >= threshold:

                # Print the correlated features and the correlation value
                if print_collinear:
                    print(col.values[0], "|", row.values[0], "|", round(val[0][0], 2))

                # Add the tuple of collinear pairs and their correlation to a list
                collinear_pairs.append(
                    (col.values[0], row.values[0], round(val[0][0], 2))
                )
                # Add one of the variable to the "drop_cols" list
                drop_cols.append(col.values[0])

    # Drop one of each pair of correlated columns
    drops = set(drop_cols)
    if drop_collinear:
        df_out = df_out.drop(columns=drops)

    # Drop additional columns that are specified by the using
    if custom_drop != []:
        df_out = df_out.drop(columns=custom_drop)

    # Add the score back in to the data
    df_out[DV] = y

    # Convert collinear_pairs to a dataframe
    df_collinear_pairs = pd.DataFrame(
        collinear_pairs, columns=["var_1", "var_2", "correlation"]
    )

    # Drop duplicated rows in terms of var_1 and var_2 (order does not matter)
    # False if row is a duplicated that needs to be removed
    mask = ~pd.DataFrame(
        np.sort(df_collinear_pairs[["var_1", "var_2"]], axis=1)
    ).duplicated()
    df_collinear_pairs = df_collinear_pairs[mask]

    return df_out, df_collinear_pairs


def cramers_v(
    df: pd.DataFrame, var1: str, var2: str, bias_correction: bool = True
) -> float:
    """Compute the Cramer's V correlation metric (with or without bias correction)

    Args:
        df (pd.DataFrame): input dataframe
        var1 (str): categorical variable 1
        var2 (str): categorical variable 2
        bias_correction (bool, optional): bias correction flag. Defaults to True.

    Returns:
        float: Cramer's V correlation metric
    """
    df = df.copy()

    # crosstab of the two variables
    crosstab = np.array(pd.crosstab(df[var1], df[var2], rownames=None, colnames=None))

    # chi2 (chi-sq statistics of the two variables)
    chi2, p, dof, ex = stats.chi2_contingency(crosstab)

    # Total number of observations
    n = np.sum(crosstab)

    # Take the min(# of rows -1, # of cols -1)
    nrow = crosstab.shape[0]
    ncol = crosstab.shape[1]

    mini = min(nrow - 1, ncol - 1)

    # Let phi be chi-sq test statistics/N
    phi = chi2 / n

    # Compute Cramer's V
    V = np.sqrt(phi / mini)

    if bias_correction:
        # Adjust phi
        phi_adj = max(0, (phi - ((ncol - 1) * (nrow - 1) / (n - 1))))

        # ncol adjusted
        ncol_adj = ncol - ((ncol - 1) ** 2 / (n - 1))
        # nrow adjusted
        nrow_adj = nrow - ((nrow - 1) ** 2 / (n - 1))

        # mini adjusted
        mini_adj = min(nrow_adj - 1, ncol_adj - 1)

        # Cramer's V with bias correction
        V_adj = np.sqrt(phi_adj / mini_adj)

        return V_adj
    else:
        return V


def same_dtype_corr_matrix(df: pd.DataFrame, dtype: str, method: str):
    """
    Given a data subset (MUST be ALL categorical variables, or ALL continuous variables),
    compute the appropiate correlation measure (Pearson or Spearman for continuous pairs,
    and Cramer V's with bias correction for categorical pairs) for each pair of variables.
    Output the correlation matrix as a dataframe

    Args:
        df (pd.DataFrame): input data subset (must by all categorical or all continuous variables)
        dtype (str): data type ("categorical" or "continuous")
        method (str): correlation metric ("cramers_v", "spearman", or "pearson")

    Returns:
        df_res (pd.DataFrame): correlation matrix
    """

    # Input checks
    # I want to ensure the methods are appropiate for the data type of the input dataframe
    if dtype == "categorical" and method != "cramers_v":
        raise ValueError(
            "Your variables are categorical, the correlation method should be cramers_v"
        )

    if dtype == "categorical" and method != "cramers_v":
        raise ValueError(
            "Your variables are continuous, the correlation method should be pearson or spearman"
        )

    # For categorical variables
    if method == "cramers_v":
        # Init a list called rows
        rows = []

        for var1 in df:
            # Init a list called col
            col = []

            for var2 in df:
                # Get Cramer's V of var1 and var2
                V_value = round(cramers_v(df=df, var1=var1, var2=var2), 2)

                # Append V_value on the col list (var1 fixed, var2 varying)
                col.append(V_value)
            # Append col (a list of Cramer's V for var1 column) to rows. So rows is a list of list
            rows.append(col)

        # convert list of list to ndarray
        res = np.array(rows)

        # Convert np.array to dataframe
        df_res = pd.DataFrame(res, columns=df.columns, index=df.columns)

    else:
        # Continuous variables
        df_res = df.corr(method=method)

    return df_res


def corr_heatmap(df_corr: pd.DataFrame, method: str, size: int = 10):
    """
    Given any correlation matrix, I take the lower triangle (exclude the diagonal)
    and then plot a heatmap

    Args:
        df_corr (pd.DataFrame): correlation matrix
        method (str): correlation metric (cramers_v, spearman, pearson), determines the min/max of the heatmap
        size (int, optional): width and height of plot. Defaults to 10.
    """

    # Different correlation metrics have different range
    # cramers_v is [0,1], and spearman or pearson is [-1,1]
    if method == "cramers_v":
        vmin = 0
    else:
        vmin = -1

    # Select the upper triangle of the correlation matrix
    lower = df_corr.where(
        np.tril(np.ones(df_corr.shape), k=-1).astype(bool)
    )  # k=-1 if you want to exclude diagonal

    # Create heatmap with figsize = sizeXsize
    fig, ax = plt.subplots(figsize=(size, size))
    sns.heatmap(
        lower, ax=ax, vmin=vmin, vmax=1, annot=True, square=True
    )  # figsize must be X,X
    plt.show()


def cont_cat_corr(
    df: pd.DataFrame, cont_vars: List[str], with_p_value: bool = False
) -> pd.DataFrame:
    """_summary_

    Args:
        df (pd.DataFrame): data subset (contains one-hot encoded categorical variables and continuous variables)
        cont_vars (List[str]): list of continuous variable names
        with_p_value (bool, optional): if set to True, display the p-values of each correlation metric. Defaults to False.

    Returns:
        pd.DataFrame: correlation matrix (contains continuous variable for each column and their correlation with all other variables in each row)
    """
    # Set color map scheme
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    # Init a list called rows
    rows = []

    # Get a counter dictionary of continuous variables
    freq = Counter(cont_vars)

    for var1 in df:

        # Init a list called col
        col = []

        for var2 in df:

            # Check to see if one of the variable is binary and the other is continuous
            is_binary_cont_pair = (freq[var1] == 0 and freq[var2] != 0) or (
                freq[var2] == 0 and freq[var1] != 0
            )
            # Check to see if both variables are continuous
            is_cont_cont_pair = freq[var1] != 0 and freq[var2] != 0

            # Check to see if var1 == var2 (if yes, then if I concat the two dataframes df[var1] and df[var2]
            # and then slicing the concat dataframe, I will have issues.
            # Let's say, var1=var2="Fare", and if I concat the dataframe
            # and then slice the concat dataframe df_combined["Fare"]. I will get back two columns of "Fare".
            paired_with_self = var1 == var2

            # Get combined dataframe (so that I can drop NA)
            # Note that stats.pointbiserialr and stats.spearmanr
            # cannot handle missing values and X and Y must have the same lengh
            df_combined = pd.concat([df[var1], df[var2]], axis="columns")

            # Drop NA
            df_combined = df_combined.dropna()

            if is_binary_cont_pair:
                # Get Biserial correlation of var1 and var2
                raw_results = stats.pointbiserialr(df_combined[var1], df_combined[var2])
            elif is_cont_cont_pair:
                # Check if both variables are continuous, if yes, then use Spearman correlation
                if paired_with_self:
                    raw_results = [1, 0]  # correlation is 1 with p-value = 0
                else:
                    raw_results = stats.spearmanr(df_combined[var1], df_combined[var2])
            else:
                # Otherwise, both variables are categorical
                # set biserial correlation of var1 and var2 to -999
                # (which we will remove later on from the matrix)
                raw_results = [-999, -999]

            # Results with p-value or without p-value
            if with_p_value:
                # Contains both correlation and p-value (used for displaying in a table)
                corr = f"{round(raw_results[0],2)}, p-value: {round(raw_results[1],3)}"
            else:
                corr = round(raw_results[0], 2)

            # Append V_value on the col list (var1 fixed, var2 varying)
            col.append(corr)

        # Append col (a list of Cramer's V for var1 column) to rows. So rows is a list of list
        rows.append(col)

    # convert list of list to ndarray
    res = np.array(rows)

    # Convert np.array to dataframe
    df_res = pd.DataFrame(res, columns=df.columns, index=df.columns)

    # Get only columns with NO -999
    if with_p_value:
        to_drop = [
            col
            for col in df_res.columns
            if Counter(df_res[col])["-999, p-value: -999"] != 0
        ]
        df_res = df_res.drop(to_drop, axis="columns")
    else:
        to_drop = [col for col in df_res.columns if Counter(df_res[col])[-999] != 0]
        df_res = df_res.drop(to_drop, axis="columns")

        with pd.option_context("display.precision", 2):
            df_res = (
                df_res.style.background_gradient(cmap=cmap, vmin=-1, vmax=1)
                .set_properties(**{"font-size": "20px"})
                .format(precision=2)
            )

    return df_res

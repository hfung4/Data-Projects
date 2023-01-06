# We will test the functions in the processing/preprocessing module.

import math

from cr_analysis.processing.preprocessing import data_preprocessing


def test_data_preprocessing(get_raw_data):

    preprocessed = data_preprocessing(get_raw_data)

    # Data type changed from obj to numeric
    assert preprocessed["dependency"].dtype == "float64"
    assert preprocessed["edjefa"].dtype == "int64"
    assert preprocessed["edjefe"].dtype == "int64"

    # Expected missing values after handling certain cases of missingness in v18q1, v2a1
    assert preprocessed["v18q1"].isnull().sum() == 0

    expected_prop_v2a1_missing = 0.1
    assert math.isclose(
        preprocessed.v2a1_missing.value_counts(normalize=True).loc[True],
        expected_prop_v2a1_missing,
        abs_tol=0.01,
    )

    # expected shape of the preprocessed dataframe
    assert preprocessed.shape[0] == 10307
    assert preprocessed.shape[1] == 222

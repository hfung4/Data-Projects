"""
pipeline.py

- We need to impute missing values for 6 features with a new level called "missing".
- Lump the rare levels of the following categorical variables to "Other":
    - state
    - city
    - race
    - gender
    - industry
- Map string encoding to integer encoding for the following ordinal variables:
    - overall_experience
    - in_field_experience
    - age_category
- One hot encode nominal features
"""


from feature_engine.encoding import OneHotEncoder, RareLabelEncoder
from feature_engine.imputation import CategoricalImputer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline

from survey_analysis.config.core import config
from survey_analysis.processing import features as pp

salary_pipeline = Pipeline(
    [
        # === Imputation ===
        # Imputing missing values in categorical variables (with a new "missing" level)
        # CategoricalImputer from feature_engine
        (
            "missing_imputation",
            CategoricalImputer(
                imputation_method="missing",
                variables=config.model_config.CATEGORICAL_VARS_WITH_NA_MISSING,
            ),
        ),
        # === Recoding categorical variables ===
        (
            "rare_label_encoder_10",
            RareLabelEncoder(
                tol=0.01,
                max_n_categories=10,
                n_categories=1,
                replace_with="Other",
                variables=config.model_config.CAT_VARS_10_MOST_FREQ,
            ),
        ),
        (
            "rare_label_encoder_2",
            RareLabelEncoder(
                tol=0.01,
                max_n_categories=2,
                n_categories=1,
                replace_with="Other",
                variables=config.model_config.CAT_VARS_2_MOST_FREQ,
            ),
        ),
        (
            "rare_label_encoder_4",
            RareLabelEncoder(
                tol=0.01,
                max_n_categories=4,
                n_categories=1,
                replace_with="Other",
                variables=config.model_config.CAT_VARS_4_MOST_FREQ,
            ),
        ),
        # === Recoding categorical variables with ordered level ===
        # Recode categorical variables with ordered level:
        # map from string encoding to numeric encoding
        # Use custom class from 'preprocessing.py' Mappers
        (
            "mapper_exp",
            pp.Mapper(
                variables=config.model_config.EXPERIENCE_VARS,
                mappings=config.model_config.DICT_EXPERIENCE_ORDERED_LEVELS,
            ),
        ),
        (
            "mapper_age",
            pp.Mapper(
                variables=config.model_config.AGE_VARS,
                mappings=config.model_config.DICT_AGE_ORDERED_LEVELS,
            ),
        ),
        # === One-hot enccode nominal variables ===
        (
            "one_hot_encoder",
            OneHotEncoder(
                drop_last=True,  # avoid dummy variable trap
                variables=config.model_config.NOMINAL_VARIABLES,
            ),
        ),
        # Gradient Boosted tree
        (
            "gradient_boosting",
            GradientBoostingRegressor(
                n_estimators=config.model_config.n_estimators,
                subsample=config.model_config.subsample,
                learning_rate=config.model_config.learning_rate,
                max_depth=config.model_config.max_depth,
                max_features=config.model_config.max_features,
                random_state=config.model_config.RANDOM_STATE,
            ),
        ),
    ]
)

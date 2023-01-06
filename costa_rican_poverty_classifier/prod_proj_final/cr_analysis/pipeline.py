from feature_engine.imputation import MeanMedianImputer
from feature_engine.selection import DropConstantFeatures
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as imb_pipeline
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import MinMaxScaler

from cr_analysis.config.core import config
from cr_analysis.processing import features as pp

# Feature selection model
sel_clf = ExtraTreesClassifier(
    n_estimators=config.model_config.FEATURE_SEL_MODEL_N_ESTIMATORS,
    random_state=config.model_config.RANDOM_STATE,
)

# Create pipeline, setting some parameters based on Random Search results
data_pipeline = imb_pipeline(
    [
        # === Imputation === #
        (
            "missing_imputation",
            MeanMedianImputer(imputation_method=config.model_config.IMPUTATION_METHOD),
        ),
        # === drop qusai-constant variables === #
        # drop variables with a level that appears in 0.8 of observations
        ("drop_nzv", DropConstantFeatures(tol=config.model_config.DROP_NZV_TOL)),
        # === oversampling === #
        # upsample the minority classes to have 0.25 of
        # the majority class, so 500 for class 1-3
        (
            "oversampling",
            SMOTE(
                # sampling_strategy=config.model_config.OVERSAMPLING_STRATEGY,
                random_state=config.model_config.RANDOM_STATE,
            ),
        ),
        # === undersampling ==== #
        # undersample the majority class to have 2x of minority class, so 1000 for class 4
        # (
        #    "undersampling",
        #    RandomUnderSampler(
        #        sampling_strategy=config.model_config.UNDERSAMPLING_STRATEGY,
        #        random_state=config.model_config.RANDOM_STATE,
        #    ),
        # ),
        # === normalization === #
        ("scaler", MinMaxScaler()),
        # === feature selection using logreg === #
        ("fs", SelectFromModel(estimator=sel_clf)),
        # === model === #
        (
            "clf",
            RandomForestClassifier(
                n_estimators=config.model_config.CLF__N_ESTIMATORS,
                max_depth=config.model_config.CLF__MAX_DEPTH,
                min_samples_leaf=config.model_config.CLF__MIN_SAMPLES_LEAF,
                min_samples_split=config.model_config.CLF__MIN_SAMPLES_SPLIT,
                random_state=config.model_config.RANDOM_STATE,
            ),
        ),
    ]
)


# Create data_pipeline_debug by inserting the debug step
# after every step in data_pipeline

data_pipeline_debug = imb_pipeline(
    [
        # === Imputation === #
        (
            "missing_imputation",
            MeanMedianImputer(imputation_method=config.model_config.IMPUTATION_METHOD),
        ),
        # Debug missing_imputation
        (
            "debug_missing_imputation",
            pp.Debug(
                step_name="missing_imputation",
            ),
        ),
        # === drop qusai-constant variables === #
        # drop variables with a level that appears in 0.8 of observations
        ("drop_nzv", DropConstantFeatures(tol=config.model_config.DROP_NZV_TOL)),
        # Debug drop_nzv
        (
            "debug_drop_nzv",
            pp.Debug(
                step_name="drop_nzv",
            ),
        ),
        # === oversampling === #
        # upsample the minority classes to have 0.25
        # of the majority class, so 500 for class 1-3
        (
            "oversampling",
            SMOTE(
                #    sampling_strategy=config.model_config.OVERSAMPLING_STRATEGY,
                random_state=config.model_config.RANDOM_STATE,
            ),
        ),
        # Debug oversampling
        (
            "debug_oversampling",
            pp.Debug(
                step_name="oversampling",
            ),
        ),
        # save column names 1
        (
            "save_col_names_1",
            pp.save_col_names(),
        ),
        # === undersampling ==== #
        # undersample the majority class to have 2x of minority class, so 1000 for class 4
        # (
        #    "undersampling",
        #    RandomUnderSampler(
        #        sampling_strategy=config.model_config.UNDERSAMPLING_STRATEGY,
        #        random_state=config.model_config.RANDOM_STATE,
        #    ),
        # ),
        # Debug undersampling
        # (
        #    "debug_undersampling",
        #    pp.Debug(
        #        step_name="undersampling",
        #    ),
        # ),
        # === normalization === #
        ("scaler", MinMaxScaler()),
        # Debug normalization
        (
            "debug_normalization",
            pp.Debug(
                step_name="normalization",
            ),
        ),
        # === feature selection using model === #
        ("fs", SelectFromModel(estimator=sel_clf)),
        # === model === #
        (
            "clf",
            RandomForestClassifier(
                n_estimators=config.model_config.CLF__N_ESTIMATORS,
                max_depth=config.model_config.CLF__MAX_DEPTH,
                min_samples_leaf=config.model_config.CLF__MIN_SAMPLES_LEAF,
                min_samples_split=config.model_config.CLF__MIN_SAMPLES_SPLIT,
                random_state=config.model_config.RANDOM_STATE,
            ),
        ),
    ]
)

"""
pipeline.py

Data processing steps:
- size: remove BNR and bedroom text, convert to float, and then remove outliers
- area_type: retain the top 2 levels and combine the rest to a level called "Other"
- availability: encode levels to "Ready to move" and "Not ready to move"
- total_sqft: process total_sqft
- one-hot encode all categorical variables
"""


import xgboost as xgb
from feature_engine.encoding import OneHotEncoder
from feature_engine.wrappers import SklearnTransformerWrapper
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from home_price_analysis.config.core import config
from home_price_analysis.processing import features as pp

price_pipeline = Pipeline(
    [
        # === Processing features ===
        ("process_area_type", pp.area_type_step()),
        ("process_availability", pp.avail_step()),
        # === One-hot encoding (nominal variables) ===
        (
            "one_hot_encoder",
            OneHotEncoder(
                drop_last=True,  # avoid dummy variable trap
                variables=config.model_config.NOMINAL_VARS,
            ),
        ),
        # === standard scalar (continuous variables) ===
        (
            "standard_scalar",
            SklearnTransformerWrapper(
                transformer=StandardScaler(),
                variables=config.model_config.CONTINUOUS_VARS,
            ),
        ),
        # === model ===
        (
            "xgboost",
            xgb.XGBRegressor(
                n_estimators=config.model_config.N_ESTIMATORS,
                gamma=config.model_config.GAMMA,
                learning_rate=config.model_config.LEARNING_RATE,
                max_depth=config.model_config.MAX_DEPTH,
                subsample=config.model_config.SUBSAMPLE,
                colsample_bytree=config.model_config.COLSAMPLE_BYTREE,
            ),
        ),
    ]
)

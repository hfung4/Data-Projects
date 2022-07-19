from home_price_analysis.processing.utils import (
    preprocessing_area_type,
    preprocessing_size,
    preprocessing_total_sqft,
)


def test_preprocessing_total_sqft(raw):
    data = preprocessing_total_sqft(raw)
    assert data["total_sqft"].dtype == float
    assert data["total_sqft"].isnull().sum() == 0
    assert data["total_sqft"].max() < 53000


def test_preprocessing_size(raw):
    data = preprocessing_size(raw)
    assert data["size"].dtype == int
    assert data["size"].isnull().sum() == 0
    assert data["size"].max() < 44


def test_preprocessing_area_type(raw):
    data = preprocessing_area_type(raw)
    assert data["area_type"].dtype == "O"
    assert data["area_type"].value_counts().index[0] == "Super_built_up_Area"
    assert data["area_type"].value_counts().index[1] == "Built_up_Area"

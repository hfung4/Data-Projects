import math

import numpy as np
import pytest

from home_price_analysis.predict import make_prediction


@pytest.mark.filterwarnings("ignore::pandas.errors.PerformanceWarning")
def test_make_prediction(test_data):
    # Given
    expected_first_prediction_value = 54
    expected_number_of_predictions = 2608

    result = make_prediction(input_data=test_data)

    # Then
    predictions = result.get("predictions")
    assert isinstance(predictions, list)
    assert isinstance(predictions[0], np.float32)
    assert result.get("errors") is None
    assert len(predictions) == expected_number_of_predictions
    assert math.isclose(predictions[0], expected_first_prediction_value, abs_tol=20)

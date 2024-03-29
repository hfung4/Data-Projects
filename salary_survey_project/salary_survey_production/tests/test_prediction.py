import math

import numpy as np

from survey_analysis.predict import make_prediction


def test_make_prediction(test_data):
    # Given
    expected_first_prediction_value = 77000
    expected_number_of_predictions = 4285

    result = make_prediction(input_data=test_data)

    # Then
    predictions = result.get("predictions")
    assert isinstance(predictions, list)
    assert isinstance(predictions[0], np.float64)
    assert result.get("errors") is None
    assert len(predictions) == expected_number_of_predictions
    assert math.isclose(predictions[0], expected_first_prediction_value, abs_tol=1000)

from cr_analysis.predict import make_prediction


def test_make_prediction(get_test_data):
    # Given
    expected_number_of_predicted_1s = 470
    expected_number_of_predicted_2s = 1129
    expected_number_of_predicted_3s = 842
    expected_number_of_predicted_4s = 4893
    expected_number_of_predictions = 7334

    # Make prediction on the test data using the persisted trained pipeline
    test_res = make_prediction(input_data=get_test_data, is_raw_data=True)

    # Create final predictions dataframe
    df_final_predictions_test = test_res["test_ids"].copy()
    df_final_predictions_test["predicted_poverty_level"] = test_res["predictions"]

    # Then
    assert df_final_predictions_test.shape[0] == expected_number_of_predictions
    assert (
        df_final_predictions_test.query("predicted_poverty_level==1").shape[0]
        == expected_number_of_predicted_1s
    )
    assert (
        df_final_predictions_test.query("predicted_poverty_level==2").shape[0]
        == expected_number_of_predicted_2s
    )
    assert (
        df_final_predictions_test.query("predicted_poverty_level==3").shape[0]
        == expected_number_of_predicted_3s
    )
    assert (
        df_final_predictions_test.query("predicted_poverty_level==4").shape[0]
        == expected_number_of_predicted_4s
    )

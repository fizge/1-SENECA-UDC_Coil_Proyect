import pytest
from unittest.mock import MagicMock, patch
from tkinter import messagebox
from scenarios.modeling_scenario import Modeling


class MockModel:
    """
    A mock class to simulate a trained machine learning model.

    The predict method is designed to return double the input value for testing purposes.
    """
    def predict(self, data):
        if not isinstance(data, list) or len(data) != 1:
            raise ValueError("Invalid input for prediction")
        return [data[0][0] * 2]  # Mock behavior: Multiply input by 2


@pytest.fixture
def modeling_instance():
    """
    Fixture to provide an instance of the Modeling class with a mock model and app.

    Returns:
        Modeling: An instance of the Modeling class with predefined attributes for testing.
    """
    app_mock = MagicMock()
    app_mock.preselection.selected_input_column = "Feature1"
    app_mock.preselection.selected_output_column = "Target"
    modeling = Modeling(app_mock)
    modeling.model = MockModel()  # Use the MockModel for predictions
    modeling.graphic_frame = MagicMock()  # Mock graphic_frame to simulate UI behavior
    modeling.prediction_input = MagicMock()  # Mock prediction_input to simulate user input
    return modeling


@patch("tkinter.messagebox.showerror")
@patch("customtkinter.CTkLabel")
def test_make_prediction_valid_input(mock_ctk_label, mock_showerror, modeling_instance):
    """
    Test the `make_prediction` method with a valid input.

    Steps:
    1. Simulate user input of "10" in the prediction_input field.
    2. Call the `make_prediction` method.
    3. Verify that the CTkLabel is created with the correct prediction result.
    4. Ensure no error messages are displayed.

    Asserts:
        - The prediction label is created with the expected text "<Target> = 20.00".
        - No error messages are shown.
    """
    modeling_instance.prediction_input.get.return_value = "10"

    # Call the method
    modeling_instance.make_prediction()

    # Verify the prediction label
    mock_ctk_label.assert_called_once_with(modeling_instance.graphic_frame,
                                           text="<Target> = 20.00 ",
                                           font=("Arial", 17, 'bold'),
                                           text_color="white")


@patch("tkinter.messagebox.showerror")
def test_make_prediction_invalid_input(mock_showerror, modeling_instance):
    """
    Test the `make_prediction` method with invalid input.

    Steps:
    1. Simulate invalid user input (e.g., "invalid") in the prediction_input field.
    2. Call the `make_prediction` method.
    3. Verify that an error message is displayed indicating the need for a valid number.

    Asserts:
        - An error message is displayed with the appropriate text.
    """
    modeling_instance.prediction_input.get.return_value = "invalid"

    # Call the method
    modeling_instance.make_prediction()

    # Verify the error message
    mock_showerror.assert_called_once_with(
        "Error", "Please enter a valid number to make the prediction.")


@patch("tkinter.messagebox.showerror")
def test_make_prediction_generic_error(mock_showerror, modeling_instance):
    """
    Test the `make_prediction` method when a generic error occurs during prediction.

    Steps:
    1. Mock the predict method to raise a generic exception.
    2. Simulate valid user input in the prediction_input field (e.g., "5").
    3. Call the `make_prediction` method.
    4. Verify that an error message is displayed indicating the generic error.

    Asserts:
        - An error message is displayed with the specific exception text.
    """
    # Mock the predict method to raise an exception
    modeling_instance.model.predict = MagicMock(
        side_effect=Exception("Generic error"))

    modeling_instance.prediction_input.get.return_value = "5"

    # Call the method
    modeling_instance.make_prediction()

    # Verify the error message
    mock_showerror.assert_called_once_with(
        "Error", "An error occurred during prediction: Generic error")

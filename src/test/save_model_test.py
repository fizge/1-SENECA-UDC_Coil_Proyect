import pytest
from unittest.mock import patch, MagicMock
from logical.save_model import SavedModel

# MockModel class to simulate the behavior of a trained linear regression model
class MockModel:
    """
    A mock class to simulate a trained linear regression model.
    """
    def __init__(self, coef, intercept):
        self.coef_ = coef
        self.intercept_ = intercept


@pytest.fixture
def saved_model():
    """
    Fixture to create a valid SavedModel object for testing.

    Returns:
        SavedModel: An instance of the SavedModel class with mock data.
    """
    model = MockModel([0.5], 1.2)
    return SavedModel(
        model=model,
        input_column="Feature1",
        output_column="Target",
        r_squared=0.85,
        mse=0.15,
        description="Test model description"
    )

# Test: Validation for null model
@patch("tkinter.messagebox.showerror")
def test_save_model_no_model(mock_error):
    """
    Test to ensure an error is raised when trying to save a null model.

    Asserts:
        - showerror is called with the appropriate error message.
    """
    saved_model = SavedModel(
        model=None,
        input_column="Feature1",
        output_column="Target",
        r_squared=0.85,
        mse=0.15,
        description="Test model description"
    )
    saved_model.save_model()
    mock_error.assert_called_once_with(
        "Error", "No model available to save. Generate a model first.")

# Test: Validation for missing columns
@patch("tkinter.messagebox.showerror")
def test_save_model_missing_columns(mock_error):
    """
    Test to ensure an error is raised when input or output columns are missing.

    Asserts:
        - showerror is called with the appropriate error message.
    """
    saved_model = SavedModel(
        model=MockModel([0.5], 1.2),
        input_column=None,  # Missing input_column
        output_column="Target",
        r_squared=0.85,
        mse=0.15,
        description="Test model description"
    )
    saved_model.save_model()
    mock_error.assert_called_once_with(
        "Error", "No model available to save. Generate a model first.")

# Test: Empty description warning
@patch("tkinter.messagebox.showwarning")
def test_save_model_empty_description(mock_warning):
    """
    Test to ensure a warning is raised when the model description is empty.

    Asserts:
        - showwarning is called with the appropriate warning message.
    """
    saved_model = SavedModel(
        model=MockModel([0.5], 1.2),
        input_column="Feature1",
        output_column="Target",
        r_squared=0.85,
        mse=0.15,
        description=""  # Empty description
    )
    saved_model.save_model()
    mock_warning.assert_called_once_with(
        "Warning", "You have not written anything in the description.")

# Test: Successful save
@patch("tkinter.filedialog.asksaveasfilename", return_value="/tmp/test_model.pkl")
@patch("tkinter.messagebox.showinfo")
def test_save_model_success(mock_info, mock_asksave, tmp_path):
    """
    Test to ensure the model is saved successfully when all data is valid.

    Asserts:
        - The saved file exists and is not empty.
        - showinfo is called with the appropriate success message.
    """
    test_file = tmp_path / "test_model.pkl"
    mock_asksave.return_value = str(test_file)

    saved_model = SavedModel(
        model=MockModel([0.5], 1.2),
        input_column="Feature1",
        output_column="Target",
        r_squared=0.85,
        mse=0.15,
        description="Test model description"
    )

    saved_model.save_model()

    # Verify that the file was created successfully
    assert test_file.exists(), "The file was not created."
    assert test_file.stat().st_size > 0, "The file is empty."

    # Verify the success message matches the format in the code
    mock_info.assert_called_once_with(
        "Success", f"Model saved successfully to:\n{test_file}")

# Test: File write error
@patch("tkinter.messagebox.showerror")
@patch("tkinter.filedialog.asksaveasfilename", return_value="/tmp/test_model.pkl")
def test_save_model_write_error(mock_asksave, mock_error):
    """
    Test to ensure an error message is shown if file writing fails.

    Asserts:
        - showerror is called with the appropriate error message.
    """
    saved_model = SavedModel(
        model=MockModel([0.5], 1.2),
        input_column="Feature1",
        output_column="Target",
        r_squared=0.85,
        mse=0.15,
        description="Test model description"
    )

    # Simulate a file writing error
    with patch("builtins.open", side_effect=Exception("Write error")):
        saved_model.save_model()

    # Verify the error message is displayed
    mock_error.assert_called_once_with(
        "Error", "Failed to save the model: Write error")

# Test: Formula validation
def test_save_model_formula():
    """
    Test to validate that the formula generated for the linear regression model is correct.

    Asserts:
        - The formula matches the expected output.
    """
    saved_model = SavedModel(
        model=MockModel([0.5], 1.2),
        input_column="Feature1",
        output_column="Target",
        r_squared=0.85,
        mse=0.15,
        description="Test model description"
    )

    formula = f"{saved_model.output_column} = ({saved_model.model.coef_[0]:.4f}) * ({saved_model.input_column}) + ({saved_model.model.intercept_:.4f})"
    assert formula == "Target = (0.5000) * (Feature1) + (1.2000)", "The generated formula is incorrect."

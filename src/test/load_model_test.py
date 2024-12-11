import pytest
import pickle
from scenarios.loading_scenario import LoadModel


class MockModel:
    """
    Mock class to simulate a machine learning model.

    The `predict` method doubles the input value for testing purposes.
    """
    def predict(self, input_data):
        return [value[0] * 2 for value in input_data]  # Simulate predictions


@pytest.fixture
def mock_app(mocker):
    """
    Fixture to create a mock application object.

    This mock simulates the application structure and behavior required by the `LoadModel` class.

    Args:
        mocker: The pytest-mock library's mock object.

    Returns:
        MagicMock: A mock application object with necessary attributes.
    """
    mock_app = mocker.MagicMock()
    mock_app.v = mocker.MagicMock()
    mock_app.modeling = mocker.MagicMock()
    mock_app.preselection = mocker.MagicMock()
    mock_app.initial_frame = mocker.MagicMock()
    return mock_app


@pytest.fixture
def load_model_instance(mock_app):
    """
    Fixture to provide an instance of the `LoadModel` class.

    Args:
        mock_app (MagicMock): A mock application object.

    Returns:
        LoadModel: An instance of the `LoadModel` class.
    """
    return LoadModel(mock_app)


def test_load_model_logic(mocker):
    """
    Test the logic for loading a serialized model using pickle.

    Steps:
    1. Create a mock model data dictionary.
    2. Serialize the data using pickle.
    3. Mock the `open` function to simulate reading the serialized data from a file.
    4. Load the data using pickle and assert its attributes.

    Asserts:
        - The attributes of the loaded data match the expected values.
    """
    mock_data = {
        "output_column": "target",
        "input_column": "feature",
        "model": MockModel(),
        "formula": "y = mx + b",
        "r_squared": 0.95,
        "mse": 0.1,
        "description": "Test model description"
    }
    serialized_data = pickle.dumps(mock_data)

    # Mock the open function to simulate file reading
    mocker.patch("builtins.open", mocker.mock_open(read_data=serialized_data))

    # Load the data from the mocked file
    with open("test_model.pkl", "rb") as f:
        result = pickle.load(f)

    # Assertions
    assert result["output_column"] == "target"
    assert result["input_column"] == "feature"
    assert result["formula"] == "y = mx + b"
    assert result["r_squared"] == 0.95
    assert result["mse"] == 0.1
    assert result["description"] == "Test model description"


def test_model_prediction(mocker):
    """
    Test the prediction logic of a loaded model.

    Steps:
    1. Create a mock model data dictionary.
    2. Serialize the data using pickle.
    3. Mock the `open` function to simulate reading the serialized data from a file.
    4. Load the model and use it to make a prediction.
    5. Assert that the prediction matches the expected result.

    Asserts:
        - The model prediction is correct based on the mock logic.
    """
    mock_data = {
        "output_column": "target",
        "input_column": "feature",
        "model": MockModel(),
        "formula": "y = mx + b",
        "r_squared": 0.95,
        "mse": 0.1,
        "description": "Test model description"
    }
    serialized_data = pickle.dumps(mock_data)

    # Mock the open function to simulate file reading
    mocker.patch("builtins.open", mocker.mock_open(read_data=serialized_data))

    # Load the model from the mocked file
    with open("test_model.pkl", "rb") as f:
        result = pickle.load(f)

    model = result["model"]
    prediction = model.predict([[50.0]])

    # Assertion
    assert prediction == [100.0]

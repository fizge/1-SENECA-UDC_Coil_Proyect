import pytest
import pickle
from scenarios.loading_scenario import LoadModel


class MockModel:
    def predict(self, input_data):
        return [value[0] * 2 for value in input_data]


@pytest.fixture
def mock_app(mocker):
    mock_app = mocker.MagicMock()
    mock_app.v = mocker.MagicMock()
    mock_app.modeling = mocker.MagicMock()
    mock_app.preselection = mocker.MagicMock()
    mock_app.initial_frame = mocker.MagicMock()
    return mock_app


@pytest.fixture
def load_model_instance(mock_app):
    return LoadModel(mock_app)


def test_load_model_logic(mocker):
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

    mocker.patch("builtins.open", mocker.mock_open(read_data=serialized_data))

    with open("test_model.pkl", "rb") as f:
        result = pickle.load(f)

    assert result["output_column"] == "target"
    assert result["input_column"] == "feature"
    assert result["formula"] == "y = mx + b"
    assert result["r_squared"] == 0.95
    assert result["mse"] == 0.1
    assert result["description"] == "Test model description"


def test_model_prediction(mocker):
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

    mocker.patch("builtins.open", mocker.mock_open(read_data=serialized_data))

    with open("test_model.pkl", "rb") as f:
        result = pickle.load(f)

    model = result["model"]
    prediction = model.predict([[50.0]])

    assert prediction == [100.0]

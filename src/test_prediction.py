import pytest
from unittest.mock import MagicMock, patch
from tkinter import messagebox
from loading_scenario import LoadModel

# Clase MockModel para simular el modelo
class MockModel:
    def predict(self, data):
        if not isinstance(data, list) or len(data) != 1:
            raise ValueError("Invalid input for prediction")
        return [sum(data[0])]

@pytest.fixture
def load_model_instance():
    """Crea una instancia de LoadModel con un modelo simulado."""
    app_mock = MagicMock()
    load_model = LoadModel(app_mock)
    load_model.model = MockModel()
    load_model.input_column = "Feature1"
    load_model.output_column = "Target"
    load_model.info_frame = MagicMock()
    return load_model

# Test: Predicción con entrada válida
def test_prediction_valid_input(load_model_instance):
    load_model_instance.prediction_input = MagicMock()
    load_model_instance.prediction_input.get.return_value = "10"
    load_model_instance.prediction_res_label = None

    load_model_instance.prediction_loaded_model()

    assert load_model_instance.prediction_res_label is not None
    assert load_model_instance.prediction_res_label.cget("text") == "<Target> = 10.00"

# Test: Predicción con entrada no válida (texto)
@patch("tkinter.messagebox.showerror")
def test_prediction_invalid_input(mock_showerror, load_model_instance):
    load_model_instance.prediction_input = MagicMock()
    load_model_instance.prediction_input.get.return_value = "invalid"

    load_model_instance.prediction_loaded_model()

    mock_showerror.assert_called_once_with("Error", "Please enter a valid number to make the prediction.")

# Test: Modelo no disponible
@patch("tkinter.messagebox.showerror")
def test_prediction_no_model(mock_showerror):
    app_mock = MagicMock()
    load_model = LoadModel(app_mock)
    load_model.input_column = None
    load_model.output_column = None

    load_model.prediction_loaded_model()

    mock_showerror.assert_called_once_with("Error", "No se pudo obtener el modelo o las columnas del archivo.")

# Test: Error genérico durante la predicción
@patch("tkinter.messagebox.showerror")
def test_prediction_generic_error(mock_showerror, load_model_instance):
    load_model_instance.model.predict = MagicMock(side_effect=Exception("Generic error"))

    load_model_instance.prediction_input = MagicMock()
    load_model_instance.prediction_input.get.return_value = "5"

    load_model_instance.prediction_loaded_model()

    mock_showerror.assert_called_once_with("Error", "An error occurred during prediction: Generic error")

import pytest
from unittest.mock import MagicMock, patch
from tkinter import messagebox
from modeling_scenario import Modeling  # Asegúrate de que el nombre y la ruta son correctos

# Mock de LinearRegression para simular el modelo
class MockModel:
    def predict(self, data):
        if not isinstance(data, list) or len(data) != 1:
            raise ValueError("Invalid input for prediction")
        return [data[0][0] * 2]  # Simula una predicción simple (por ejemplo, 2 * input_value)

@pytest.fixture
def modeling_instance():
    """Crea una instancia de Modeling con un modelo simulado."""
    app_mock = MagicMock()
    app_mock.preselection.selected_input_column = "Feature1"
    app_mock.preselection.selected_output_column = "Target"
    modeling = Modeling(app_mock)
    modeling.model = MockModel()  # Asigna el modelo simulado
    modeling.graphic_frame = MagicMock()  # Mock de la interfaz gráfica
    modeling.prediction_input = MagicMock()  # Mock del campo de entrada de predicción
    return modeling

# Test: Predicción con entrada válida
@patch("tkinter.messagebox.showerror")  # Mock de showerror para evitar ventanas emergentes
@patch("customtkinter.CTkLabel")  # Mock de CTkLabel para evitar la creación real de la etiqueta
def test_make_prediction_valid_input(mock_ctk_label, mock_showerror, modeling_instance):
    # Simula la entrada de predicción
    modeling_instance.prediction_input.get.return_value = "10"
    
    # Hacemos la predicción
    modeling_instance.make_prediction()

    # Verifica que la etiqueta de predicción fue llamada correctamente con el texto esperado
    mock_ctk_label.assert_called_once_with(modeling_instance.graphic_frame,
                                           text="<Target> = 20.00 ",  # Se añadió el espacio extra aquí
                                           font=("Arial", 17, 'bold'),
                                           text_color="white")

# Test: Predicción con entrada no válida
@patch("tkinter.messagebox.showerror")  # Mock de showerror para evitar ventanas emergentes
def test_make_prediction_invalid_input(mock_showerror, modeling_instance):
    # Simula una entrada inválida
    modeling_instance.prediction_input.get.return_value = "invalid"
    
    # Llamamos a la función de predicción
    modeling_instance.make_prediction()

    # Verifica que se muestra el mensaje de error adecuado
    mock_showerror.assert_called_once_with("Error", "Please enter a valid number to make the prediction.")

# Test: Error genérico durante la predicción
@patch("tkinter.messagebox.showerror")  # Mock de showerror para evitar ventanas emergentes
def test_make_prediction_generic_error(mock_showerror, modeling_instance):
    # Simula que ocurre un error inesperado en la predicción
    modeling_instance.model.predict = MagicMock(side_effect=Exception("Generic error"))
    
    modeling_instance.prediction_input.get.return_value = "5"
    
    # Llamamos a la función de predicción
    modeling_instance.make_prediction()

    # Verifica que se muestra el mensaje de error adecuado
    mock_showerror.assert_called_once_with("Error", "An error occurred during prediction: Generic error")
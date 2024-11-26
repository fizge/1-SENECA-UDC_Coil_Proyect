import pytest
from unittest.mock import Mock
from loading_scenario import LoadModel  
import pytest
from unittest.mock import Mock, patch
from loading_scenario import LoadModel


import customtkinter as ctk

@pytest.fixture
def mock_app():
    app = Mock()
    app.preselection = Mock()
    app.modeling = Mock()
    app.v = ctk.CTk()
    return app


class SerializableModel:
    def predict(self, X):
        return [250000] * len(X)  

@pytest.fixture
def mock_saved_model(tmp_path):
    """Crea un archivo de modelo simulado para pruebas."""
    model_data = {
        "output_column": "house_price",
        "input_column": "total_rooms",
        "model": SerializableModel(),  # Modelo serializable
        "formula": "house_price = 0.97 * total_rooms + 5000",
        "r_squared": 0.97,
        "mse": 9.3,
        "description": "Test model"
    }
    file_path = tmp_path / "test_model.pkl"
    with open(file_path, "wb") as f:
        import pickle
        pickle.dump(model_data, f)
    return str(file_path)



def test_load_model(mock_app, mock_saved_model):
    """Prueba el método load_model para cargar un modelo guardado."""
    # Crear instancia de LoadModel con mock_app
    loader = LoadModel(mock_app)

    # Simular selección de archivo y cargar modelo
    with patch("loading_scenario.filedialog.askopenfilename", return_value=mock_saved_model):
        with patch("loading_scenario.messagebox.showinfo") as mock_info:
            loader.load_model()

            # Verificar que los atributos del modelo se establecen correctamente
            assert loader.output_column == "house_price"
            assert loader.input_column == "total_rooms"
            assert callable(loader.model.predict)  # Verifica que el modelo tenga un método predict
            assert loader.formula == "house_price = 0.97 * total_rooms + 5000"
            assert loader.r_squared == 0.97
            assert loader.mse == 9.3
            assert loader.description == "Test model"

            # Verificar que se muestra un mensaje de éxito
            mock_info.assert_called_once_with(
                "Recovered model",
                "Recovered model. Output Column: house_price, Input Column: total_rooms"
            )


def test_load_model_error(mock_app, tmp_path):
    """Prueba el manejo de errores al cargar un modelo."""
    # Crear un archivo corrupto
    corrupted_file_path = tmp_path / "corrupt_model.pkl"
    with open(corrupted_file_path, "wb") as f:
        f.write(b"not a pickle")

    # Crear instancia de LoadModel con mock_app
    loader = LoadModel(mock_app)

    # Simular selección de archivo corrupto
    with patch("loading_scenario.filedialog.askopenfilename", return_value=str(corrupted_file_path)):
        with patch("loading_scenario.messagebox.showerror") as mock_error:
            loader.load_model()

    # Verificar que se muestra un mensaje de error
    mock_error.assert_called_once()
    error_message = mock_error.call_args[0][1]
    assert "No se pudo cargar el archivo" in error_message


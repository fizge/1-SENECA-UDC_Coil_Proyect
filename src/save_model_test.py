import pytest
from unittest.mock import patch, MagicMock
from save_model import SavedModel

# Clase MockModel para simular el modelo
class MockModel:
    def __init__(self, coef, intercept):
        self.coef_ = coef
        self.intercept_ = intercept

@pytest.fixture
def saved_model():
    """Fixture que crea un objeto SavedModel con datos válidos."""
    model = MockModel([0.5], 1.2)
    return SavedModel(
        model=model,
        input_column="Feature1",
        output_column="Target",
        r_squared=0.85,
        mse=0.15,
        description="Test model description"
    )

# Test: Validación de modelo nulo
@patch("tkinter.messagebox.showerror")
def test_save_model_no_model(mock_error):
    saved_model = SavedModel(
        model=None,
        input_column="Feature1",
        output_column="Target",
        r_squared=0.85,
        mse=0.15,
        description="Test model description"
    )
    saved_model.save_model()
    mock_error.assert_called_once_with("Error", "No model available to save. Generate a model first.")

# Test: Validación de columnas faltantes
@patch("tkinter.messagebox.showerror")
def test_save_model_missing_columns(mock_error):
    saved_model = SavedModel(
        model=MockModel([0.5], 1.2),
        input_column=None,  # Falta input_column
        output_column="Target",
        r_squared=0.85,
        mse=0.15,
        description="Test model description"
    )
    saved_model.save_model()
    mock_error.assert_called_once_with("Error", "No model available to save. Generate a model first.")

# Test: Descripción vacía
@patch("tkinter.messagebox.showwarning")
def test_save_model_empty_description(mock_warning):
    saved_model = SavedModel(
        model=MockModel([0.5], 1.2),
        input_column="Feature1",
        output_column="Target",
        r_squared=0.85,
        mse=0.15,
        description=""  # Descripción vacía
    )
    saved_model.save_model()
    mock_warning.assert_called_once_with("Warning", "You have not written anything in the description.")

# Test: Guardado exitoso
@patch("tkinter.filedialog.asksaveasfilename", return_value="/tmp/test_model.pkl")
@patch("tkinter.messagebox.showinfo")
def test_save_model_success(mock_info, mock_asksave, tmp_path):
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

    # Verifica que el archivo se creó correctamente
    assert test_file.exists(), "El archivo no fue creado."
    assert test_file.stat().st_size > 0, "El archivo está vacío."

    # Verifica que el mensaje de éxito coincide con el formato del código
    mock_info.assert_called_once_with("Success", f"Model saved successfully to:{test_file}")


# Test: Error de escritura en archivo
@patch("tkinter.messagebox.showerror")
@patch("tkinter.filedialog.asksaveasfilename", return_value="/tmp/test_model.pkl")
def test_save_model_write_error(mock_asksave, mock_error):
    saved_model = SavedModel(
        model=MockModel([0.5], 1.2),
        input_column="Feature1",
        output_column="Target",
        r_squared=0.85,
        mse=0.15,
        description="Test model description"
    )

    # Simula un error al abrir el archivo
    with patch("builtins.open", side_effect=Exception("Error de escritura")):
        saved_model.save_model()

    # Verifica que se muestra un mensaje de error con el texto correcto
    mock_error.assert_called_once_with("Error", "Failed to save the model: Error de escritura")

# Test: Validación de fórmula
def test_save_model_formula():
    saved_model = SavedModel(
        model=MockModel([0.5], 1.2),
        input_column="Feature1",
        output_column="Target",
        r_squared=0.85,
        mse=0.15,
        description="Test model description"
    )

    formula = f"{saved_model.output_column} = ({saved_model.model.coef_[0]:.4f}) * ({saved_model.input_column}) + ({saved_model.model.intercept_:.4f})"
    assert formula == "Target = (0.5000) * (Feature1) + (1.2000)", "La fórmula generada no es correcta."

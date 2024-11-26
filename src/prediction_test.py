import pytest
from unittest.mock import MagicMock, patch
from tkinter import messagebox
from modeling_scenario import Modeling  

class MockModel:
    def predict(self, data):
        if not isinstance(data, list) or len(data) != 1:
            raise ValueError("Invalid input for prediction")
        return [data[0][0] * 2]  

@pytest.fixture
def modeling_instance():
    app_mock = MagicMock()
    app_mock.preselection.selected_input_column = "Feature1"
    app_mock.preselection.selected_output_column = "Target"
    modeling = Modeling(app_mock)
    modeling.model = MockModel() 
    modeling.graphic_frame = MagicMock()  
    modeling.prediction_input = MagicMock()  
    return modeling

@patch("tkinter.messagebox.showerror") 
@patch("customtkinter.CTkLabel")  
def test_make_prediction_valid_input(mock_ctk_label, mock_showerror, modeling_instance):
    modeling_instance.prediction_input.get.return_value = "10"
    
    modeling_instance.make_prediction()

    mock_ctk_label.assert_called_once_with(modeling_instance.graphic_frame,
                                           text="<Target> = 20.00 ",  
                                           font=("Arial", 17, 'bold'),
                                           text_color="white")

@patch("tkinter.messagebox.showerror")  
def test_make_prediction_invalid_input(mock_showerror, modeling_instance):
    modeling_instance.prediction_input.get.return_value = "invalid"
    
    modeling_instance.make_prediction()

    mock_showerror.assert_called_once_with("Error", "Please enter a valid number to make the prediction.")

@patch("tkinter.messagebox.showerror") 
def test_make_prediction_generic_error(mock_showerror, modeling_instance):
    modeling_instance.model.predict = MagicMock(side_effect=Exception("Generic error"))
    
    modeling_instance.prediction_input.get.return_value = "5"

    modeling_instance.make_prediction()

    mock_showerror.assert_called_once_with("Error", "An error occurred during prediction: Generic error")
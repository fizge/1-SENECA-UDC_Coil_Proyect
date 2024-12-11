import pytest
from sklearn.linear_model import LinearRegression
import pandas as pd
from scenarios.modeling_scenario import Modeling
from sklearn.metrics import r2_score, mean_squared_error


@pytest.fixture
def sample_data():
    """
    Fixture to provide sample data for testing.

    Returns:
        pd.DataFrame: A dataframe containing an 'input_column' and 'output_column' 
                      with values following a linear relationship.
    """
    return pd.DataFrame({
        'input_column': [1, 2, 3, 4, 5],
        'output_column': [2, 4, 6, 8, 10]
    })


def test_generate_model(sample_data):
    """
    Test the `generate_model` method of the Modeling class.

    This test validates:
    - A linear regression model is generated correctly.
    - The generated model is an instance of `LinearRegression`.
    - The calculated R² (coefficient of determination) and MSE (mean squared error)
      are correct and match expected values.

    Steps:
    1. Mock the app and its dependencies (`preselection` and dataset).
    2. Initialize the Modeling class with the mocked app.
    3. Call `generate_model` to train a model on the sample data.
    4. Validate the following:
       - The model exists and is of type `LinearRegression`.
       - R² and MSE match the expected metrics calculated independently.

    Args:
        sample_data (pd.DataFrame): Sample dataset provided by the fixture.
    """
    # Mock application and its preselection component
    app_mock = type('MockApp', (), {})()
    app_mock.v = None
    app_mock.preselection = type('MockPreselection', (), {})()
    app_mock.preselection.loaded_data = sample_data
    app_mock.preselection.selected_input_column = 'input_column'
    app_mock.preselection.selected_output_column = 'output_column'

    # Initialize the Modeling class and generate the model
    modeling = Modeling(app_mock)
    modeling.generate_model()

    # Validate that a model was created and is of the correct type
    assert modeling.model is not None, "Model was not generated."
    assert isinstance(modeling.model, LinearRegression), "Generated model is not of type LinearRegression."

    # Extract data for validation
    X = app_mock.preselection.loaded_data[['input_column']]
    y = app_mock.preselection.loaded_data['output_column']
    predictions = modeling.model.predict(X)

    # Calculate expected metrics
    expected_r2 = r2_score(y, predictions)
    expected_mse = mean_squared_error(y, predictions)

    # Validate R² and MSE
    assert modeling.r_squared == pytest.approx(expected_r2, rel=1e-3), "R² value does not match the expected value."
    assert modeling.mse == pytest.approx(expected_mse, rel=1e-3), "MSE value does not match the expected value."

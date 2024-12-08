

import pytest
from sklearn.linear_model import LinearRegression
import pandas as pd
from scenarios.modeling_scenario import Modeling
from sklearn.metrics import r2_score, mean_squared_error


@pytest.fixture
def sample_data():

    return pd.DataFrame({
        'input_column': [1, 2, 3, 4, 5],
        'output_column': [2, 4, 6, 8, 10]
    })


def test_generate_model(sample_data):
    app_mock = type('MockApp', (), {})()
    app_mock.v = None
    app_mock.preselection = type('MockPreselection', (), {})()
    app_mock.preselection.loaded_data = sample_data
    app_mock.preselection.selected_input_column = 'input_column'
    app_mock.preselection.selected_output_column = 'output_column'

    modeling = Modeling(app_mock)
    modeling.generate_model()

    assert modeling.model is not None
    assert isinstance(modeling.model, LinearRegression)

    X = app_mock.preselection.loaded_data[['input_column']]
    y = app_mock.preselection.loaded_data['output_column']
    predictions = modeling.model.predict(X)

    expected_r2 = r2_score(y, predictions)
    expected_mse = mean_squared_error(y, predictions)

    assert modeling.r_squared == pytest.approx(expected_r2, rel=1e-3)
    assert modeling.mse == pytest.approx(expected_mse, rel=1e-3)

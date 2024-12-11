from unittest.mock import MagicMock
import pytest
import pandas as pd
from scenarios.preselection_scenario import Preselection


class MockApp:
    """
    Mock class to simulate the behavior of the main application used in the Preselection scenario.
    """
    def __init__(self):
        self.v = MagicMock()
        self.deleted_rows = MagicMock()
        self.output_select = MagicMock()
        self.modeling = MagicMock()
        self.load = MagicMock()
        self.modeling.graphic_frame = None


@pytest.fixture
def preselection():
    """
    Fixture to provide an instance of the Preselection class with a mock application.

    Returns:
        Preselection: An instance of the Preselection class.
    """
    app = MockApp()
    preselection_instance = Preselection(app)
    return preselection_instance


def test_fill_na_values_mean(preselection):
    """
    Test the functionality of `fill_na_values` when filling NaN values with the mean.

    Steps:
    1. Create a DataFrame with NaN values.
    2. Call the `fill_na_values` method with the "Fill with Mean" option.
    3. Assert that `display_data_in_treeview` is called with the updated DataFrame.
    4. Verify that the method is called exactly once.

    Asserts:
        - The updated DataFrame is displayed in the treeview.
        - The method call count is 1.
    """
    preselection.original_data = pd.DataFrame(
        {"A": [1, None, 3], "B": [4, 5, None]})
    preselection.loaded_data = preselection.original_data.copy()

    # Mock the display function
    preselection.display_data_in_treeview = MagicMock()

    # Call the method
    preselection.fill_na_values("Fill with Mean", ["A", "B"])

    # Assertions
    preselection.display_data_in_treeview.assert_called_with(
        preselection.loaded_data)
    assert preselection.display_data_in_treeview.call_count == 1


def test_fill_na_values_median(preselection):
    """
    Test the functionality of `fill_na_values` when filling NaN values with the median.

    Steps:
    1. Create a DataFrame with NaN values.
    2. Call the `fill_na_values` method with the "Fill with Median" option.
    3. Assert that `display_data_in_treeview` is called with the updated DataFrame.
    4. Verify that the method is called exactly once.

    Asserts:
        - The updated DataFrame is displayed in the treeview.
        - The method call count is 1.
    """
    preselection.original_data = pd.DataFrame(
        {"A": [2, None, 13], "B": [64, 985, None]})
    preselection.loaded_data = preselection.original_data.copy()

    # Mock the display function
    preselection.display_data_in_treeview = MagicMock()

    # Call the method
    preselection.fill_na_values("Fill with Median", ["A", "B"])

    # Assertions
    preselection.display_data_in_treeview.assert_called_with(
        preselection.loaded_data)
    assert preselection.display_data_in_treeview.call_count == 1


@pytest.fixture
def preselection3():
    """
    Fixture to provide an instance of the Preselection class with a specific DataFrame 
    containing NaN values for testing row removal.

    Returns:
        Preselection: An instance of the Preselection class with predefined attributes.
    """
    app = MagicMock()
    preselection_instance = Preselection(app)
    preselection_instance.original_data = pd.DataFrame({
        "A": [1, None, 3],
        "B": [4, 5, None],
    })
    preselection_instance.loaded_data = preselection_instance.original_data.copy()
    preselection_instance.selected_input_column = "A"
    preselection_instance.selected_output_column = "B"
    return preselection_instance


def test_remove_nan_rows(preselection3):
    """
    Test the functionality of `apply_preprocessing` when removing rows with NaN values.

    Steps:
    1. Use a fixture to provide a DataFrame containing NaN values.
    2. Call the `apply_preprocessing` method with the "Remove rows with NaN" option.
    3. Assert that the resulting DataFrame has only non-NaN rows.
    4. Assert that `display_data_in_treeview` is called with the updated DataFrame.
    5. Verify that the method is called exactly once.

    Asserts:
        - The resulting DataFrame contains only rows without NaN values.
        - The updated DataFrame is displayed in the treeview.
        - The method call count is 1.
    """
    # Mock the display function
    preselection3.display_data_in_treeview = MagicMock()

    # Call the method to remove NaN rows
    preselection3.apply_preprocessing("Remove rows with NaN")

    # Assertions
    assert preselection3.loaded_data.shape[0] == 1
    assert preselection3.loaded_data["A"].iloc[0] == 1
    assert preselection3.loaded_data["B"].iloc[0] == 4

    preselection3.display_data_in_treeview.assert_called_once_with(
        preselection3.loaded_data)
    assert preselection3.display_data_in_treeview.call_count == 1

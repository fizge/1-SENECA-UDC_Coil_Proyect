from unittest.mock import MagicMock
import pytest
from unittest.mock import MagicMock
import pandas as pd
from scenarios.preselection_scenario import Preselection


class MockApp:
    def __init__(self):
        self.v = MagicMock()
        self.deleted_rows = MagicMock()
        self.output_select = MagicMock()
        self.modeling = MagicMock()
        self.load = MagicMock()

        self.modeling.graphic_frame = None


@pytest.fixture
def preselection():
    app = MockApp()
    preselection_instance = Preselection(app)
    return preselection_instance


def test_fill_na_values_mean(preselection):
    preselection.original_data = pd.DataFrame(
        {"A": [1, None, 3], "B": [4, 5, None]})
    preselection.loaded_data = preselection.original_data.copy()

    preselection.display_data_in_treeview = MagicMock()

    preselection.fill_na_values("Fill with Mean", ["A", "B"])

    preselection.display_data_in_treeview.assert_called_with(
        preselection.loaded_data)
    assert preselection.display_data_in_treeview.call_count == 1


def test_fill_na_values_median(preselection):
    preselection.original_data = pd.DataFrame(
        {"A": [2, None, 13], "B": [64, 985, None]})
    preselection.loaded_data = preselection.original_data.copy()

    preselection.display_data_in_treeview = MagicMock()

    preselection.fill_na_values("Fill with Median", ["A", "B"])

    preselection.display_data_in_treeview.assert_called_with(
        preselection.loaded_data)
    assert preselection.display_data_in_treeview.call_count == 1


@pytest.fixture
def preselection3():
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

    preselection3.display_data_in_treeview = MagicMock()
    preselection3.apply_preprocessing("Remove rows with NaN")

    assert preselection3.loaded_data.shape[0] == 1
    assert preselection3.loaded_data["A"].iloc[0] == 1
    assert preselection3.loaded_data["B"].iloc[0] == 4

    preselection3.display_data_in_treeview.assert_called_once_with(
        preselection3.loaded_data)
    assert preselection3.display_data_in_treeview.call_count == 1

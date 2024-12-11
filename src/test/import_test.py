import pytest
import pandas as pd
from logical.file_reader import FileReader
import sqlite3
from unittest.mock import MagicMock
from scenarios.preselection_scenario import Preselection


class MockApp:
    """
    Mock class to simulate the application structure used in Preselection.

    Attributes:
        v: Mocked main application frame.
        deleted_rows: Mocked object for deleted rows handling.
        output_select: Mocked object for output column selection.
        modeling: Mocked object for modeling-related functionality.
        load: Mocked object for loading models.
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
    Fixture to provide an instance of the Preselection class with a mocked app.

    Returns:
        Preselection: An instance of the Preselection class.
    """
    app = MockApp()
    preselection_instance = Preselection(app)
    return preselection_instance


def test_import_data(preselection):
    """
    Test the `import_data` method for various file types.

    Steps:
    1. Mock the application's UI components.
    2. Simulate importing data from various file formats.
    3. Assert that `original_data` is populated for valid formats.

    Asserts:
        - `original_data` is not None after importing valid files.
    """
    preselection.app.v = MagicMock()
    preselection.tree = None
    preselection.original_data = pd.DataFrame(
        {"A": [1, None, 5, 7], "B": [3, 4, None, 90]})
    preselection.import_data("data.db")
    assert preselection.original_data is not None
    preselection.import_data("data.xlsx")
    assert preselection.original_data is not None
    preselection.import_data("data.csv")
    assert preselection.original_data is not None
    preselection.import_data("data.sqlite")
    assert preselection.original_data is not None
    preselection.import_data("data.xls")
    assert preselection.original_data is not None


@pytest.fixture
def file_reader():
    """
    Fixture to provide an instance of the FileReader class.

    Returns:
        FileReader: An instance of the FileReader class.
    """
    return FileReader()


@pytest.fixture
def excel_test_paths(tmp_path):
    """
    Fixture to create test Excel files in various configurations.

    Args:
        tmp_path: A temporary directory provided by pytest.

    Returns:
        dict: Paths to single-sheet, empty, and multi-sheet Excel files.
    """
    excel_path = tmp_path / "test.xlsx"
    df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    df.to_excel(excel_path, index=False)

    empty_excel_path = tmp_path / "empty.xlsx"
    pd.DataFrame().to_excel(empty_excel_path, index=False)

    multi_sheet_excel_path = tmp_path / "multi_sheet.xlsx"
    with pd.ExcelWriter(multi_sheet_excel_path) as writer:
        df.to_excel(writer, sheet_name="Sheet1", index=False)
        pd.DataFrame({"colA": [10, 20], "colB": [30, 40]}).to_excel(
            writer, sheet_name="Sheet2", index=False)

    return {
        "excel": excel_path,
        "empty_excel": empty_excel_path,
        "multi_sheet_excel": multi_sheet_excel_path,
    }


def test_read_csv_success(file_reader, tmp_path):
    """
    Test successful reading of a CSV file using FileReader.

    Asserts:
        - The data frame read from the file matches the expected content.
    """
    csv_path = tmp_path / "test.csv"
    df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    df.to_csv(csv_path, index=False)

    result = file_reader.read_csv_or_excel(csv_path)
    pd.testing.assert_frame_equal(result, df)


def test_read_excel_success(file_reader, excel_test_paths):
    """
    Test successful reading of a single-sheet Excel file using FileReader.

    Asserts:
        - The data frame read from the file matches the expected content.
    """
    result = file_reader.read_csv_or_excel(excel_test_paths["excel"])
    pd.testing.assert_frame_equal(
        result, pd.DataFrame({"col1": [1, 2], "col2": [3, 4]}))


def test_open_file_empty_excel(file_reader, excel_test_paths):
    """
    Test reading an empty Excel file using FileReader.

    Asserts:
        - The result is a non-null but empty data frame.
    """
    result = file_reader.read_csv_or_excel(excel_test_paths["empty_excel"])
    assert result is not None
    assert result.empty


def test_open_file_multi_sheet_excel(file_reader, excel_test_paths):
    """
    Test reading a multi-sheet Excel file using FileReader.

    Asserts:
        - The result is not empty.
        - The columns match the first sheet's columns.
    """
    df = file_reader.read_csv_or_excel(excel_test_paths["multi_sheet_excel"])
    assert not df.empty
    assert list(df.columns) == ["col1", "col2"]


def test_read_nonexistent_file(file_reader):
    """
    Test attempting to read a nonexistent file using FileReader.

    Asserts:
        - The result is None.
    """
    result = file_reader.read_csv_or_excel("nonexistent.csv")
    assert result is None


def test_read_invalid_file(file_reader, tmp_path):
    """
    Test attempting to read an invalid file using FileReader.

    Asserts:
        - The result is None.
    """
    invalid_path = tmp_path / "invalid.txt"
    invalid_path.write_text("not,a,valid,csv")

    result = file_reader.read_csv_or_excel(invalid_path)
    assert result is None


def test_read_sqlite_success(file_reader, tmp_path):
    """
    Test successful reading of a SQLite database table using FileReader.

    Asserts:
        - The data frame read from the database matches the expected content.
    """
    db_path = tmp_path / "test.db"
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE test_table (col1 INTEGER, col2 INTEGER);")
    cursor.execute(
        "INSERT INTO test_table (col1, col2) VALUES (1, 3), (2, 4);")
    connection.commit()
    connection.close()

    result = file_reader.read_sqlite(db_path)
    expected_df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    pd.testing.assert_frame_equal(result, expected_df)


def test_read_sqlite_no_table(file_reader, tmp_path):
    """
    Test reading an empty SQLite database with no tables using FileReader.

    Asserts:
        - The result is None.
    """
    db_path = tmp_path / "empty.db"
    sqlite3.connect(db_path).close()

    result = file_reader.read_sqlite(db_path)
    assert result is None


def test_read_sqlite_nonexistent_file(file_reader):
    """
    Test attempting to read a nonexistent SQLite database using FileReader.

    Asserts:
        - The result is None.
    """
    result = file_reader.read_sqlite("nonexistent.db")
    assert result is None

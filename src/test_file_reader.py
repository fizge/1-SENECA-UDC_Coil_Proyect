import os
import pytest
import pandas as pd
from file_reader import FileReader
import sqlite3

@pytest.fixture
def file_reader():
    return FileReader()

def test_read_csv_success(file_reader, tmp_path):
    csv_path = tmp_path / "test.csv"
    df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    df.to_csv(csv_path, index=False)

    result = file_reader.read_csv_or_excel(csv_path)
    pd.testing.assert_frame_equal(result, df)

def test_read_excel_success(file_reader, tmp_path):
    excel_path = tmp_path / "test.xlsx"
    df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    df.to_excel(excel_path, index=False)

    result = file_reader.read_csv_or_excel(excel_path)
    pd.testing.assert_frame_equal(result, df)

def test_read_nonexistent_file(file_reader):
    result = file_reader.read_csv_or_excel("nonexistent.csv")
    assert result is None

def test_read_invalid_file(file_reader, tmp_path):
    invalid_path = tmp_path / "invalid.txt"
    invalid_path.write_text("not,a,valid,csv")
    
    result = file_reader.read_csv_or_excel(invalid_path)
    assert result is None



def test_read_sqlite_success(file_reader, tmp_path):
    db_path = tmp_path / "test.db"
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE test_table (col1 INTEGER, col2 INTEGER);")
    cursor.execute("INSERT INTO test_table (col1, col2) VALUES (1, 3), (2, 4);")
    connection.commit()
    connection.close()

    result = file_reader.read_sqlite(db_path)
    expected_df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    pd.testing.assert_frame_equal(result, expected_df)

def test_read_sqlite_no_table(file_reader, tmp_path):
    db_path = tmp_path / "empty.db"
    sqlite3.connect(db_path).close()  # Create an empty database

    result = file_reader.read_sqlite(db_path)
    assert result is None

def test_read_sqlite_nonexistent_file(file_reader):
    result = file_reader.read_sqlite("nonexistent.db")
    assert result is None



### poner en el terminal pytest .
import pandas as pd
import sqlite3
import os

class FileReader:
    def __init__(self):
        pass

    def read_csv_or_excel(self, file_path):
        """
        Reads a CSV or Excel file and returns the data as a DataFrame.
        
        Args:
            file_path (str): Path to the file to be read.

        Returns:
            pd.DataFrame or None: DataFrame containing the data, or None if an error occurs.
        """
        try:
            file_path = str(file_path)
            if file_path.endswith(".csv"):
                data = pd.read_csv(file_path)
            else:
                data = pd.read_excel(file_path)
            return data
        except (FileNotFoundError, pd.errors.ParserError, pd.errors.EmptyDataError):
            return None
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return None

    def read_sqlite(self, db_path):
        """
        Reads data from the first table of a SQLite database and returns it as a DataFrame.
        
        Args:
            db_path (str): Path to the SQLite database.

        Returns:
            pd.DataFrame or None: DataFrame containing the data from the first table, or None if an error occurs.
        """
        try:
            if not os.path.exists(db_path):
                return None

            connection = sqlite3.connect(db_path)
            query = "SELECT name FROM sqlite_master WHERE type='table';"
            table_name = pd.read_sql_query(query, connection).iloc[0]['name']
            data = pd.read_sql_query(f"SELECT * FROM {table_name}", connection)
            return data
        except (FileNotFoundError, sqlite3.Error):
            return None
        except Exception as e:
            print(f"An error occurred while reading the SQLite database: {e}")
            return None





        

        
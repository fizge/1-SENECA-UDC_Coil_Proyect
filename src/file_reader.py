import pandas as pd
import sqlite3
import os

def read_csv_or_excel(file_path):
    try:
        if file_path.endswith(".csv"):
            data = pd.read_csv(file_path)
        else:
            data = pd.read_excel(file_path)
        print(data.head())
        return data
    except Exception as error:
        print(f"Error reading the file: {error}")
    except FileNotFoundError:
        print("File not found")
    except pd.errors.ParserError:
        print("Error parsing the file")
    except pd.errors.EmptyDataError:
        print("The file is empty")

def read_sqlite(db_path):
    try:
        if not os.path.exists(db_path):
            print("Database does not exist")
            return None

        connection = sqlite3.connect(db_path)
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        table_name = pd.read_sql_query(query, connection).iloc[0]['name']
        data = pd.read_sql_query(f"SELECT * FROM {table_name}", connection)
        print(data.head())
        return data
    except Exception as e:
        print(f"Unexpected error: {e}")
    except FileNotFoundError:
        print("File not found")
    except pd.errors.ParserError:
        print("Error parsing the file")
    except pd.errors.EmptyDataError:
        print("The file is empty")

def import_data(file_path):
    if file_path.endswith('.csv') or file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        return read_csv_or_excel(file_path)
    elif file_path.endswith('.sqlite') or file_path.endswith('.db'):
        return read_sqlite(file_path)
    else:
        print("File format not supported")


        

        

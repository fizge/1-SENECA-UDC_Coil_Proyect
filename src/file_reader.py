import pandas as pd
import sqlite3
import os

def read_csv_or_excel(file_path):
    try:
        if file_path.endswith(".csv"):
            data = pd.read_csv(file_path)
        else:
            data = pd.read_excel(file_path)
        return data
    except Exception as e:
        return None
    except FileNotFoundError:
        return None
    except pd.errors.ParserError:
        return None
    except pd.errors.EmptyDataError:
        return None

def read_sqlite(db_path):
    try:
        if not os.path.exists(db_path):
            return None

        connection = sqlite3.connect(db_path)
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        table_name = pd.read_sql_query(query, connection).iloc[0]['name']
        data = pd.read_sql_query(f"SELECT * FROM {table_name}", connection)
        return data
    except Exception as e:
        return None
    except FileNotFoundError:
        return None
    except pd.errors.ParserError:
        return None
    except pd.errors.EmptyDataError:
        return None

def import_data(file_path):
    if file_path.endswith('.csv') or file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        return read_csv_or_excel(file_path)
    elif file_path.endswith('.sqlite') or file_path.endswith('.db'):
        return read_sqlite(file_path)
    else:
        return None


        

        

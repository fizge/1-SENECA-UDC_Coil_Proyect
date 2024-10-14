import pandas as pd
import sqlite3
import os

def read_csv_or_excel(file_path):
    try:
        if file_path.endswith(".csv"):
            data = pd.read_csv(file_path)
        else:
            datos = pd.read_excel(ruta_archivo)
        print(datos.head())  
        return datos
    
    except Exception as error:
        print(f"Error al leer el archivo: {error}")
    except FileNotFoundError:
        print("Archivo no encontrado ")
    except pd.errors.ParserError:
        print("Error al analizar el archivo ")
    except pd.errors.EmptyDataError:
        print("El archivo está vacío ")

def read_sqlite(db_path):
    try:
        if not os.path.exists(ruta_bd):
            print("La base de datos no existe")
            return None

        conexion = sqlite3.connect(ruta_bd)
        consulta = "SELECT name FROM sqlite_master WHERE type='table';"
        nombre_tabla = pd.read_sql_query(consulta, conexion).iloc[0]['name']
        datos = pd.read_sql_query(f"SELECT * FROM {nombre_tabla}", conexion)
        print(datos.head()) 
        return datos
    
    except Exception as e:
        print(f"Error inesperado: {e}")
    except FileNotFoundError:
        print("Archivo no encontrado ")
    except pd.errors.ParserError:
        print("Error al analizar el archivo ")
    except pd.errors.EmptyDataError:
        print("El archivo está vacío ")
    
        
def importar_datos(ruta_archivo):
    if ruta_archivo.endswith('.csv') or ruta_archivo.endswith('.xlsx') or ruta_archivo.endswith('.xls'):
        return leer_csv_o_excel(ruta_archivo)
    elif ruta_archivo.endswith('.sqlite') or ruta_archivo.endswith('.db'):
        return leer_sqlite(ruta_archivo)
    else:
        print("Formato de archivo no soportado")

arch =input("Introduzca el archivo: ")
datos = importar_datos(arch)




        


        
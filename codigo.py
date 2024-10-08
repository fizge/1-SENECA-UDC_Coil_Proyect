import pandas as pd
import sqlite3
import os

def leer_csv_o_excel(ruta_archivo):
    """ Importa datos desde un archivo CSV o Excel. """
    try:
        if ruta_archivo.endswith(".csv"):
            datos = pd.read_csv(ruta_archivo)
        else:
            datos = pd.read_excel(ruta_archivo)
        print(datos.head())  # Muestra las primeras filas para confirmación
        return datos
    except Exception as error:
        print(f"Error al leer el archivo: {error}")

def leer_sqlite(ruta_bd):
    """ Importa datos desde una base de datos SQLite. """
    try:
        if not os.path.exists(ruta_bd):
            print("La base de datos no existe")
            return None

        conexion = sqlite3.connect(ruta_bd)
        consulta = "SELECT name FROM sqlite_master WHERE type='table';"
        nombre_tabla = pd.read_sql_query(consulta, conexion).iloc[0]['name']
        datos = pd.read_sql_query(f"SELECT * FROM {nombre_tabla}", conexion)
        print(datos.head())  # Muestra las primeras filas para confirmación
        return datos
    except Exception as error:
        print(f"Error al leer la base de datos: {error}")

def importar_datos(ruta_archivo):
    """ Determina el tipo de archivo y llama a la función de importación adecuada. """
    if ruta_archivo.endswith('.csv') or ruta_archivo.endswith('.xlsx') or ruta_archivo.endswith('.xls'):
        return leer_csv_o_excel(ruta_archivo)
    elif ruta_archivo.endswith('.sqlite') or ruta_archivo.endswith('.db'):
        return leer_sqlite(ruta_archivo)
    else:
        print("Formato de archivo no soportado")

# Ejemplo de uso:
if __name__ == "__main__":
    datos = importar_datos(r"C:\Users\Portatil\Desktop\2º CARRERA\ING. SOFT\INGENIERIA-SOFTWARE\1-SENECA-UDC_Coil_Proyect\housing.csv")
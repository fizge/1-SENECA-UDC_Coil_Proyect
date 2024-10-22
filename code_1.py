
import pandas as pd
import sqlite3
import os
from file_reader import import_data

def read(file_path):
    data = import_data(file_path)
    
    if data is None:
        return
    
    print("########## COLUMNAS CON VALORES NULOS ##########")
    print(data.isna().sum())
    
    # Ejecuta el menú de selección de opción
    data = menu(data)

    output_file = (
        file_path.replace(".xlsx", "_modificado.xlsx")
                 .replace(".csv", "_modificado.csv")
                 .replace(".db", "_modificado.db")
    )

    # Guardar el nuevo archivo según el tipo de archivo original
    if file_path.endswith(".xlsx"):
        data.to_excel(output_file, index=False)
    elif file_path.endswith(".csv"):
        data.to_csv(output_file, index=False)
    elif file_path.endswith(".db"):
        # Guardar en una nueva base de datos (o sobreescribir la existente)
        connection = sqlite3.connect(output_file)
        data.to_sql(name='modified_data', con=connection, if_exists='replace', index=False)
        connection.close()
        print(f"Los cambios se han guardado en la base de datos: {output_file}")
    else:
        print("Formato de archivo no soportado para guardar.")

    print(f"Los cambios se han guardado en: {output_file}")
    print("########## COLUMNAS CON VALORES NULOS DESPUÉS ##########")
    print(data.isna().sum())

def menu(data):
    while True:
        print("\nSelecciona la opción para el cambio:")
        print("1: Eliminar filas con valores nulos")
        print("2: Rellenar valores nulos con la mediana de la columna")
        print("3: Rellenar valores nulos con la media de la columna")
        print("4: Salir sin hacer cambios")
        
        selection = input("Escribe el número de la opción (1, 2, 3, o 4): ")

        # Opción 1: Eliminar filas con valores nulos
        if selection == "1":
            print(f"Filas con valores nulos antes de eliminarlas: {data.isna().sum().sum()}")  
            data = data.dropna()
            print(f"Filas con valores nulos eliminadas. Filas restantes: {data.isna().sum().sum()}")
            break

        # Opción 2: Rellenar valores nulos con la mediana
        elif selection == "2":
            column = input("¿En qué columna quieres rellenar con la mediana? ")
            if column in data.columns:
                data[column].fillna(data[column].median(), inplace=True)
                print(f"Valores nulos en la columna {column} rellenados con la mediana.")
            else:
                print("Columna no encontrada. Inténtalo de nuevo.")
            break

        # Opción 3: Rellenar valores nulos con la media
        elif selection == "3":
            column = input("¿En qué columna quieres rellenar con la media? ")
            if column in data.columns:
                data[column].fillna(data[column].mean(), inplace=True)
                print(f"Valores nulos en la columna {column} rellenados con la media.")
            else:
                print("Columna no encontrada. Inténtalo de nuevo.")
            break

        # Opción 4: Salir sin hacer cambios
        elif selection == "4":
            print("Saliendo sin hacer cambios.")
            break

        else:
            print("Selección no válida. Inténtalo de nuevo.")
    
    return data

print(read("/Users/sagez/Library/CloudStorage/OneDrive-UniversidadedaCoruña/2IA/ES/TRABAJO_SENECA/sprint3/housing.db"))

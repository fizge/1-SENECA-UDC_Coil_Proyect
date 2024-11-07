
import pickle
from sklearn.linear_model import LinearRegression
import numpy as np

# CREAR Y ENTRENAR EL MODELO
def crear_modelo():
    # Datos de prueba
    X = np.array([[1, 1], [2, 2], [3, 3], [4, 4]])
    y = np.dot(X, np.array([1, 2])) + 3
    # Crear y entrenar el modelo
    model = LinearRegression().fit(X, y)
    return model

# GUARDAR EL MODELO CON PICKLE
def guardar_modelo(model, file_name='model_pickle.pkl'):
    with open(file_name, 'wb') as file:
        pickle.dump(model, file)

# CARGAR EL MODELO GUARDADO CON PICKLE
def cargar_modelo(file_name='model_pickle.pkl'):
    with open(file_name, 'rb') as file:
        model = pickle.load(file)
    return model

# PROBAR EL MODELO CARGADO
def probar_modelo(model):
    X_test = np.array([[5, 5]])
    prediccion = model.predict(X_test)
    print(f"Predicción con el modelo cargado: {prediccion}")

def main():
    modelo = crear_modelo()
    guardar_modelo(modelo)  # Guardamos el modelo
    modelo_cargado = cargar_modelo()  # Cargamos el modelo
    probar_modelo(modelo_cargado)  # Probamos el modelo cargado



if __name__ == "_main_":
    main()
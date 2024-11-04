
import joblib
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

# GUARDAR EL MODELO CON JOBLIB
def guardar_modelo(model, file_name='model_joblib.pkl'):
    joblib.dump(model, file_name)

# CARGAR EL MODELO GUARDADO CON JOBLIB
def cargar_modelo(file_name='model_joblib.pkl'):
    model = joblib.load(file_name)
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

if _name_ == "_main_":
    main()
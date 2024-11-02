import pandas as pd 
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from file_reader import import_data



def head(path):
    data = pd.read_excel(path)
    return data.head()

def describe(data):
    return data.describe()

def plot_describe(data):
    data.drop(['housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'median_house_value'], axis=1).hist()
    plt.show()

def main():
    data = import_data("/Users/sagez/Library/CloudStorage/OneDrive-UniversidadedaCoruña/2IA/ES/TRABAJO_SENECA/sprint3/housing_modificado.db")
    
    # Seleccionar múltiples variables independientes (predictoras)
    X = data[['total_bedrooms', 'total_rooms', 'population']]  # Variables independientes
    y = data['median_house_value']  # Variable dependiente

    # Crear el objeto de Regresión Lineal
    regr = linear_model.LinearRegression()
    
    # Entrenar el modelo
    regr.fit(X, y)
    
    # Hacer predicciones
    y_pred = regr.predict(X)

    # Coeficientes y errores
    print('Coeficientes: \n', regr.coef_)  # Coeficientes de cada variable independiente
    print('Término independiente: \n', regr.intercept_)  # Intercepto
    print("Error cuadrático medio: %.2f" % mean_squared_error(y, y_pred))

    # Visualización 1: Predicciones vs. valores reales
    plt.figure(figsize=(10, 6))
    plt.scatter(y, y_pred, color='blue')  # Gráfico de dispersión de valores reales vs predicciones
    plt.plot([y.min(), y.max()], [y.min(), y.max()], color='red', lw=2)  # Línea de referencia de una predicción perfecta
    plt.title('Predicciones vs Valores reales')
    plt.xlabel('Valores Reales (median_house_value)')
    plt.ylabel('Predicciones (median_house_value)')
    plt.grid(True)
    plt.show()

    # Visualización 2: Gráficos individuales para cada variable independiente
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))  # Subplots para tres gráficos
    axs[0].scatter(X['total_bedrooms'], y, color='blue')
    axs[0].set_title('total_bedrooms vs median_house_value')
    axs[0].set_xlabel('total_bedrooms')
    axs[0].set_ylabel('median_house_value')

    axs[1].scatter(X['total_rooms'], y, color='green')
    axs[1].set_title('total_rooms vs median_house_value')
    axs[1].set_xlabel('total_rooms')
    axs[1].set_ylabel('median_house_value')

    axs[2].scatter(X['population'], y, color='purple')
    axs[2].set_title('population vs median_house_value')
    axs[2].set_xlabel('population')
    axs[2].set_ylabel('median_house_value')

    plt.tight_layout()
    plt.show()

    # Ejemplo de predicción para una casa con valores específicos en las variables independientes
    num_habitaciones = 3
    num_total_rooms = 5
    poblacion = 1200
    prediccion = regr.predict([[num_habitaciones, num_total_rooms, poblacion]])
    print(f"El valor medio de la vivienda para una casa con {num_habitaciones} habitaciones, {num_total_rooms} total de cuartos, y población de {poblacion} es: {prediccion[0]:.2f} unidades monetarias")

main()

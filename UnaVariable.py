#https://www.aprendemachinelearning.com/regresion-lineal-en-espanol-con-python/
#https://docs.hektorprofe.net/academia/python/poo-para-interfaces-graficas/



import pandas as pd 
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from file_reader import import_data
# regresión simple con una variable con numero de habitaciones y coste de la casa . El nº de habitaciones puedes afectar al coste de la casa

def head(path):
    data = pd.read_excel(path) # Las primeras filas de los datos para hacernos una idea 
    return data.head()

def describe(data):
    return describe(data) # algunas medidas estadísticas comunes como la media etc.

def plot_describe(data):
    # Visualizamos rápidamente las caraterísticas de entrada
    data.drop(['housing_median_age','total_rooms','total_bedrooms','population','edian_house_value'],1).hist()
    plt.show()
    
  
def main():
    data = import_data("/Users/sagez/Library/CloudStorage/OneDrive-UniversidadedaCoruña/2IA/ES/TRABAJO_SENECA/sprint3/prueba_modificado.xlsx")
    
    # Seleccionar características
    X = data[['total_bedrooms']]  # Variable independiente
    y = data['median_house_value']  # Variable dependiente

    # Creamos el objeto de Regresión Lineal
    regr = linear_model.LinearRegression()
    
    # Entrenamos nuestro modelo
    regr.fit(X, y)
    
    # Hacemos las predicciones
    y_pred = regr.predict(X)

    # Coeficientes y errores
    print('Coefficients: \n', regr.coef_) # ES LA m , y significa que por cada habitacion se espere que se aumente m unidades monetarias
    print('Independent term: \n', regr.intercept_) # es la b
    print("Mean squared error: %.2f" % mean_squared_error(y, y_pred))
    

    """
    ECUACION DE LA RECTA : y = mX + b
    """

    #Vamos a comprobar:
    # Ejemplo de predicción para una casa con 3 habitaciones el precio que debe tener 
    num_habitaciones = 3
    prediccion = regr.predict([[num_habitaciones]])
    print(f"El valor medio de la vivienda para {num_habitaciones} habitaciones es: {prediccion[0]:.2f} unidades monetarias")


    # Visualización
    # plt.figure(figsize=(12, 6))
    # plt.scatter(X, y, color='blue', label='Datos reales')  # Puntos de datos reales
    # plt.plot(X, y_pred, color='red', linewidth=2, label='Línea de regresión')  # Línea de regresión
    # plt.title('Regresión Lineal: Valor Medio de la Vivienda vs. Número de Habitaciones')
    # plt.xlabel('Número de Habitaciones (total_bedrooms)')
    # plt.ylabel('Valor Medio de la Vivienda (median_house_value)')
    # plt.legend()
    # plt.grid(True)
    # plt.show()

main()
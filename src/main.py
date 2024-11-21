
from initial_scenario import LinearRegressionAnalyitics
#DOCUMENTAR FUNCIONES Y CLASES, MANTENER VALORES DE SELECTION DESPUES DE REINICIO
# CHECK A FILL OPTIONS

if __name__ == "__main__":
    app = LinearRegressionAnalyitics()
    app.create_window()
    app.gui_presentation()
    app.v.mainloop()

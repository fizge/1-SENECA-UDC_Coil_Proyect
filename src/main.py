
from initial_scenario import LinearRegressionAnalyitics
#DOCUMENTAR FUNCIONES Y CLASES, MANTENER VALORES DE SELECTION DESPUES DE REINICIO,MOVER PREDICTIONS ABAJO DETODO
#MOVER SAVE MODEL DEBAJO DE INFO, PONER TITULO ATODO,CHECK A FILL OPTIONS, MODIFICAR PREDICTION

if __name__ == "__main__":
    app = LinearRegressionAnalyitics()
    app.create_window()
    app.gui_presentation()
    app.v.mainloop()

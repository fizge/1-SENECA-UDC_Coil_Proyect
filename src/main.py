
from scenarios.initial_scenario import LinearRegressionAnalyitics
# DOCUMENTAR FUNCIONES Y CLASES Y HACER RELEASE

if __name__ == "__main__":
    app = LinearRegressionAnalyitics()
    app.create_window()
    app.gui_presentation()
    app.v.mainloop()

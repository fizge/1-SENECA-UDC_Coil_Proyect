
from gui import DataViewerApp
#MOVER A GUI TODOS FRAMES Y BOTONES, ARREGLAR REAJUSTE OPEN FILES Y MOVER AL MEDIO AL PRINCIPIO

if __name__ == "__main__":
    app = DataViewerApp()
    app.create_window()
    app.create_button()
    app.v.mainloop()

from GUI import DataViewerApp
# METER LA GRAFICA EN LA MISMA VENTANA, GUARDAR LA TABLA ORIGINAL PARA CAMBIAR LOS FILL, CAMBIAR COLOR FILL SELECCIONADOS
if __name__ == "__main__":
    app = DataViewerApp()
    app.create_window()
    app.create_button()
    app.v.mainloop()

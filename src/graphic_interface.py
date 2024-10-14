import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QTreeWidget, QTreeWidgetItem
from file_reader import read_csv_or_excel, read_sqlite

#Probé la librería PyQt y encontré que ofrece una amplia gama de funcionalidades gráficas avanzadas, ideal para proyectos grandes o que requieren interfaces personalizadas. Su principal ventaja es la flexibilidad y la capacidad de crear interfaces complejas, aunque su curva de aprendizaje puede ser más empinada, especialmente para principiantes. PyQt es multiplataforma y funciona bien en Windows, macOS y Linux, lo que la hace muy versátil. Sin embargo, la documentación, aunque extensa, puede ser algo técnica para quienes recién empiezan, lo que puede ralentizar el proceso de aprendizaje.

class FileReaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    # Función para crear la ventana
    def initUI(self):
        self.setWindowTitle('Mostrar datos')
        self.setGeometry(100, 100, 700, 600)

        layout = QVBoxLayout()

        # Crear etiqueta
        self.label = QLabel('Selecciona un archivo', self)
        layout.addWidget(self.label)

        # Crear botón para abrir archivo
        btn = QPushButton('Abrir archivo', self)
        btn.clicked.connect(self.abrir_archivos)
        layout.addWidget(btn)

        # Crear TreeView para mostrar datos
        self.tree = QTreeWidget()
        self.tree.setColumnCount(5)  # Asumimos que los datos tendrán hasta 5 columnas (ajustable según archivo)
        self.tree.setHeaderLabels(['Columna 1', 'Columna 2', 'Columna 3', 'Columna 4', 'Columna 5'])
        layout.addWidget(self.tree)

        self.setLayout(layout)

    # Función para abrir archivos
    def abrir_archivos(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Abrir archivo', '', 
                        'Archivos CSV (*.csv);;Archivos Excel (*.xlsx;*.xls);;Archivos SQLite (*.sqlite;*.db)')
        if file_path:
            self.importar_datos(file_path)

    # Función para importar datos
    def importar_datos(self, file_path):
        if file_path.endswith(('.csv', '.xlsx', '.xls')):
            data = leer_csv_o_excel(file_path)
        elif file_path.endswith(('.sqlite', '.db')):
            data = leer_sqlite(file_path)
        
        if data is not None:
            self.mostrar_datos_en_treeview(data)
        else:
            self.limpiar_label()
            self.label.setText("No se pudo leer el archivo")

    # Función para mostrar los datos en un TreeView
    def mostrar_datos_en_treeview(self, data):
        self.tree.clear()  # Limpiar TreeView
        self.tree.setColumnCount(len(data.columns))
        self.tree.setHeaderLabels(data.columns)

        for index, row in data.iterrows():
            items = [str(row[col]) for col in data.columns]
            tree_item = QTreeWidgetItem(items)
            self.tree.addTopLevelItem(tree_item)

    # Función para limpiar la etiqueta
    def limpiar_label(self):
        self.label.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    reader = FileReaderApp()
    reader.show()
    sys.exit(app.exec_())

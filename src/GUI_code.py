
import wx
import wx.grid as gridlib
import file_reader as fr  # Asegúrate de tener tu módulo file_reader

class FileLoaderApp(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(1000, 150))
        self.file_path = None
        self.init_ui()

    def init_ui(self):
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(240, 248, 255))  # Fondo azul claro

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # Campo de texto para mostrar la ruta del archivo
        self.path_display = wx.TextCtrl(panel, style=wx.TE_READONLY)
        self.path_display.SetBackgroundColour(wx.Colour(255, 255, 240))  # Fondo beige claro
        self.path_display.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        hbox.Add(self.path_display, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        # Botón para abrir el explorador de archivos
        open_button = wx.Button(panel, label='Cargar Archivo')
        open_button.SetBackgroundColour(wx.Colour(100, 149, 237))  # Azul medio
        open_button.SetForegroundColour(wx.Colour(255, 255, 255))  # Texto blanco
        open_button.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        open_button.Bind(wx.EVT_BUTTON, self.on_open_file)
        hbox.Add(open_button, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=10)

        vbox.Add(hbox, flag=wx.EXPAND)

        # Botón para mostrar los datos, oculto inicialmente
        self.show_button = wx.Button(panel, label='Mostrar Datos')
        self.show_button.SetBackgroundColour(wx.Colour(72, 209, 204))  # Turquesa medio
        self.show_button.SetForegroundColour(wx.Colour(255, 255, 255))  # Texto blanco
        self.show_button.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.show_button.Bind(wx.EVT_BUTTON, self.on_show_data)
        self.show_button.Disable()  # Deshabilitado hasta que se cargue un archivo
        vbox.Add(self.show_button, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        panel.SetSizer(vbox)
        self.Show()

    def on_open_file(self, event):
        """Abre un diálogo para seleccionar el archivo (csv, xlsx, db)."""
        with wx.FileDialog(self, "Abrir archivo",
                           wildcard="Supported files (*.csv;*.xlsx;*.db)|*.csv;*.xlsx;*.db",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # El usuario canceló la operación

            self.file_path = fileDialog.GetPath()
            self.path_display.SetValue(self.file_path)
            self.show_button.Enable()  # Habilita el botón "Mostrar Datos"

    def on_show_data(self, event):
        """Muestra los datos en una tabla si hay un archivo cargado."""
        if self.file_path:
            data = fr.import_data(self.file_path)  # Usa el módulo file_reader para importar datos
            if data is not None and not data.empty:
                self.show_data_frame(data)
            else:
                wx.MessageBox('No hay datos para mostrar', 'Info', wx.OK | wx.ICON_INFORMATION)

    def show_data_frame(self, data):
        """Muestra los datos en una nueva ventana."""
        frame = wx.Frame(None, title='Datos Cargados', size=(1000, 1000))
        frame.SetBackgroundColour(wx.Colour(230, 230, 250))  # Fondo lavanda claro
        panel = wx.Panel(frame)
        grid = gridlib.Grid(panel)
        grid.CreateGrid(len(data), len(data.columns))

        # Decorar la tabla
        grid.SetLabelBackgroundColour(wx.Colour(72, 61, 139))  # Azul oscuro para encabezado
        grid.SetLabelTextColour(wx.WHITE)  # Texto blanco para encabezado
        grid.SetDefaultCellBackgroundColour(wx.Colour(245, 245, 245))  # Fondo gris claro para celdas
        grid.SetDefaultCellTextColour(wx.Colour(47, 79, 79))  # Texto gris oscuro para celdas
        grid.SetDefaultCellFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        for col_idx, col_name in enumerate(data.columns):
            grid.SetColLabelValue(col_idx, col_name)
            for row_idx, value in enumerate(data[col_name]):
                grid.SetCellValue(row_idx, col_idx, str(value))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid, 1, wx.EXPAND)
        panel.SetSizer(sizer)
        frame.Show()

if __name__ == '__main__':
    app = wx.App(False)
    FileLoaderApp(None, title='Cargador de Archivos')
    app.MainLoop()

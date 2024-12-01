import pandas as pd
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, ttk, filedialog
from file_reader import FileReader
from charging_bar import ChargingWindow


class Preselection:
    def __init__(self, app):
        self.app = app
        self.loaded_data = None
        self.deleted_rows = None
        self.tree = None
        self.tree_frame = None
        self.selection_frame = None
        self.option_frame = None
        self.input_select = None
        self.output_select = None
        self.selected_input_column = None
        self.selected_output_column = None
        self.output_label = None
        self.input_label = None
        self.input_columns = []
        self.output_columns = []
        self.confirm_button = None
        self.preprocess_label = None
        self.option_menu = None
        self.generate_button = None
        self.original_data = None
        self.file_reader = FileReader()

    def import_data(self, file_path):

        self.deleted_rows = None
        if file_path.endswith(('.csv', '.xlsx', '.xls')):
            self.loaded_data = self.file_reader.read_csv_or_excel(file_path)
        elif file_path.endswith(('.sqlite', '.db')):
            self.loaded_data = self.file_reader.read_sqlite(file_path)

        if self.loaded_data is not None:
            self.original_data = self.loaded_data.copy()
            self.display_data_in_treeview(self.loaded_data)
        if self.app.modeling.graphic_frame is not None:
            self.app.modeling.graphic_frame.destroy()
            self.app.modeling.graphic_frame = None
            self.app.v.grid_columnconfigure(0, weight=1, uniform="column")
            self.app.v.grid_columnconfigure(1, weight=0, uniform="column2")
        if self.option_frame is not None:
            self.option_frame.grid_forget()
        if self.app.load.info_frame is not None:
            self.app.load.info_frame.destroy()
        self.selected_input_column, self.selected_output_column = None, None
        self.app.v.geometry("1000x450+200+0")

    def open_files(self):
        file = filedialog.askopenfilename(
            title="Open",
            filetypes=[("Supported Files", "*.csv *.xlsx *.xls *.sqlite *.db")]
        )
        if file:

            charging = ChargingWindow(self.app)
            charging.bar()

            self.import_data(file)
            self.app.file_path_entry.configure(state="normal")
            self.app.file_path_entry.delete(0, tk.END)
            self.app.file_path_entry.insert(0, file)
            self.app.file_path_entry.configure(state="readonly")

            charging.close_bar()

    def display_data_in_treeview(self, data):

        if self.tree is None:
            self.tree_frame = ctk.CTkFrame(self.app.v)
            self.tree_frame.grid(row=3, column=0,
                                 padx=10, pady=(10,0), sticky="nsew")
            self.tree = ttk.Treeview(self.tree_frame)
            self.tree.grid(row=0, column=0, sticky="nsew")
            scrollbar_x = ttk.Scrollbar(
                self.tree_frame, orient="horizontal", command=self.tree.xview)
            self.tree.configure(xscrollcommand=scrollbar_x.set)
            scrollbar_x.grid(row=1, column=0, sticky="ew")
            self.app.v.grid_rowconfigure(5, weight=1)

        self.tree.delete(*self.tree.get_children())
        self.tree['columns'] = list(data.columns)
        self.tree['show'] = 'headings'

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", background="#2B2B2B",
                        foreground="white", font=("Arial", 10, 'bold'))

        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=190, stretch=False)

        self.tree.tag_configure(
            'oddrow', background='#333333', foreground='white')
        self.tree.tag_configure(
            'evenrow', background='#2B2B2B', foreground='white')

        for i, (_, row) in enumerate(data.iterrows()):
            if i % 2 == 0:
                self.tree.insert("", "end", values=list(row),
                                 tags=('evenrow',))
            else:
                self.tree.insert("", "end", values=list(row), tags=('oddrow',))

        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)

        self.gui_preselection(data.columns)

    def gui_preselection(self, columns):
        self.input_columns = list(columns)
        self.output_columns = list(columns)

        if self.selection_frame is not None:
            self.selection_frame.grid_forget()
        if self.selection_frame is None:
            self.selection_frame = ctk.CTkFrame(self.app.v,fg_color='#242424')

        if self.option_frame is None:
            self.option_frame = ctk.CTkFrame(self.app.v,fg_color='#242424')

      
        self.selection_frame.grid(
            row=5, column=0,pady=0, padx=(0,10), sticky="new")

        self.input_label = ctk.CTkLabel(
            self.selection_frame, text="Select Input:", font=("Arial", 14, 'bold'))
        self.input_label.grid(row=0, column=0,  padx=(
            100, 20), pady=(40,10), sticky="e")

        self.input_select = ctk.CTkOptionMenu(
            self.selection_frame, width=230,corner_radius=30, values=self.input_columns, command=self.update_output_options)
        self.input_select.grid(row=0, column=1, padx=10, pady=(40,10), sticky="ew")

        self.output_label = ctk.CTkLabel(
            self.selection_frame, text="Select Output:", font=("Arial", 14, 'bold'))
        self.output_label.grid(row=1, column=0, padx=(
            100, 20), pady=10, sticky="e")

        self.output_select = ctk.CTkOptionMenu(
            self.selection_frame, width=230,corner_radius=30, values=self.output_columns, command=self.update_input_options)
        self.output_select.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.confirm_button = ctk.CTkButton(self.selection_frame, text="Confirm Selections", font=(
            "Arial", 14, "bold"), width=100, height=40,corner_radius=100, command=self.confirm_selections)
        if self.app.modeling.graphic_frame is None:   
            self.confirm_button.grid(row=0, column=3, rowspan=2,
                            padx=50, pady=(40,10), sticky="ew")

        self.preprocess_label = ctk.CTkLabel(
            self.option_frame, text="Preprocessing Options:", font=("Arial", 15, 'bold'))

        options = [
            "Remove rows with NaN", 
            "Fill with Mean", 
            "Fill with Median", 
            "Fill with Constant Value"
        ]

        # Crear una variable para almacenar la opción seleccionada
        self.selected_option = ctk.StringVar(value='Choose one fill option')

        # Crear el OptionMenu
        self.option_menu = ctk.CTkOptionMenu(
            self.option_frame, 
            variable=self.selected_option, 
            values=options, 
            width=250,
            height=40,
            corner_radius=30,
            font=("Arial", 14, 'bold'), 
            command=self.apply_preprocessing
        )
        

        self.generate_button = ctk.CTkButton(self.option_frame,corner_radius=40, text="Generate model", font=(
           "Arial", 20, "bold"), height=50, width=40, command=self.regression_model)

        if self.input_columns and self.output_columns:
            if self.selected_input_column is not None and self.selected_output_column is not None:
                self.input_select.set(self.selected_input_column)
                self.output_select.set(self.selected_output_column)
            else:
                self.input_select.set(self.input_columns[0])
                if len(self.output_columns) > 1:
                    self.output_select.set(self.output_columns[1])
                else:
                    self.output_select.set(self.output_columns[0])

    def update_output_options(self, selected_input):
        if selected_input:
            self.output_columns = [
                col for col in self.original_data.columns if col != selected_input]
            self.output_select.configure(values=self.output_columns)
            if self.output_select.get() == selected_input:
                self.output_select.set(self.output_columns[0])

    def update_input_options(self, selected_output):
        if selected_output:
            self.input_columns = [
                col for col in self.original_data.columns if col != selected_output]
            self.input_select.configure(values=self.input_columns)
            if self.input_select.get() == selected_output:
                self.input_select.set(self.input_columns[0])

    def confirm_selections(self):
        self.selected_input_column = self.input_select.get()
        self.selected_output_column = self.output_select.get()

        messagebox.showinfo(
            "Selections Confirmed", f"Input Column: {self.selected_input_column}\nOutput Column: {self.selected_output_column}")
        if self.app.modeling.graphic_frame is None:
            self.app.v.geometry("1000x610+200+0")

            self.option_frame.grid(row=7, column=0, pady=(
                10, 10), padx=10, sticky="new")

        self.preprocess_label.grid(
            row=0, column=0, padx=100,pady=(0,10), sticky="w")
        self.option_menu.grid(
            row=1, column=0, padx=100,pady=(0,30), sticky="w")
        self.generate_button.grid(
            row=0, column=0,rowspan=2, padx=510,pady=30, sticky="nw")

        self.loaded_data = self.original_data
        self.display_data_in_treeview(self.loaded_data)

    def apply_preprocessing(self, option):
        columns_to_process = [self.selected_input_column,
                              self.selected_output_column]

        if option == "Remove rows with NaN":
            self.loaded_data = self.original_data.copy()
            self.loaded_data.dropna(subset=columns_to_process, inplace=True)
            self.deleted_rows = pd.concat(
                [self.original_data.copy(), self.loaded_data]).drop_duplicates(keep=False)
            if self.deleted_rows.empty:
                messagebox.showinfo("No Rows Deleted", "No rows were deleted.")
            else:
                messagebox.showinfo(
                    "Success", "Rows with NaN have been deleted.")
            self.display_data_in_treeview(self.loaded_data)

        elif option in ["Fill with Mean", "Fill with Median", "Fill with Constant Value"]:
            self.fill_na_values(option, columns_to_process)

    def fill_na_values(self, method, columns):
        self.loaded_data = self.original_data.copy()
     
        columns_with_nan = [
            col for col in columns if self.loaded_data[col].isna().any()]

        if not columns_with_nan:
            messagebox.showinfo(
                "No NaN", "No columns with NaN values found in the selected Input and Output.")
            return

        if method == "Fill with Constant Value":

            top = ctk.CTkToplevel(self.app.v)
            top.title("Fill NaN Values")
            top.lift()
            top.grab_set()
            top.geometry(
                f"+{self.app.v.winfo_x() + 250}+{self.app.v.winfo_y() + 250}")

            ctk.CTkLabel(top, text="Enter constant values for the selected columns with NaN:").pack(
                pady=10, padx=20)

            entries = {}
            for column in columns_with_nan:
                ctk.CTkLabel(top, text=f"{column}:").pack(pady=5)
                entry = ctk.CTkEntry(top)
                entry.pack(pady=5)
                entries[column] = entry

            def apply_values():
                try:
                   
                    for column in columns_with_nan:
                        entry = entries[column]
                        if entry.get():
                            constant_value = float(entry.get())
                            self.loaded_data[column] = self.original_data[column].fillna(
                                constant_value)
                            messagebox.showinfo(
                                "Success", f"NaN values in '{column}' filled with: {constant_value}")
                    top.grab_release()
                    top.destroy()
                    self.display_data_in_treeview(self.loaded_data)
                except ValueError:
                    messagebox.showerror(
                        "Error", f"Invalid numeric value for '{column}'.")
                    return

            ctk.CTkButton(top, text="Apply",
                          command=apply_values).pack(pady=10)
            top.protocol("WM_DELETE_WINDOW", lambda: (
                top.grab_release(), top.destroy()))

        else:
            # Llenar con media o mediana
            for column in columns_with_nan:
                if method == "Fill with Mean":
                    value = round(self.original_data[column].mean(), 5)
                    self.loaded_data[column] = self.original_data[column].fillna(
                        value)
                    messagebox.showinfo(
                        "Success", f"NaN values in '{column}' filled with mean: {value:.5f}")
                elif method == "Fill with Median":
                    value = round(self.original_data[column].median(), 5)
                    self.loaded_data[column] = self.original_data[column].fillna(
                        value)
                    messagebox.showinfo(
                        "Success", f"NaN values in '{column}' filled with median: {value:.5f}")
            self.display_data_in_treeview(self.loaded_data)


    def regression_model(self):
        self.app.modeling.generate_model()
        if self.app.modeling.graphic_frame is not None:
            
            self.app.v.geometry("1500x830+0+0")
            self.app.v.grid_columnconfigure(0, weight=2, uniform="column")
            self.app.v.grid_columnconfigure(2, weight=2, uniform="column")

            separator = tk.Frame(self.app.v, width=2, bg='gray')
            separator.grid(row=0, column=1, rowspan=8, padx=(20,0),pady=60, sticky="ns")

            self.app.initial_frame.grid(
                row=2, column=0, pady=10, padx=10, sticky="nsew")
            self.tree_frame.grid(row=3, column=0,
                                padx=10, pady=10, sticky="nsew")
            self.selection_frame.grid(
                row=5, column=0, pady=10, padx=10, sticky="new")
            self.option_frame.grid(row=7, column=0, pady=(10, 60), padx=10, sticky="new")

                
            

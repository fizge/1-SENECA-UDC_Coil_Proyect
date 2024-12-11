import pandas as pd
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, ttk, filedialog
from logical.file_reader import FileReader
from utils.charging_bar import ChargingWindow


class Preselection:
    """
    A class to manage the preselection phase of data for linear regression modeling.

    This class provides functionality for:
    - Importing datasets (CSV, Excel, SQLite) and displaying them in a treeview.
    - Allowing users to select input and output columns for regression modeling.
    - Preprocessing data, including handling NaN values.
    - Initiating the linear regression model generation process.

    Attributes:
        app: Reference to the main application instance.
        loaded_data: The dataset currently loaded into the application.
        original_data: A copy of the original dataset for reference.
        deleted_rows: Rows deleted during preprocessing.
        tree: Treeview widget to display dataset.
        tree_frame: Frame containing the treeview.
        selection_frame: Frame for column selection UI.
        option_frame: Frame for preprocessing and model generation options.
        input_select: Dropdown for selecting input columns.
        output_select: Dropdown for selecting output columns.
        selected_input_column: The currently selected input column.
        selected_output_column: The currently selected output column.
        output_label: Label for the output column dropdown.
        input_label: Label for the input column dropdown.
        input_columns: List of potential input columns.
        output_columns: List of potential output columns.
        confirm_button: Button to confirm column selections.
        preprocess_label: Label for preprocessing options.
        option_menu: Dropdown for selecting preprocessing actions.
        generate_button: Button to generate the regression model.
        separator: Visual separator in the UI.
        file_reader: Instance of the `FileReader` class to read datasets.
    """

    def __init__(self, app):
        """
        Initializes the `Preselection` class.

        :param app: Reference to the main application instance.
        """
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
        self.separator = None
        self.original_data = None
        self.file_reader = FileReader()

    def import_data(self, file_path):
        """
        Imports a dataset from the specified file path.

        Supports files in CSV, Excel, and SQLite formats. Resets the UI and 
        loads the dataset into the treeview.

        :param file_path: The file path of the dataset to import.
        """
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
            self.app.v.grid_columnconfigure(2, weight=0, uniform="column3")
        if self.option_frame is not None:
            self.option_frame.grid_forget()
        if self.app.load.info_frame is not None:
            self.app.load.info_frame.destroy()
        if self.separator is not None:
            self.separator.grid_forget()
        self.selected_input_column, self.selected_output_column = None, None
        self.app.v.geometry("1000x450+200+0")

    def open_files(self):
        """
        Opens a file dialog for selecting a dataset to import.

        Displays a loading bar during the import process and updates the file
        path entry with the selected file path.
        """
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
        """
        Displays the loaded dataset in a treeview widget.

        Configures the treeview to show column headers and populates it with
        alternating row colors for better readability.

        :param data: The dataset to display.
        """
        if self.tree is None:
            self.tree_frame = ctk.CTkFrame(self.app.v)
            self.tree_frame.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="nsew")
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
        """
        Creates and configures the UI for selecting input and output columns.

        Also sets up preprocessing options and the button to generate the model.

        :param columns: Columns available in the dataset.
        """
        self.input_columns = list(columns)
        self.output_columns = list(columns)

        if self.selection_frame is not None:
            self.selection_frame.grid_forget()
        if self.selection_frame is None:
            self.selection_frame = ctk.CTkFrame(self.app.v, fg_color='#242424')

        if self.option_frame is None:
            self.option_frame = ctk.CTkFrame(self.app.v, fg_color='#242424')

        self.selection_frame.grid(row=5, column=0, pady=0, padx=(0, 10), sticky="new")

        self.input_label = ctk.CTkLabel(
            self.selection_frame, text="Select Input:", font=("Arial", 14, 'bold'))
        self.input_label.grid(row=0, column=0, padx=(100, 20), pady=(40, 10), sticky="e")

        self.input_select = ctk.CTkOptionMenu(
            self.selection_frame, width=230, corner_radius=30, values=self.input_columns, command=self.update_output_options)
        self.input_select.grid(row=0, column=1, padx=10, pady=(40, 10), sticky="ew")

        self.output_label = ctk.CTkLabel(
            self.selection_frame, text="Select Output:", font=("Arial", 14, 'bold'))
        self.output_label.grid(row=1, column=0, padx=(100, 20), pady=10, sticky="e")

        self.output_select = ctk.CTkOptionMenu(
            self.selection_frame, width=230, corner_radius=30, values=self.output_columns, command=self.update_input_options)
        self.output_select.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.confirm_button = ctk.CTkButton(self.selection_frame, text="Confirm Selections", font=(
            "Arial", 14, "bold"), width=100, height=40, corner_radius=100, command=self.confirm_selections)
        self.confirm_button.grid(row=0, column=3, rowspan=2,
                                 padx=50, pady=(0, 30), sticky="sw")

        self.preprocess_label = ctk.CTkLabel(
            self.option_frame, text="Preprocessing Options:", font=("Arial", 15, 'bold'))

        options = [
            "Remove rows with NaN",
            "Fill with Mean",
            "Fill with Median",
            "Fill with Constant Value"
        ]

        self.selected_option = ctk.StringVar(value='Choose one fill option')
        self.option_menu = ctk.CTkOptionMenu(
            self.option_frame, variable=self.selected_option, values=options,
            width=250, height=40, corner_radius=30, font=("Arial", 14, 'bold'),
            command=self.apply_preprocessing)

        self.generate_button = ctk.CTkButton(self.option_frame, corner_radius=40, text="Generate model", font=(
            "Arial", 20, "bold"), height=60, width=40, command=self.regression_model)

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
        """
        Updates the output column dropdown when a new input column is selected.

        :param selected_input: The selected input column.
        """
        if selected_input:
            self.output_columns = [
                col for col in self.original_data.columns if col != selected_input]
            self.output_select.configure(values=self.output_columns)
            if self.output_select.get() == selected_input:
                self.output_select.set(self.output_columns[0])

    def update_input_options(self, selected_output):
        """
        Updates the input column dropdown when a new output column is selected.

        :param selected_output: The selected output column.
        """
        if selected_output:
            self.input_columns = [
                col for col in self.original_data.columns if col != selected_output]
            self.input_select.configure(values=self.input_columns)
            if self.input_select.get() == selected_output:
                self.input_select.set(self.input_columns[0])

    def confirm_selections(self):
        """
        Confirms the selected input and output columns for regression modeling.

        Validates the selections and updates the UI for preprocessing and modeling.
        """
        self.selected_input_column = self.input_select.get()
        self.selected_output_column = self.output_select.get()

        if self.selected_input_column not in self.input_columns or self.selected_output_column not in self.output_columns or self.selected_input_column is None or self.selected_output_column is None:
            messagebox.showerror("Error", "Column/s is not in data")
            return

        messagebox.showinfo(
            "Selections Confirmed", f"Input Column: {self.selected_input_column}\nOutput Column: {self.selected_output_column}")
        if self.app.modeling.graphic_frame is None:
            self.app.v.geometry("1000x610+200+0")
            self.option_frame.grid(row=6, column=0, pady=(10, 20), padx=10, sticky="new")

        self.preprocess_label.grid(row=0, column=0, padx=100, pady=(0, 10), sticky="w")
        self.option_menu.grid(row=1, column=0, padx=100, pady=(0, 30), sticky="w")
        self.generate_button.grid(row=0, column=0, rowspan=2, padx=490, pady=(0, 30), sticky="sw")

        self.loaded_data = self.original_data
        self.display_data_in_treeview(self.loaded_data)

    def apply_preprocessing(self, option):
        """
        Applies the selected preprocessing option to the dataset.

        Options include:
        - Removing rows with NaN values.
        - Filling NaN values with the mean, median, or a constant value.

        :param option: The selected preprocessing option.
        """
        columns_to_process = [self.selected_input_column, self.selected_output_column]

        if not pd.api.types.is_numeric_dtype(self.loaded_data[self.selected_input_column]) or not pd.api.types.is_numeric_dtype(self.loaded_data[self.selected_output_column]):
            messagebox.showerror("Error", "The selected input or output column contains non-numeric data. Please select numeric columns.")
            return

        if option == "Remove rows with NaN":
            self.loaded_data = self.original_data.copy()
            self.loaded_data.dropna(subset=columns_to_process, inplace=True)
            self.deleted_rows = pd.concat(
                [self.original_data.copy(), self.loaded_data]).drop_duplicates(keep=False)
            if self.deleted_rows.empty:
                messagebox.showinfo("No Rows Deleted", "No rows were deleted.")
            else:
                messagebox.showinfo("Success", "Rows with NaN have been deleted.")
            self.display_data_in_treeview(self.loaded_data)

        elif option in ["Fill with Mean", "Fill with Median", "Fill with Constant Value"]:
            self.fill_na_values(option, columns_to_process)

    def fill_na_values(self, method, columns):
        """
        Fills NaN values in the dataset using the specified method.

        Methods include:
        - Filling with the mean or median of the column.
        - Filling with a constant value provided by the user.

        :param method: The method to use for filling NaN values.
        :param columns: The columns to process.
        """
        self.loaded_data = self.original_data.copy()
        columns_with_nan = [col for col in columns if self.loaded_data[col].isna().any()]

        if not columns_with_nan:
            messagebox.showinfo(
                "No NaN", "No columns with NaN values found in the selected Input and Output.")
            return

        if method == "Fill with Constant Value":
            top = ctk.CTkToplevel(self.app.v)
            top.title("Fill NaN Values")
            top.lift()
            top.grab_set()
            top.geometry(f"+{self.app.v.winfo_x() + 250}+{self.app.v.winfo_y() + 250}")

            ctk.CTkLabel(top, text="Enter constant values for the selected columns with NaN:").pack(pady=10, padx=20)

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
                            self.loaded_data[column] = self.original_data[column].fillna(constant_value)
                            messagebox.showinfo(
                                "Success", f"NaN values in '{column}' filled with: {constant_value}")
                    top.grab_release()
                    top.destroy()
                    self.display_data_in_treeview(self.loaded_data)
                except ValueError:
                    messagebox.showerror(
                        "Error", f"Invalid numeric value for '{column}'.")
                    return

            ctk.CTkButton(top, text="Apply", command=apply_values).pack(pady=10)
            top.protocol("WM_DELETE_WINDOW", lambda: (top.grab_release(), top.destroy()))

        else:
            for column in columns_with_nan:
                if method == "Fill with Mean":
                    value = round(self.original_data[column].mean(), 5)
                    self.loaded_data[column] = self.original_data[column].fillna(value)
                    messagebox.showinfo(
                        "Success", f"NaN values in '{column}' filled with mean: {value:.5f}")
                elif method == "Fill with Median":
                    value = round(self.original_data[column].median(), 5)
                    self.loaded_data[column] = self.original_data[column].fillna(value)
                    messagebox.showinfo(
                        "Success", f"NaN values in '{column}' filled with median: {value:.5f}")
            self.display_data_in_treeview(self.loaded_data)

    def regression_model(self):
        """
        Initiates the regression model generation process.

        Updates the UI to display the generated model and other relevant elements.
        """
        self.app.modeling.generate_model()

        if self.app.modeling.graphic_frame is not None:
            self.app.v.geometry("1500x830+0+0")
            self.app.v.grid_columnconfigure(0, weight=2, uniform="column")
            self.app.v.grid_columnconfigure(2, weight=2, uniform="column")

            self.separator = tk.Frame(self.app.v, width=2, bg='gray')
            self.separator.grid(row=0, column=1, rowspan=8, padx=(20, 0), pady=60, sticky="ns")

            self.app.initial_frame.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")
            self.tree_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
            self.selection_frame.grid(row=5, column=0, pady=10, padx=10, sticky="new")
            self.option_frame.grid(row=6, column=0, pady=(10, 120), padx=10, sticky="nsew")

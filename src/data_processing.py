import pandas as pd
import tkinter as tk
from tkinter import messagebox,ttk,filedialog
from file_reader import FileReader
import customtkinter as ctk

class DataProcessing:
    def __init__(self, app):
        self.app = app
        self.tree_frame = None
        self.preprocess_label = None
        self.fill_nan_button = None
        self.fill_mean_button = None
        self.fill_meadian_button = None
        self.fill_constant_button = None
        self.generate_button = None
        self.option_frame = None
        self.file_reader = FileReader()
        self.input_columns = []
        self.output_columns = []
        self.original_data = None

    def import_data(self, file_path):
        self.app.deleted_rows = None
        if file_path.endswith(('.csv', '.xlsx', '.xls')):
            self.app.loaded_data = self.file_reader.read_csv_or_excel(file_path)
        elif file_path.endswith(('.sqlite', '.db')):
            self.app.loaded_data = self.file_reader.read_sqlite(file_path)

        if self.app.loaded_data is not None:
            if self.original_data is None:
                self.original_data = self.app.loaded_data.copy()
            
            self.display_data_in_treeview(self.app.loaded_data)
            if self.app.modeling.graphic_frame is not None:
                  self.app.modeling.graphic_frame.grid_forget()
                  self.app.v.grid_columnconfigure(0, weight=1, uniform="column")
                  self.app.v.grid_columnconfigure(1, weight=0, uniform="column2")
            if self.option_frame is not None:
                  self.option_frame.grid_forget()
            self.app.v.geometry("1000x450+0+0")
        '''
        self.app.deleted_rows = None
        if file_path.endswith(('.csv', '.xlsx', '.xls')):
            self.app.loaded_data = self.file_reader.read_csv_or_excel(file_path)
        elif file_path.endswith(('.sqlite', '.db')):
            self.app.loaded_data = self.file_reader.read_sqlite(file_path)

        if self.app.loaded_data is not None:
            if self.original_data is None:
                self.original_data = self.app.loaded_data.copy()
            
            self.display_data_in_treeview(self.app.loaded_data)
            self.app.v.geometry("1000x450+200+0")
        '''

    def open_files(self):    
        file = filedialog.askopenfilename(
            title="Open",
            filetypes=[("Supported Files", "*.csv *.xlsx *.xls *.sqlite *.db")]
        )
        if file:
            self.import_data(file)
            self.app.file_path_entry.configure(state="normal")
            self.app.file_path_entry.delete(0, tk.END)
            self.app.file_path_entry.insert(0, file)
            self.app.file_path_entry.configure(state="readonly")

    def display_data_in_treeview(self, data):
        if self.app.tree is None:
            self.tree_frame = ctk.CTkFrame(self.app.v)
            self.tree_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
            self.app.tree = ttk.Treeview(self.tree_frame)
            self.app.tree.grid(row=0, column=0, sticky="nsew")
            scrollbar_x = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.app.tree.xview)
            self.app.tree.configure(xscrollcommand=scrollbar_x.set)
            scrollbar_x.grid(row=1, column=0, sticky="ew")
            self.app.v.grid_rowconfigure(5, weight=1)

        self.app.tree.delete(*self.app.tree.get_children())
        self.app.tree['columns'] = list(data.columns)
        self.app.tree['show'] = 'headings'

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", background="#2B2B2B", foreground="white", font=("Arial", 10, 'bold'))

        for col in self.app.tree['columns']:
            self.app.tree.heading(col, text=col)
            self.app.tree.column(col, width=190, stretch=False)

        self.app.tree.tag_configure('oddrow', background='#333333', foreground='white')
        self.app.tree.tag_configure('evenrow', background='#2B2B2B', foreground='white')

        for i, (_, row) in enumerate(data.iterrows()):
            if i % 2 == 0:
                self.app.tree.insert("", "end", values=list(row), tags=('evenrow',))
            else:
                self.app.tree.insert("", "end", values=list(row), tags=('oddrow',))

        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)
      
        self.options_selection(data.columns)

    def options_selection(self, columns):
        self.input_columns = list(columns)
        self.output_columns = list(columns)

        if self.app.selection_frame is not None:
            self.app.selection_frame.grid_forget()

        if self.option_frame is None:
            self.option_frame = ctk.CTkFrame(self.app.v)

        self.app.selection_frame = ctk.CTkFrame(self.app.v)
        if self.app.modeling.graphic_frame is None:
            self.app.selection_frame.grid(row=5, column=0, columnspan=3, pady=10, padx=10, sticky="ew")
        else:
            self.app.selection_frame.grid(row=5, column=0, columnspan=1, pady=10, padx=10, sticky="ew")

        self.preprocess_label = ctk.CTkLabel(self.option_frame, text="Preprocessing Options:", font=("Arial", 15, 'bold'))

        self.remove_nan_button = ctk.CTkButton(self.option_frame, text="Remove rows with NaN", font=("Arial", 12, "bold"), width=160, height=40, command=lambda: self.apply_preprocessing("Remove rows with NaN"))
        self.fill_mean_button = ctk.CTkButton(self.option_frame, text="Fill with Mean", font=("Arial", 12, "bold"), width=160, height=40, command=lambda: self.apply_preprocessing("Fill with Mean"))
        self.fill_median_button = ctk.CTkButton(self.option_frame, text="Fill with Median", font=("Arial", 12, "bold"), width=160, height=40, command=lambda: self.apply_preprocessing("Fill with Median"))
        self.fill_constant_button = ctk.CTkButton(self.option_frame, text="Fill with Constant Value", font=("Arial", 12, "bold"), width=160, height=40, command=lambda: self.apply_preprocessing("Fill with Constant Value"))

        input_label = ctk.CTkLabel(self.app.selection_frame, text="Select Input:", font=("Arial", 12, 'bold'))
        input_label.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        self.app.input_select = ctk.CTkOptionMenu(self.app.selection_frame, values=self.input_columns, command=self.update_output_options)
        self.app.input_select.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

        output_label = ctk.CTkLabel(self.app.selection_frame, text="Select Output:", font=("Arial", 12, 'bold'))
        output_label.grid(row=1, column=2, padx=10, pady=10, sticky="e")

        self.app.output_select = ctk.CTkOptionMenu(self.app.selection_frame, values=self.output_columns, command=self.update_input_options)
        self.app.output_select.grid(row=1, column=3, padx=10, pady=10, sticky="ew")

        confirm_button = ctk.CTkButton(self.app.selection_frame, text="Confirm Selections", font=("Arial", 12, "bold"), width=50, height=40, command=self.confirm_selections)
        confirm_button.grid(row=0, column=4, rowspan=2, padx=(20, 10), pady=10, sticky="ew")

        self.generate_button = ctk.CTkButton(self.option_frame, text="Generate model", font=("Arial", 12, "bold"), height=50, width=40, command=self.regression_model)

        if self.input_columns and self.output_columns:
            self.app.input_select.set(self.input_columns[0])
            if len(self.output_columns) > 1:
                self.app.output_select.set(self.output_columns[1])
            else:
                self.app.output_select.set(self.output_columns[0])

    def update_output_options(self, selected_input):
        if selected_input:
            self.output_columns = [col for col in self.original_data.columns if col != selected_input]
            self.app.output_select.configure(values=self.output_columns)
            if self.app.output_select.get() == selected_input:
                self.app.output_select.set("")

    def update_input_options(self, selected_output):
        if selected_output:
            self.input_columns = [col for col in self.original_data.columns if col != selected_output]
            self.app.input_select.configure(values=self.input_columns)
            if self.app.input_select.get() == selected_output:
                self.app.input_select.set("")

    def confirm_selections(self):
        self.app.selected_input_column = self.app.input_select.get()
        self.app.selected_output_column = self.app.output_select.get()

        messagebox.showinfo("Selections Confirmed", f"Input Column: {self.app.selected_input_column}\nOutput Column: {self.app.selected_output_column}")

        if self.app.modeling.graphic_frame is None:
            self.app.v.geometry("1000x680+200+0")
            self.option_frame.grid_columnconfigure(0, weight=1, uniform="column")
            self.option_frame.grid_columnconfigure(1, weight=1, uniform="column")
            self.option_frame.grid_columnconfigure(2, weight=1, uniform="column")
            self.option_frame.grid_columnconfigure(3, weight=1, uniform="column")
            self.option_frame.grid(row=6, column=0, columnspan=2, pady=(10, 10), padx=10, sticky="ew")
            self.preprocess_label.grid(row=2, column=0, columnspan=4, padx=100, pady=10, sticky="nsew")
            self.remove_nan_button.grid(row=3, column=0, padx=(30, 0), pady=10, sticky="ew")
            self.fill_mean_button.grid(row=3, column=1, padx=(20, 0), pady=10, sticky="ew")
            self.fill_median_button.grid(row=3, column=2, padx=(20, 0), pady=10, sticky="ew")
            self.fill_constant_button.grid(row=3, column=3, padx=(20, 30), pady=10, sticky="ew")
            self.generate_button.grid(row=4, column=1, columnspan=2, rowspan=2, padx=70, pady=(20, 20), sticky="nsew")
        self.app.loaded_data = self.original_data    
        self.display_data_in_treeview(self.app.loaded_data)

    def apply_preprocessing(self, option):
        columns_to_process = [self.app.selected_input_column, self.app.selected_output_column]

        if option == "Remove rows with NaN":
            self.app.loaded_data = self.original_data.copy()
            self.app.loaded_data.dropna(subset=columns_to_process, inplace=True)
            self.app.deleted_rows = pd.concat([self.original_data.copy(), self.app.loaded_data]).drop_duplicates(keep=False)
            if self.app.deleted_rows.empty:
                messagebox.showinfo("No Rows Deleted", "No rows were deleted.")
            else:
                messagebox.showinfo("Success", "Rows with NaN have been deleted.")
            self.display_data_in_treeview(self.app.loaded_data)

            self.fill_mean_button.configure(fg_color="#1465B1")
            self.fill_median_button.configure(fg_color="#1465B1")
            self.fill_constant_button.configure(fg_color="#1465B1")
            self.remove_nan_button.configure(fg_color="green")

        elif option in ["Fill with Mean", "Fill with Median", "Fill with Constant Value"]:
            self.fill_na_values(option, columns_to_process)

        if self.app.modeling.graphic_frame is None:
            self.app.v.geometry("1000x750+200+0")

    def fill_na_values(self, method, columns):
        self.app.loaded_data = self.original_data.copy()
        columns_with_nan = [col for col in columns if self.original_data.copy()[col].isna().any()]

        if not columns_with_nan:
            messagebox.showinfo("No NaN", "No columns with NaN values found in the selected Input and Output.")
            return

        if method == "Fill with Constant Value":
            top = ctk.CTkToplevel(self.app.v)
            top.title("Fill NaN Values")
            top.lift()
            top.grab_set()
            top.geometry(f"+{self.app.v.winfo_x() + 200}+{self.app.v.winfo_y() + 200}")

            ctk.CTkLabel(top, text="Enter constant values for the selected columns with NaN:").pack(pady=10)

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
                            self.app.loaded_data[column] = self.original_data.copy()[column].fillna(constant_value)
                            messagebox.showinfo("Success", f"NaN values in '{column}' filled with: {constant_value}")
                except ValueError:
                        messagebox.showerror("Error", f"Invalid numeric value for '{column}'.")
                        return

                top.grab_release()
                top.destroy()
                self.display_data_in_treeview(self.app.loaded_data)

                self.fill_median_button.configure(fg_color="#1465B1")
                self.fill_mean_button.configure(fg_color="#1465B1")
                self.remove_nan_button.configure(fg_color="#1465B1")
                self.fill_constant_button.configure(fg_color="green")
                self.app.v.update_idletasks()

            ctk.CTkButton(top, text="Apply", command=apply_values).pack(pady=10)
            top.protocol("WM_DELETE_WINDOW", lambda: (top.grab_release(), top.destroy()))

        else:
            for column in columns_with_nan:
                if method == "Fill with Mean":
                    value = round(self.original_data.copy()[column].mean(), 5)
                    self.app.loaded_data[column] = self.original_data.copy()[column].fillna(value)
                    messagebox.showinfo("Success", f"NaN values in '{column}' filled with mean: {value:.5f}")

                    self.display_data_in_treeview(self.app.loaded_data)

                    self.fill_constant_button.configure(fg_color="#1465B1")
                    self.fill_median_button.configure(fg_color="#1465B1")
                    self.remove_nan_button.configure(fg_color="#1465B1")
                    self.fill_mean_button.configure(fg_color="green")

                elif method == "Fill with Median":
                    value = round(self.original_data.copy()[column].median(), 5)
                    self.app.loaded_data[column] = self.original_data.copy()[column].fillna(value)
                    messagebox.showinfo("Success", f"NaN values in '{column}' filled with median: {value:.5f}")

                    self.display_data_in_treeview(self.app.loaded_data)
                    
                    self.fill_constant_button.configure(fg_color="#1465B1")
                    self.fill_mean_button.configure(fg_color="#1465B1")
                    self.remove_nan_button.configure(fg_color="#1465B1")
                    self.fill_median_button.configure(fg_color="green")

        if self.app.modeling.graphic_frame is None:
            self.app.v.geometry("1000x750+0+0")

    def regression_model(self):
        self.app.modeling.generate_model()
        if self.app.modeling.graphic_frame is not None:
            self.app.v.geometry("1500x680+0+0")
            self.app.v.grid_columnconfigure(0, weight=2, uniform="column")
            self.app.v.grid_columnconfigure(1, weight=2, uniform="column")

            self.app.button_frame.grid(row=2, column=0, columnspan=1, pady=10, padx=10, sticky="nsew")
            self.tree_frame.grid(row=3, column=0, columnspan=1, padx=10, pady=10, sticky="nsew")
            self.app.selection_frame.grid(row=5, column=0, columnspan=1, pady=10, padx=10, sticky="ew")
            self.option_frame.grid(row=6, column=0, columnspan=1, pady=(10, 20), padx=10, sticky="ew")
            self.preprocess_label.grid(row=2, column=0, columnspan=4, padx=100, pady=10, sticky="nsew")
            
            self.remove_nan_button.configure(font=("Arial", 11, "bold"))
            self.fill_mean_button.configure(font=("Arial", 11, "bold"))
            self.fill_median_button.configure(font=("Arial", 11, "bold"))
            self.fill_constant_button.configure(font=("Arial", 11, "bold"))
            self.generate_button.configure(font=("Arial", 24, "bold"), height=70, width=150)

            self.remove_nan_button.grid(row=3, column=0, padx=(15, 0), pady=10, sticky="ew")
            self.fill_mean_button.grid(row=3, column=1, padx=(15, 0), pady=10, sticky="ew")
            self.fill_median_button.grid(row=3, column=2, padx=(15, 0), pady=10, sticky="ew")
            self.fill_constant_button.grid(row=3, column=3, padx=(15, 15), pady=10, sticky="ew")
            self.generate_button.grid(row=4, column=1, columnspan=2, rowspan=2, padx=70, pady=(20, 20), sticky="nsew")

import pandas as pd
from tkinter import messagebox, ttk
from file_reader import FileReader  # Importar la clase FileReader
import customtkinter as ctk

class DataProcessing:
    def __init__(self, app):
        self.app = app
        self.tree_frame = None  
        self.file_reader = FileReader()  # Instanciar FileReader

    def import_data(self, file_path):
        self.app.deleted_rows = None  
        if self.app.show_deleted_button:
            self.app.show_deleted_button.grid_forget()
        
        # Usar FileReader para cargar datos según la extensión del archivo
        if file_path.endswith(('.csv', '.xlsx', '.xls')):
            self.app.loaded_data = self.file_reader.read_csv_or_excel(file_path)
        elif file_path.endswith(('.sqlite', '.db')):
            self.app.loaded_data = self.file_reader.read_sqlite(file_path)
        
        if self.app.loaded_data is not None:
            self.display_data_in_treeview(self.app.loaded_data)

   
    def display_data_in_treeview(self, data):
        # Use self.tree_frame instead of a local variable
        if self.app.tree is None:
            self.tree_frame = ctk.CTkFrame(self.app.v)  # Assign to self.tree_frame
            self.tree_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
            
            self.app.tree = ttk.Treeview(self.tree_frame)  # Use self.app.tree
            self.app.tree.grid(row=0, column=0, sticky="nsew")
            
            scrollbar_x = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.app.tree.xview)
            self.app.tree.configure(xscrollcommand=scrollbar_x.set)
            scrollbar_x.grid(row=1, column=0, sticky="ew")
            
            self.app.v.grid_rowconfigure(5, weight=1)
        
        self.app.tree.delete(*self.app.tree.get_children())  
        self.app.tree['columns'] = list(data.columns)
        self.app.tree['show'] = 'headings'
        
        for col in self.app.tree['columns']:
            self.app.tree.heading(col, text=col)
        
        for _, row in data.iterrows():
            self.app.tree.insert("", "end", values=list(row))

        self.tree_frame.grid_rowconfigure(0, weight=1)  
        self.tree_frame.grid_columnconfigure(0, weight=1)
        
        # Llamar a options_selection después de actualizar el Treeview
        self.options_selection(data.columns)

    def options_selection(self, columns):
        if self.app.selection_frame is not None:
            self.app.selection_frame.grid_forget()
        
        self.app.selection_frame = ctk.CTkFrame(self.app.v)
        self.app.selection_frame.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        self.app.v.geometry("1000x580")

        preprocess_label = ctk.CTkLabel(self.app.selection_frame, text="Preprocessing Options:", font=("Arial", 15, 'bold'))
        preprocess_label.grid(row=0, column=2, padx=(80, 10), pady=10, sticky="e")

        options = ["Remove rows with NaN", "Fill with Mean", "Fill with Median", 
                   "Fill with Constant Value", "Show rows with NaN"]

        preprocess_var = ctk.StringVar(value=options[0])
        preprocess_menu = ctk.CTkOptionMenu(self.app.selection_frame, variable=preprocess_var, values=options)
        preprocess_menu.grid(row=0, column=3, padx=(2, 5), pady=10, sticky="ew")

        apply_button = ctk.CTkButton(self.app.selection_frame, text="Apply Preprocessing", font=("Arial", 14, "bold"),  width=160, height=40,
                                      command=lambda: self.apply_preprocessing(preprocess_var.get()))
        apply_button.grid(row=0, column=4, padx=(5, 5), pady=10, sticky="ew")


        input_label = ctk.CTkLabel(self.app.selection_frame, text="Select Input:", font=("Arial", 14, 'bold'))
        input_label.grid(row=1, column=4, padx=10, pady=10, sticky="e")
        
        self.app.input_select = ctk.CTkOptionMenu(self.app.selection_frame, values=list(columns))
        self.app.input_select.grid(row=1, column=5, padx=10, pady=10, sticky="ew")

        output_label = ctk.CTkLabel(self.app.selection_frame, text="Select Output:", font=("Arial", 14, 'bold'))
        output_label.grid(row=2, column=4, padx=10, pady=10, sticky="e")
        
        self.app.output_select = ctk.CTkOptionMenu(self.app.selection_frame, values=list(columns))
        self.app.output_select.grid(row=2, column=5, padx=10, pady=10, sticky="ew")

        generate_button = ctk.CTkButton(self.app.selection_frame, text="Generate model", font=("Arial", 24, "bold"), width=290, height=80, command=self.generate_model)
        generate_button.grid(row=1, column=0, columnspan=3, rowspan=2, padx=(40, 140), pady=10, sticky="ew")
        
        confirm_button = ctk.CTkButton(self.app.selection_frame, text="Confirm Selections", font=("Arial", 15, "bold"), width=70, height=80, command=self.confirm_selections)
        confirm_button.grid(row=1, column=6, rowspan=2, padx=(20, 10), pady=10, sticky="ew")

    def confirm_selections(self):
        self.app.selected_input_column = self.app.input_select.get()
        self.app.selected_output_column = self.app.output_select.get()
        
        if not self.app.selected_input_column or not self.app.selected_output_column:
            messagebox.showerror("Error", "Please select both Input and Output columns.")
            return

        messagebox.showinfo("Selections Confirmed", f"Input Column: {self.app.selected_input_column}\nOutput Column: {self.app.selected_output_column}")

    def generate_model(self):
        if not self.app.selected_input_column or not self.app.selected_output_column:
            messagebox.showerror("Error", "You must confirm Input and Output selections before generating the model.")
            return

        messagebox.showinfo("Model Generation", f"Model generated with Input: {self.app.selected_input_column} and Output: {self.app.selected_output_column}")

    def apply_preprocessing(self, option):
        if self.app.loaded_data is None:
            messagebox.showerror("Error", "Please load a file first.")
            return

        if not self.app.selected_input_column or not self.app.selected_output_column:
            messagebox.showerror("Error", "Please confirm Input and Output selections first.")
            return

        if self.app.selected_input_column not in self.app.loaded_data.columns or self.app.selected_output_column not in self.app.loaded_data.columns:
            messagebox.showerror("Error", "One or more selected columns no longer exist in the dataset.")
            return
        
        columns_to_process = [self.app.selected_input_column, self.app.selected_output_column]
        
        if option == "Remove rows with NaN":
            df_original = self.app.loaded_data.copy()  
            self.app.loaded_data.dropna(subset=columns_to_process, inplace=True)
            self.app.deleted_rows = pd.concat([df_original, self.app.loaded_data]).drop_duplicates(keep=False)
            if self.app.deleted_rows.empty:
                messagebox.showinfo("No Rows Deleted", "No rows were deleted.")
            else:
                messagebox.showinfo("Success", "Rows with NaN have been deleted.")
                if not self.app.show_deleted_button:
                    self.app.show_deleted_button = ctk.CTkButton(self.app.v, text="Show Deleted Rows", command=lambda: self.show_deleted_rows(self.app.deleted_rows))
                self.app.show_deleted_button.grid(row=6, column=0, columnspan=2, pady=10)

        elif option in ["Fill with Mean", "Fill with Median", "Fill with Constant Value"]:
            self.fill_na_values(option, columns_to_process)

        elif option == "Show rows with NaN":
            self.show_nan_rows(self.app.loaded_data[columns_to_process])

        self.display_data_in_treeview(self.app.loaded_data)

    def fill_na_values(self, method, columns):
        columns_with_nan = [col for col in columns if self.app.loaded_data[col].isna().any()]

        if not columns_with_nan:
            messagebox.showinfo("No NaN", "No columns with NaN values found in the selected Input and Output.")
            return

        if method == "Fill with Constant Value":
            top = ctk.CTkToplevel(self.app.v)
            top.title("Fill NaN Values")
            top.lift()

            ctk.CTkLabel(top, text="Enter constant values for the selected columns with NaN:").pack(pady=10)

            entries = {}
            
            for column in columns_with_nan:
                ctk.CTkLabel(top, text=f"{column}:").pack(pady=5)
                entry = ctk.CTkEntry(top)
                entry.pack(pady=5)
                entries[column] = entry

            def apply_values():
                for column in columns_with_nan:
                    entry = entries[column]
                    if entry.get():  
                        try:
                            constant_value = float(entry.get())
                            self.app.loaded_data[column] = self.app.loaded_data[column].fillna(constant_value)
                            messagebox.showinfo("Success", f"NaN values in '{column}' filled with: {constant_value}")
                        except ValueError:
                            messagebox.showerror("Error", f"Invalid numeric value for '{column}'.")
                            return

                top.destroy()
                self.display_data_in_treeview(self.app.loaded_data)

            ctk.CTkButton(top, text="Apply", command=apply_values).pack(pady=10)
            top.protocol("WM_DELETE_WINDOW", top.destroy)
        else:
            for column in columns_with_nan:
                if method == "Fill with Mean":
                    value = self.app.loaded_data[column].mean()
                    self.app.loaded_data[column] = self.app.loaded_data[column].fillna(value)
                    messagebox.showinfo("Success", f"NaN values in '{column}' filled with mean: {value:.2f}")
                elif method == "Fill with Median":
                    value = self.app.loaded_data[column].median()
                    self.app.loaded_data[column] = self.app.loaded_data[column].fillna(value)
                    messagebox.showinfo("Success", f"NaN values in '{column}' filled with median: {value:.2f}")

        self.display_data_in_treeview(self.app.loaded_data)

    def show_nan_rows(self, df):
        nan_rows = df[df.isna().any(axis=1)]
        if nan_rows.empty:
            messagebox.showinfo("No Rows with NaN", "There are no rows with missing values.")
        else:
            self.show_data_in_window(nan_rows, "Rows with NaN")

    def show_deleted_rows(self, df_deleted):
        if df_deleted.empty:
            messagebox.showinfo("No Deleted Rows", "No rows were deleted.")
        else:
            self.show_data_in_window(df_deleted, "Deleted Rows")

    def show_data_in_window(self, df, title):
        top = ctk.CTkToplevel(self.app.v)
        top.title(title)
        treeview = ttk.Treeview(top)
        treeview.pack(fill="both", expand=True)
        
        treeview["columns"] = list(df.columns)
        treeview["show"] = 'headings'
        
        for col in treeview["columns"]:
            treeview.heading(col, text=col)
        
        for _, row in df.iterrows():
            treeview.insert("", "end", values=list(row))

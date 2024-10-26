
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import customtkinter as ctk
import pandas as pd
from file_reader import read_csv_or_excel, read_sqlite

class DataViewerApp:
    def __init__(self):
        self.v = None
        self.tree = None
        self.loaded_data = None
        self.deleted_rows = None
        self.show_deleted_button = None
        self.input_select = None
        self.output_select = None
        self.selection_frame = None
        self.selected_input_column = None
        self.selected_output_column = None
        self.original_window_size = None
        self.file_path_entry = None

        self.create_window()
        self.create_label()
        self.create_button()

    def create_window(self):
        ctk.set_appearance_mode("pink")
        ctk.set_default_color_theme("blue")
        
        self.v = ctk.CTk()
        self.v.title("Data Viewer")
        self.original_window_size = "1000x500"
        self.v.geometry(self.original_window_size)
        
        self.v.grid_rowconfigure(0, weight=1)
        self.v.grid_columnconfigure(0, weight=1)

    def open_files(self):
        file = filedialog.askopenfilename(
                title="Open",
                filetypes=(("CSV Files", "*.csv"),
                           ("Excel Files", "*.xlsx"),
                           ("Excel Files", "*.xls"),
                           ("SQLite Files", "*.sqlite"),
                           ("DB Files", "*.db"))
        )
        if file:
            self.import_data(file)
            self.file_path_entry.configure(state="normal")
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, file)
            self.file_path_entry.configure(state="readonly")

    def clear_table(self):
        if self.tree is None:
            return

        self.tree.delete(*self.tree.get_children())
        if self.selection_frame is not None:
            self.selection_frame.grid_forget()
            self.input_select = None
            self.output_select = None
            self.v.geometry(self.original_window_size)

        self.file_path_entry.configure(state="normal")
        self.file_path_entry.delete(0, tk.END)
        self.file_path_entry.insert(0, "No file selected")
        self.file_path_entry.configure(state="readonly")

    def create_button(self):
        button_frame = ctk.CTkFrame(self.v)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        open_button = ctk.CTkButton(button_frame, text="Open File", font=("Arial", 15, "bold"), width=140, height=40, command=self.open_files)
        clear_button = ctk.CTkButton(button_frame, text="Clear", font=("Arial", 15, "bold"), width=140, height=40, command=self.clear_table)

        open_button.grid(row=0, column=0, padx=(40, 5), pady=5, sticky="ew")
        clear_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.file_path_entry = ctk.CTkEntry(button_frame, width=400, font=("Arial", 12))
        self.file_path_entry.grid(row=1, column=0, columnspan=2, padx=40, pady=10, sticky="ew")
        self.file_path_entry.insert(0, "No file selected")
        self.file_path_entry.configure(state="readonly")

        preprocess_label = ctk.CTkLabel(button_frame, text="Preprocessing Options:", font=("Arial", 15, 'bold'))
        preprocess_label.grid(row=0, column=2, padx=(80, 10), pady=10, sticky="e")

        options = ["Remove rows with NaN", "Fill with Mean", "Fill with Median", 
                   "Fill with Constant Value", "Show rows with NaN"]

        preprocess_var = ctk.StringVar(value=options[0])
        preprocess_menu = ctk.CTkOptionMenu(button_frame, variable=preprocess_var, values=options)
        preprocess_menu.grid(row=0, column=3, padx=(2, 5), pady=10, sticky="ew")

        apply_button = ctk.CTkButton(button_frame, text="Apply Preprocessing", font=("Arial", 14, "bold"), width=160, height=40, command=lambda: self.apply_preprocessing(preprocess_var.get()))
        apply_button.grid(row=1, column=3, padx=(5, 5), pady=10, sticky="ew")

    def create_label(self):
        label_title = ctk.CTkLabel(self.v, text="LINEAR REGRESSION ANALYTICS", font=("Arial", 45, "bold"))
        label_title.grid(row=0, column=0, columnspan=2, pady=20, sticky="ew")

    def import_data(self, file_path):
        self.deleted_rows = None
        if self.show_deleted_button:
            self.show_deleted_button.grid_forget()

        if file_path.endswith(('.csv', '.xlsx', '.xls')):
            self.loaded_data = read_csv_or_excel(file_path)
        elif file_path.endswith(('.sqlite', '.db')):
            self.loaded_data = read_sqlite(file_path)

        if self.loaded_data is not None:
            self.detect_nan(self.loaded_data)
            self.display_data_in_treeview(self.loaded_data)

    def detect_nan(self, data):
        nan_info = data.isna().sum()
        nan_cols = nan_info[nan_info > 0]
        if not nan_cols.empty:
            messagebox.showinfo("Missing Values", f"NaN detected in: \n{nan_cols}")
        else:
            messagebox.showinfo("No Missing Values", "There are no missing values in the data.")

    def display_data_in_treeview(self, data):
        if self.tree is None:
            tree_frame = ctk.CTkFrame(self.v)
            tree_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

            self.tree = ttk.Treeview(tree_frame, show="headings", columns=list(data.columns), height=15)
            self.tree.grid(row=0, column=0, sticky="nsew")

            scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
            self.tree.configure(xscrollcommand=scrollbar_x.set)
            scrollbar_x.grid(row=1, column=0, sticky="ew")

            scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
            self.tree.configure(yscrollcommand=scrollbar_y.set)
            scrollbar_y.grid(row=0, column=1, sticky="ns")

            self.v.grid_rowconfigure(5, weight=1)

        self.tree.delete(*self.tree.get_children())
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        for _, row in data.iterrows():
            self.tree.insert("", "end", values=list(row))

        self.add_input_output_buttons(data.columns)

    def add_input_output_buttons(self, columns):
        if self.selection_frame is not None:
            self.selection_frame.grid_forget()

        self.selection_frame = ctk.CTkFrame(self.v)
        self.selection_frame.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        self.v.geometry("1000x700")

        input_label = ctk.CTkLabel(self.selection_frame, text="Select Input:", font=("Arial", 14, 'bold'))
        input_label.grid(row=0, column=4, padx=10, pady=10, sticky="e")

        self.input_select = ctk.CTkOptionMenu(self.selection_frame, values=list(columns))
        self.input_select.grid(row=0, column=5, padx=10, pady=10, sticky="ew")

        output_label = ctk.CTkLabel(self.selection_frame, text="Select Output:", font=("Arial", 14, 'bold'))
        output_label.grid(row=1, column=4, padx=10, pady=10, sticky="e")

        self.output_select = ctk.CTkOptionMenu(self.selection_frame, values=list(columns))
        self.output_select.grid(row=1, column=5, padx=10, pady=10, sticky="ew")

        generate_button = ctk.CTkButton(self.selection_frame, text="Generate model", font=("Arial", 24, "bold"), width=290, height=80, command=self.generate_model)
        generate_button.grid(row=0, column=0, columnspan=3, rowspan=2, padx=(40, 140), pady=10, sticky="ew")

        confirm_button = ctk.CTkButton(self.selection_frame, text="Confirm Selections", font=("Arial", 15, "bold"), width=70, height=80, command=self.confirm_selections)
        confirm_button.grid(row=0, column=6, rowspan=2, padx=(20, 10), pady=10, sticky="ew")

    def confirm_selections(self):
        self.selected_input_column = self.input_select.get()
        self.selected_output_column = self.output_select.get()

        if not self.selected_input_column or not self.selected_output_column:
            messagebox.showerror("Error", "Please select both Input and Output columns.")
            return

        messagebox.showinfo("Selections Confirmed", f"Input Column: {self.selected_input_column}\nOutput Column: {self.selected_output_column}")

    def generate_model(self):
        if not self.selected_input_column or not self.selected_output_column:
            messagebox.showerror("Error", "You must confirm Input and Output selections before generating the model.")
            return

        messagebox.showinfo("Model Generation", f"Model generated with Input: {self.selected_input_column} and Output: {self.selected_output_column}")

    def apply_preprocessing(self, option):
        if self.loaded_data is None:
            messagebox.showerror("Error", "Please load a file first.")
            return

        if not self.selected_input_column or not self.selected_output_column:
            messagebox.showerror("Error", "Please confirm Input and Output selections first.")
            return

        if self.selected_input_column not in self.loaded_data.columns or self.selected_output_column not in self.loaded_data.columns:
            messagebox.showerror("Error", "One or more selected columns no longer exist in the dataset.")
            return

        columns_to_process = [self.selected_input_column, self.selected_output_column]

        if option == "Remove rows with NaN":
            self.remove_rows_with_nan(columns_to_process)
        elif option == "Fill with Mean":
            self.fill_na_values(columns_to_process, "mean")
        elif option == "Fill with Median":
            self.fill_na_values(columns_to_process, "median")
        elif option == "Fill with Constant Value":
            self.fill_na_with_constant(columns_to_process)
        elif option == "Show rows with NaN":
            self.show_nan_rows(columns_to_process)

        self.display_data_in_treeview(self.loaded_data)

    def remove_rows_with_nan(self, columns_to_process):
        df_original = self.loaded_data.copy()
        self.loaded_data.dropna(subset=columns_to_process, inplace=True)
        self.deleted_rows = pd.concat([df_original, self.loaded_data]).drop_duplicates(keep=False)
        if self.deleted_rows.empty:
            messagebox.showinfo("No Rows Deleted", "No rows were deleted.")
        else:
            messagebox.showinfo("Success", "Rows with NaN have been deleted.")
            if not self.show_deleted_button:
                self.show_deleted_button = ctk.CTkButton(self.v, text="Show Deleted Rows", command=lambda: self.show_deleted_rows(self.deleted_rows))
            self.show_deleted_button.grid(row=6, column=0, columnspan=2, pady=10)

    def fill_na_values(self, columns_to_process, method):
        for column in columns_to_process:
            if method == "mean":
                value = self.loaded_data[column].mean()
            elif method == "median":
                value = self.loaded_data[column].median()
            self.loaded_data[column] = self.loaded_data[column].fillna(value)
            messagebox.showinfo("Success", f"NaN values in '{column}' filled with {method}: {value:.2f}")

    def fill_na_with_constant(self, columns_to_process):
        top = ctk.CTkToplevel(self.v)
        top.title("Fill NaN Values")
        top.lift()

        ctk.CTkLabel(top, text="Enter constant values for the selected columns with NaN:").pack(pady=10)
        entries = {}

        for column in columns_to_process:
            ctk.CTkLabel(top, text=f"{column}:").pack(pady=5)
            entry = ctk.CTkEntry(top)
            entry.pack(pady=5)
            entries[column] = entry

        def apply_values():
            for column in columns_to_process:
                entry = entries[column]
                if entry.get():
                    try:
                        constant_value = float(entry.get())
                        self.loaded_data[column] = self.loaded_data[column].fillna(constant_value)
                        messagebox.showinfo("Success", f"NaN values in '{column}' filled with: {constant_value}")
                    except ValueError:
                        messagebox.showerror("Error", f"Invalid numeric value for '{column}'.")
                        return

            top.destroy()
            self.display_data_in_treeview(self.loaded_data)

        ctk.CTkButton(top, text="Apply", command=apply_values).pack(pady=10)
        top.protocol("WM_DELETE_WINDOW", top.destroy)

    def show_nan_rows(self, columns_to_process):
        nan_rows = self.loaded_data[columns_to_process][self.loaded_data[columns_to_process].isna().any(axis=1)]
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
        top = ctk.CTkToplevel(self.v)
        top.title(title)
        treeview = ttk.Treeview(top)
        treeview.pack(fill="both", expand=True)

        treeview["columns"] = list(df.columns)
        treeview["show"] = "headings"

        for col in treeview["columns"]:
            treeview.heading(col, text=col)

        for _, row in df.iterrows():
            treeview.insert("", "end", values=list(row))

def main():
    app = DataViewerApp()
    app.v.mainloop()

if __name__ == "__main__":
    main()

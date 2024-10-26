
import pandas as pd
from tkinter import messagebox, ttk
from file_reader import FileReader
from modeling import Modeling
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
        self.generate_frame = None
        self.file_reader = FileReader()
        self.modeling = Modeling(self.app)

    def import_data(self, file_path):
        self.app.deleted_rows = None
        if file_path.endswith(('.csv', '.xlsx', '.xls')):
            self.app.loaded_data = self.file_reader.read_csv_or_excel(
                file_path)
        elif file_path.endswith(('.sqlite', '.db')):
            self.app.loaded_data = self.file_reader.read_sqlite(file_path)

        if self.app.loaded_data is not None:
            self.display_data_in_treeview(self.app.loaded_data)

    def display_data_in_treeview(self, data):
        if self.app.tree is None:
            self.tree_frame = ctk.CTkFrame(self.app.v)
            self.tree_frame.grid(row=3, column=0, columnspan=2,
                                 padx=10, pady=10, sticky="nsew")
            self.app.tree = ttk.Treeview(self.tree_frame)
            self.app.tree.grid(row=0, column=0, sticky="nsew")
            scrollbar_x = ttk.Scrollbar(
                self.tree_frame, orient="horizontal", command=self.app.tree.xview)
            self.app.tree.configure(xscrollcommand=scrollbar_x.set)
            scrollbar_x.grid(row=1, column=0, sticky="ew")
            self.app.v.grid_rowconfigure(5, weight=1)

        self.app.tree.delete(*self.app.tree.get_children())
        self.app.tree['columns'] = list(data.columns)
        self.app.tree['show'] = 'headings'

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", background="#2B2B2B",
                        foreground="white", font=("Arial", 10, 'bold'))

        for col in self.app.tree['columns']:
            self.app.tree.heading(col, text=col)
            self.app.tree.column(col, width=150)

        self.app.tree.tag_configure(
            'oddrow', background='#333333', foreground='white')
        self.app.tree.tag_configure(
            'evenrow', background='#2B2B2B', foreground='white')

        for i, (_, row) in enumerate(data.iterrows()):
            if i % 2 == 0:
                self.app.tree.insert(
                    "", "end", values=list(row), tags=('evenrow',))
            else:
                self.app.tree.insert(
                    "", "end", values=list(row), tags=('oddrow',))

        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)

        self.options_selection(data.columns)

    def options_selection(self, columns):
        if self.app.selection_frame is not None:
            self.app.selection_frame.grid_forget()

        if self.option_frame is None:
            self.option_frame = ctk.CTkFrame(self.app.v)

        if self.generate_frame is None:
            self.generate_frame = ctk.CTkFrame(self.app.v)

        self.app.selection_frame = ctk.CTkFrame(self.app.v)
        self.app.selection_frame.grid(
            row=5, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        self.app.v.geometry("1000x550")

        self.preprocess_label = ctk.CTkLabel(
            self.option_frame, text="Preprocessing Options:", font=("Arial", 15, 'bold'))

        self.remove_nan_button = ctk.CTkButton(self.option_frame, text="Remove rows with NaN", font=(
            "Arial", 14, "bold"), width=160, height=40, command=lambda: self.apply_preprocessing("Remove rows with NaN"))
        self.fill_mean_button = ctk.CTkButton(self.option_frame, text="Fill with Mean", font=(
            "Arial", 14, "bold"), width=160, height=40, command=lambda: self.apply_preprocessing("Fill with Mean"))
        self.fill_median_button = ctk.CTkButton(self.option_frame, text="Fill with Median", font=(
            "Arial", 14, "bold"), width=160, height=40, command=lambda: self.apply_preprocessing("Fill with Median"))
        self.fill_constant_button = ctk.CTkButton(self.option_frame, text="Fill with Constant Value", font=(
            "Arial", 14, "bold"), width=160, height=40, command=lambda: self.apply_preprocessing("Fill with Constant Value"))

        input_label = ctk.CTkLabel(
            self.app.selection_frame, text="Select Input:", font=("Arial", 14, 'bold'))
        input_label.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        self.app.input_select = ctk.CTkOptionMenu(
            self.app.selection_frame, values=list(columns))
        self.app.input_select.grid(
            row=0, column=3, padx=10, pady=10, sticky="ew")

        output_label = ctk.CTkLabel(
            self.app.selection_frame, text="Select Output:", font=("Arial", 14, 'bold'))
        output_label.grid(row=1, column=2, padx=10, pady=10, sticky="e")

        self.app.output_select = ctk.CTkOptionMenu(
            self.app.selection_frame, values=list(columns))
        self.app.output_select.grid(
            row=1, column=3, padx=10, pady=10, sticky="ew")

        confirm_button = ctk.CTkButton(self.app.selection_frame, text="Confirm Selections", font=(
            "Arial", 15, "bold"), width=70, height=80, command=self.confirm_selections)
        confirm_button.grid(row=0, column=4, rowspan=2,
                            padx=(20, 10), pady=10, sticky="ew")

        self.generate_button = ctk.CTkButton(self.generate_frame, text="Generate model", font=(
            "Arial", 24, "bold"), width=290, height=80, command=self.modeling.generate_model)

    def confirm_selections(self):
        self.app.selected_input_column = self.app.input_select.get()
        self.app.selected_output_column = self.app.output_select.get()

        messagebox.showinfo(
            "Selections Confirmed", f"Input Column: {self.app.selected_input_column}\nOutput Column: {self.app.selected_output_column}")

        if self.generate_frame is not None:
            self.generate_frame.grid_forget()
        self.app.v.geometry("1000x680")
        self.option_frame.grid(row=6, column=0, columnspan=2,
                               pady=(10, 20), padx=10, sticky="ew")
        self.preprocess_label.grid(
            row=2, column=0, columnspan=4, padx=240, pady=10, sticky="e")
        self.remove_nan_button.grid(
            row=3, column=0, padx=(100, 0), pady=10, sticky="ew")
        self.fill_mean_button.grid(
            row=3, column=1, padx=(20, 0), pady=10, sticky="ew")
        self.fill_median_button.grid(
            row=3, column=2, padx=(20, 0), pady=10, sticky="ew")
        self.fill_constant_button.grid(
            row=3, column=3, padx=(20, 0), pady=10, sticky="ew")

    def apply_preprocessing(self, option):
        if self.app.selected_input_column not in self.app.loaded_data.columns or self.app.selected_output_column not in self.app.loaded_data.columns:
            messagebox.showerror(
                "Error", "One or more selected columns no longer exist in the dataset.")
            return

        columns_to_process = [
            self.app.selected_input_column, self.app.selected_output_column]

        if option == "Remove rows with NaN":
            df_original = self.app.loaded_data.copy()
            self.app.loaded_data.dropna(
                subset=columns_to_process, inplace=True)
            self.app.deleted_rows = pd.concat(
                [df_original, self.app.loaded_data]).drop_duplicates(keep=False)
            if self.app.deleted_rows.empty:
                messagebox.showinfo("No Rows Deleted", "No rows were deleted.")
            else:
                messagebox.showinfo(
                    "Success", "Rows with NaN have been deleted.")
        elif option in ["Fill with Mean", "Fill with Median", "Fill with Constant Value"]:
            self.fill_na_values(option, columns_to_process)

        self.display_data_in_treeview(self.app.loaded_data)

        if self.option_frame is not None:
            self.option_frame.grid_forget()
        self.app.v.geometry("1000x680")
        self.generate_frame.grid(row=6, column=0, pady=(0, 20))
        self.generate_button.grid(row=0, column=0, columnspan=4, rowspan=2, sticky="ew")

    def fill_na_values(self, method, columns):
        columns_with_nan = [
            col for col in columns if self.app.loaded_data[col].isna().any()]

        if not columns_with_nan:
            messagebox.showinfo(
                "No NaN", "No columns with NaN values found in the selected Input and Output.")
            return

        if method == "Fill with Constant Value":
            top = ctk.CTkToplevel(self.app.v)
            top.title("Fill NaN Values")
            top.lift()
            top.grab_set()
            top.geometry(f"+{self.app.v.winfo_x() + 200}+{self.app.v.winfo_y() + 200}")

            ctk.CTkLabel(
                top, text="Enter constant values for the selected columns with NaN:").pack(pady=10)

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
                            self.app.loaded_data[column] = self.app.loaded_data[column].fillna(
                                constant_value)
                            messagebox.showinfo(
                                "Success", f"NaN values in '{column}' filled with: {constant_value}")
                        except ValueError:
                            messagebox.showerror(
                                "Error", f"Invalid numeric value for '{column}'.")
                            return

                top.grab_release()
                top.destroy()
                self.display_data_in_treeview(self.app.loaded_data)

            ctk.CTkButton(top, text="Apply", command=apply_values).pack(pady=10)
            top.protocol("WM_DELETE_WINDOW", lambda: (top.grab_release(), top.destroy()))
        else:
            for column in columns_with_nan:
                if method == "Fill with Mean":
                    value = self.app.loaded_data[column].mean()
                    self.app.loaded_data[column] = self.app.loaded_data[column].fillna(value)
                    messagebox.showinfo(
                        "Success", f"NaN values in '{column}' filled with mean: {value:.2f}")
                elif method == "Fill with Median":
                    value = self.app.loaded_data[column].median()
                    self.app.loaded_data[column] = self.app.loaded_data[column].fillna(value)
                    messagebox.showinfo(
                        "Success", f"NaN values in '{column}' filled with median: {value:.2f}")

        self.display_data_in_treeview(self.app.loaded_data)
 
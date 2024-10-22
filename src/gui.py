import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import customtkinter as ctk
import pandas as pd
from file_reader import read_csv_or_excel, read_sqlite

v = None  
tree = None  
loaded_data = None  
deleted_rows = None  
show_deleted_button = None  
input_select = None
output_select = None
selection_frame = None
selected_input_column = None
selected_output_column = None
original_window_size = None
file_path_entry = None

def create_window():
    global v, original_window_size
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    
    v = ctk.CTk()  
    v.title("Data Viewer")
    original_window_size = "1000x500"
    v.geometry(original_window_size)
    
    v.grid_rowconfigure(0, weight=1)
    v.grid_columnconfigure(0, weight=1)
    
    return v

def open_files():
    global file_path_entry
    file = filedialog.askopenfilename(
            title="Open",
            filetypes=(("CSV Files","*.csv"),
                       ("Excel Files","*.xlsx"),
                       ("Excel Files","*.xls"),
                       ("SQLite Files","*.sqlite"),
                       ("DB Files","*.db"))
    )
    if file:  
        import_data(file)
        file_path_entry.configure(state="normal")
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(0, file)
        file_path_entry.configure(state="readonly")

def clear_table():
    global input_select, output_select, selection_frame, original_window_size, file_path_entry
    
    if tree is None:
        return

    tree.delete(*tree.get_children())  

    if selection_frame is not None:
        selection_frame.grid_forget()
        input_select = None
        output_select = None
        v.geometry(original_window_size)

    file_path_entry.configure(state="normal")
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, "No file selected")
    file_path_entry.configure(state="readonly")

def create_button():
    global file_path_entry
    button_frame = ctk.CTkFrame(v)  
    button_frame.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    open_button = ctk.CTkButton(button_frame, text="Open File", font=("Arial", 15, "bold"), width=140, height=40, command=open_files)
    clear_button = ctk.CTkButton(button_frame, text="Clear", font=("Arial", 15, "bold"), width=140, height=40, command=clear_table)
   
    open_button.grid(row=0, column=0, padx=(40,5), pady=5, sticky="ew")
    clear_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    file_path_entry = ctk.CTkEntry(button_frame, width=400, font=("Arial", 12))
    file_path_entry.grid(row=1, column=0, columnspan=2, padx=40, pady=10, sticky="ew")
    file_path_entry.insert(0, "No file selected")
    file_path_entry.configure(state="readonly")

    preprocess_label = ctk.CTkLabel(button_frame, text="Preprocessing Options:", font=("Arial", 15, 'bold'))
    preprocess_label.grid(row=0, column=2, padx=(80, 10), pady=10, sticky="e")

    options = ["Remove rows with NaN", "Fill with Mean", "Fill with Median", 
               "Fill with Constant Value", "Show rows with NaN"]

    preprocess_var = ctk.StringVar(value=options[0])
    preprocess_menu = ctk.CTkOptionMenu(button_frame, variable=preprocess_var, values=options)
    preprocess_menu.grid(row=0, column=3, padx=(2, 5), pady=10, sticky="ew")

    apply_button = ctk.CTkButton(button_frame, text="Apply Preprocessing",font=("Arial", 14, "bold"),  width=160, height=40,command=lambda: apply_preprocessing(preprocess_var.get()))
    apply_button.grid(row=1, column=3, padx=(5, 5), pady=10, sticky="ew")

def create_label():
    label_title = ctk.CTkLabel(v, text="LINEAR REGRESSION ANALYTICS", font=("Arial", 45, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=20, sticky="ew")

def import_data(file_path):
    global loaded_data, deleted_rows, show_deleted_button
    deleted_rows = None  
    if show_deleted_button:
        show_deleted_button.grid_forget()
    
    if file_path.endswith(('.csv', '.xlsx', '.xls')):
        loaded_data = read_csv_or_excel(file_path)
    elif file_path.endswith(('.sqlite', '.db')):
        loaded_data = read_sqlite(file_path)
    
    if loaded_data is not None:
        detect_nan(loaded_data)
        display_data_in_treeview(loaded_data)

def detect_nan(data):
    nan_info = data.isna().sum()
    nan_cols = nan_info[nan_info > 0]
    if not nan_cols.empty:
        messagebox.showinfo("Missing Values", f"NaN detected in: \n{nan_cols}")
    else:
        messagebox.showinfo("No Missing Values", "There are no missing values in the data.")

def display_data_in_treeview(data):
    global tree, tree_frame, input_select, output_select, selection_frame
    if tree is None:
        tree_frame = ctk.CTkFrame(v)
        tree_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        tree = ttk.Treeview(tree_frame)
        tree.grid(row=0, column=0, sticky="nsew")
        
        scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        v.grid_rowconfigure(5, weight=1)
    
    tree.delete(*tree.get_children())  
    tree['columns'] = list(data.columns)
    tree['show'] = 'headings'
    
    for col in tree['columns']:
        tree.heading(col, text=col)
    
    for _, row in data.iterrows():
        tree.insert("", "end", values=list(row))

    tree_frame.grid_rowconfigure(0, weight=1)  
    tree_frame.grid_columnconfigure(0, weight=1)
    
    add_input_output_buttons(data.columns)

def add_input_output_buttons(columns):
    global input_select, output_select, selection_frame

    if selection_frame is not None:
        selection_frame.grid_forget()
    
    selection_frame = ctk.CTkFrame(v)
    selection_frame.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    v.geometry("1000x700")

    input_label = ctk.CTkLabel(selection_frame, text="Select Input:", font=("Arial", 14, 'bold'))
    input_label.grid(row=0, column=4, padx=10, pady=10, sticky="e")
    
    input_select = ctk.CTkOptionMenu(selection_frame, values=list(columns))
    input_select.grid(row=0, column=5, padx=10, pady=10, sticky="ew")

    output_label = ctk.CTkLabel(selection_frame, text="Select Output:", font=("Arial", 14, 'bold'))
    output_label.grid(row=1, column=4, padx=10, pady=10, sticky="e")
    
    output_select = ctk.CTkOptionMenu(selection_frame, values=list(columns))
    output_select.grid(row=1, column=5, padx=10, pady=10, sticky="ew")

    generate_button = ctk.CTkButton(selection_frame, text="Generate model", font=("Arial", 24, "bold"), width=290, height=80, command=generate_model)
    generate_button.grid(row=0, column=0, columnspan=3,rowspan=2, padx=(40,140), pady=10, sticky="ew")
    
    confirm_button = ctk.CTkButton(selection_frame, text="Confirm Selections", font=("Arial", 15, "bold"), width=70, height=80, command=confirm_selections)
    confirm_button.grid(row=0, column=6, rowspan=2, padx=(20,10), pady=10, sticky="ew")

def confirm_selections():
    global selected_input_column, selected_output_column
    
    selected_input_column = input_select.get()
    selected_output_column = output_select.get()
    
    if not selected_input_column or not selected_output_column:
        messagebox.showerror("Error", "Please select both Input and Output columns.")
        return

    messagebox.showinfo("Selections Confirmed", f"Input Column: {selected_input_column}\nOutput Column: {selected_output_column}")

def generate_model():
    global selected_input_column, selected_output_column

    if not selected_input_column or not selected_output_column:
        messagebox.showerror("Error", "You must confirm Input and Output selections before generating the model.")
        return

    messagebox.showinfo("Model Generation", f"Model generated with Input: {selected_input_column} and Output: {selected_output_column}")

def apply_preprocessing(option):
    global loaded_data, deleted_rows, show_deleted_button, selected_input_column, selected_output_column
    if loaded_data is None:
        messagebox.showerror("Error", "Please load a file first.")
        return

    if not selected_input_column or not selected_output_column:
        messagebox.showerror("Error", "Please confirm Input and Output selections first.")
        return

    if selected_input_column not in loaded_data.columns or selected_output_column not in loaded_data.columns:
        messagebox.showerror("Error", "One or more selected columns no longer exist in the dataset.")
        return
    
    columns_to_process = [selected_input_column, selected_output_column]
    
    if option == "Remove rows with NaN":
        df_original = loaded_data.copy()  
        loaded_data.dropna(subset=columns_to_process, inplace=True)
        deleted_rows = pd.concat([df_original, loaded_data]).drop_duplicates(keep=False)
        if deleted_rows.empty:
            messagebox.showinfo("No Rows Deleted", "No rows were deleted.")
        else:
            messagebox.showinfo("Success", "Rows with NaN have been deleted.")
            if not show_deleted_button:
                show_deleted_button = ctk.CTkButton(v, text="Show Deleted Rows", command=lambda: show_deleted_rows(deleted_rows))
            show_deleted_button.grid(row=6, column=0, columnspan=2, pady=10)

    elif option in ["Fill with Mean", "Fill with Median", "Fill with Constant Value"]:
        fill_na_values(option, columns_to_process)

    elif option == "Show rows with NaN":
        show_nan_rows(loaded_data[columns_to_process])

    display_data_in_treeview(loaded_data)

def fill_na_values(method, columns):
    global loaded_data

    columns_with_nan = [col for col in columns if loaded_data[col].isna().any()]

    if not columns_with_nan:
        messagebox.showinfo("No NaN", "No columns with NaN values found in the selected Input and Output.")
        return

    if method == "Fill with Constant Value":
        top = ctk.CTkToplevel(v)
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
                        loaded_data[column] = loaded_data[column].fillna(constant_value)
                        messagebox.showinfo("Success", f"NaN values in '{column}' filled with: {constant_value}")
                    except ValueError:
                        messagebox.showerror("Error", f"Invalid numeric value for '{column}'.")
                        return

            top.destroy()
            display_data_in_treeview(loaded_data)

        ctk.CTkButton(top, text="Apply", command=apply_values).pack(pady=10)
        top.protocol("WM_DELETE_WINDOW", top.destroy)
    else:
        for column in columns_with_nan:
            if method == "Fill with Mean":
                value = loaded_data[column].mean()
                loaded_data[column] = loaded_data[column].fillna(value)
                messagebox.showinfo("Success", f"NaN values in '{column}' filled with mean: {value:.2f}")
            elif method == "Fill with Median":
                value = loaded_data[column].median()
                loaded_data[column] = loaded_data[column].fillna(value)
                messagebox.showinfo("Success", f"NaN values in '{column}' filled with median: {value:.2f}")

    display_data_in_treeview(loaded_data)

def show_nan_rows(df):
    nan_rows = df[df.isna().any(axis=1)]
    if nan_rows.empty:
        messagebox.showinfo("No Rows with NaN", "There are no rows with missing values.")
    else:
        show_data_in_window(nan_rows, "Rows with NaN")

def show_deleted_rows(df_deleted):
    if df_deleted.empty:
        messagebox.showinfo("No Deleted Rows", "No rows were deleted.")
    else:
        show_data_in_window(df_deleted, "Deleted Rows")

def show_data_in_window(df, title):
    top = ctk.CTkToplevel(v)
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
    create_window()
    create_label()
    create_button()
    v.mainloop()

if __name__ == "__main__":
    main()

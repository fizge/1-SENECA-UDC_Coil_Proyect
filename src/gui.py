

import tkinter as tk 
from tkinter import filedialog, ttk, messagebox
import customtkinter as ctk
import pandas as pd
from file_reader import read_csv_or_excel, read_sqlite
from data_processing import DataProcessing

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
        self.data_processing = DataProcessing(self)

    def create_window(self):
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        self.v = ctk.CTk()  
        self.v.title("Data Viewer")
        self.original_window_size = "1000x700"
        self.v.geometry(self.original_window_size)
        self.v.minsize(1000,500)
        
        self.v.grid_rowconfigure(0, weight=1)
        self.v.grid_columnconfigure(0, weight=1)

        
        return self.v

    def open_files(self):
        file = filedialog.askopenfilename(
                title="Open",
                filetypes=(("CSV Files","*.csv"),
                           ("Excel Files","*.xlsx"),
                           ("Excel Files","*.xls"),
                           ("SQLite Files","*.sqlite"),
                           ("DB Files","*.db"))
        )
        if file:  
            self.data_processing.import_data(file)
            self.file_path_entry.configure(state="normal")
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, file)
            self.file_path_entry.configure(state="readonly")

    # def clear_table(self):
    #     if self.tree is None:
    #         return

    #     self.tree.delete(*self.tree.get_children())  

    #     if self.selection_frame is not None:
    #         self.selection_frame.grid_forget()
    #         self.input_select = None
    #         self.output_select = None
    #         self.v.geometry(self.original_window_size)

    #     self.file_path_entry.configure(state="normal")
    #     self.file_path_entry.delete(0, tk.END)
    #     self.file_path_entry.insert(0, "No file selected")
    #     self.file_path_entry.configure(state="readonly")

    def create_button(self):
        button_frame = ctk.CTkFrame(self.v)  
        button_frame.grid(row=2, column=0, columnspan=1, pady=5, padx=5)

        
        open_button = ctk.CTkButton(button_frame, text="Open File", font=("Arial", 15, "bold"), width=140, height=40, command=self.open_files)
        # clear_button = ctk.CTkButton(button_frame, text="Clear", font=("Arial", 15, "bold"), width=140, height=40, command=self.clear_table)
       
        open_button.grid(row=0, column=0, padx=(40,5), pady=5, sticky="ew")
        # clear_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.file_path_entry = ctk.CTkEntry(button_frame, width=400, font=("Arial", 12))
        self.file_path_entry.grid(row=1, column=0, columnspan=2, padx=40, pady=10, sticky="ew")
        self.file_path_entry.insert(0, "No file selected")
        self.file_path_entry.configure(state="readonly")
        self.file_path_entry.configure(state="normal")

        preprocess_label = ctk.CTkLabel(button_frame, text="Preprocessing Options:", font=("Arial", 15, 'bold'))
        preprocess_label.grid(row=0, column=2, padx=(80, 10), pady=10, sticky="e")

        options = ["Remove rows with NaN", "Fill with Mean", "Fill with Median", 
                   "Fill with Constant Value"]

        preprocess_var = ctk.StringVar(value=options[0])
        preprocess_menu = ctk.CTkOptionMenu(button_frame, variable=preprocess_var, values=options)
        preprocess_menu.grid(row=0, column=3, padx=(2, 5), pady=10, sticky="ew")

        apply_button = ctk.CTkButton(button_frame, text="Apply Preprocessing or select input/output", font=("Arial", 14, "bold"),  width=160, height=40,
                                      command=lambda: self.data_processing.apply_preprocessing(preprocess_var.get()))
        apply_button.grid(row=1, column=3, padx=(5, 5), pady=10, sticky="ew")

    def create_label(self):
        label_title = ctk.CTkLabel(self.v, text="LINEAR REGRESSION ANALYTICS", font=("Arial", 15, "bold"))
        label_title.grid(row=0, column=0, columnspan=1, pady=10)

    
    
    def main(self):
        self.create_window()
        self.create_label()
        self.create_button()
        self.v.mainloop()

if __name__ == "__main__":
    app = DataViewerApp()
    app.main()
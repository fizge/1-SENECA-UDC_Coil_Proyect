import tkinter as tk 
from tkinter import filedialog, ttk, messagebox
import customtkinter as ctk
import pandas as pd
from data_processing import DataProcessing

class DataViewerApp:
    def __init__(self):
        self.v = None  
        self.tree = None  
        self.loaded_data = None  
        self.deleted_rows = None
        self.open_button = None  
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
        self.v.title("LINEAR REGRESION ANALYTICS")
        self.original_window_size = "1000x150"
        self.v.geometry(self.original_window_size)
        
        self.v.grid_rowconfigure(0, weight=1)
        self.v.grid_columnconfigure(0, weight=1)
        
        return self.v

    def open_files(self):
        file = filedialog.askopenfilename(
                title="Open",
                filetypes=[("CSV Files","*.csv"),
                           ("Excel Files","*.xlsx"),
                           ("Excel Files","*.xls"),
                           ("SQLite Files","*.sqlite ; *.db")]
        )
        if file:  
            self.data_processing.import_data(file)
            self.file_path_entry.configure(state="normal")
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, file)
            self.file_path_entry.configure(state="readonly")
        self.open_button.configure(text="Clear", command=self.clear_table)

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
        self.open_button.configure(text="Open File", command=self.open_files)

    def create_button(self):
        button_frame = ctk.CTkFrame(self.v)  
        button_frame.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")
        button_frame.grid_columnconfigure(0, weight=1)

        self.open_button = ctk.CTkButton(button_frame, text="Open File", font=("Arial", 20, "bold"), width=140, height=40, command=self.open_files)
        self.open_button.grid(row=0, column=0,columnspan =10, padx=250, pady=20, sticky="ew")
        
        path_label = ctk.CTkLabel(button_frame, text="Path:", font=("Arial", 18, 'bold'))
        path_label.grid(row=1, column=0, padx=250, pady=10, sticky="w")
        
        self.file_path_entry = ctk.CTkEntry(button_frame, width=1000, font=("Arial", 12))
        self.file_path_entry.grid(row=1, column=0, columnspan=4, padx=310, pady=10, )
        self.file_path_entry.insert(0, "No file selected")
        self.file_path_entry.configure(state="readonly")

        


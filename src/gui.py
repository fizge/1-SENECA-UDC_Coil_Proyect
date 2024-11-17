import tkinter as tk
import customtkinter as ctk
import pandas as pd
from data_processing import DataProcessing
from modeling import Modeling
from load_model import LoadModel

class DataViewerApp:
    def __init__(self):
        self.v = None
        self.tree = None
        self.button_frame = None
        self.loaded_data = None
        self.deleted_rows = None
        self.open_button = None
        self.input_select = None
        self.output_select = None
        self.selection_frame = None
        self.selected_input_column = None
        self.selected_output_column = None
        self.original_window_size = None
        self.file_path_entry = None
        self.data_processing = DataProcessing(self)
        self.modeling = Modeling(self)
        self.load = LoadModel(self)
        self.save_model_button = None
        

    def create_window(self):
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.v = ctk.CTk()
        self.v.title("LINEAR REGRESION ANALYTICS")
        self.original_window_size = "1000x450+200+0"
        self.v.geometry(self.original_window_size)

        self.v.grid_rowconfigure(0, weight=1)
        self.v.grid_columnconfigure(0, weight=1)

        return self.v
    
    def create_button(self):
        self.button_frame = ctk.CTkFrame(self.v)
        self.button_frame.grid(row=0, column=0, pady=10, padx=10, sticky="ew")
        self.button_frame.grid_columnconfigure(0, weight=0)  
        self.button_frame.grid_columnconfigure(1, weight=1)  
        self.button_frame.grid_columnconfigure(2, weight=0)  

        path_label = ctk.CTkLabel(self.button_frame, text="Path:", font=("Arial", 18, 'bold'))
        path_label.grid(row=0, column=0, padx=(40, 10), pady=10, sticky="w")

        self.file_path_entry = ctk.CTkEntry(self.button_frame, width=100, font=("Arial", 12))
        self.file_path_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")
        self.file_path_entry.insert(0, "No file selected")
        self.file_path_entry.configure(state="readonly")

        self.open_button = ctk.CTkButton(self.button_frame, text="Open File", font=("Arial", 20, "bold"),
                                         width=140, height=40, command=self.data_processing.open_files)
        self.open_button.grid(row=0, column=2, padx=(10, 20), pady=10, sticky="e")

        # Cargar Modelo Button (al lado de Open File)
        self.load_button = ctk.CTkButton(self.button_frame, text="Load Model", font=("Arial", 20, "bold"),
                                        width=140, height=40, command=self.load.load_model)
        self.load_button.grid(row=0, column=3, padx=(0, 20), pady=10, sticky="e")

    

import tkinter as tk
import customtkinter as ctk
import pandas as pd
from preselection_scenario import Preselection
from modeling_scenario import Modeling
from loading_scenario import LoadModel

class LinearRegressionAnalyitics:
    def __init__(self):
        self.v = None
        self.tree = None
        self.initial_frame = None
        self.original_window_size = None
        self.open_button = None
        self.file_path_entry = None
        self.file_path_label = None
        self.preselection = Preselection(self)
        self.modeling = Modeling(self)
        self.load = LoadModel(self)
        
        

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
    
    def gui_initialization(self):
        self.initial_frame = ctk.CTkFrame(self.v)
        self.initial_frame.grid(row=0, column=0, pady=10, padx=10, sticky="ew")
        self.initial_frame.grid_columnconfigure(0, weight=0)  
        self.initial_frame.grid_columnconfigure(1, weight=1)  
        self.initial_frame.grid_columnconfigure(2, weight=0)  

        self.file_path_label = ctk.CTkLabel(self.initial_frame, text="Path:", font=("Arial", 18, 'bold'))
        self.file_path_label.grid(row=0, column=0, padx=(40, 10), pady=10, sticky="w")

        self.file_path_entry = ctk.CTkEntry(self.initial_frame, width=100, font=("Arial", 12))
        self.file_path_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")
        self.file_path_entry.insert(0, "No file selected")
        self.file_path_entry.configure(state="readonly")

        self.open_button = ctk.CTkButton(self.initial_frame, text="Open File", font=("Arial", 20, "bold"),
                                         width=140, height=40, command=self.preselection.open_files)
        self.open_button.grid(row=0, column=2, padx=(10, 20), pady=10, sticky="e")

        self.load_button = ctk.CTkButton(self.initial_frame, text="Load Model", font=("Arial", 20, "bold"),
                                        width=140, height=40, command=self.load.load_model)
        self.load_button.grid(row=0, column=3, padx=(0, 20), pady=10, sticky="e")

    

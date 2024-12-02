import tkinter as tk
import customtkinter as ctk
import pandas as pd
from PIL import Image, ImageTk
from scenarios.preselection_scenario import Preselection
from scenarios.modeling_scenario import Modeling
from scenarios.loading_scenario import LoadModel


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
        self.v.title("DataPilot")
        self.original_window_size = "1000x450+200+0"
        self.v.geometry(self.original_window_size)

        self.v.grid_rowconfigure(0, weight=1)
        self.v.grid_columnconfigure(0, weight=1)

        return self.v

    def gui_presentation(self):
        self.presentation_frame = ctk.CTkFrame(self.v, fg_color='#242424')
        self.presentation_frame.grid(
            row=0, column=0, pady=10, padx=10, sticky="nsew")

        self.presentation1_label = ctk.CTkLabel(
            self.presentation_frame, text="¡ Welcome to  DataPilot !", font=("Arial", 36, 'bold'))
        self.presentation1_label.grid(
            row=0, column=0, padx=60, pady=40, sticky="n")

        self.start_button = ctk.CTkButton(self.presentation_frame, text="Start", font=("Arial", 40, "bold"),
                                          width=240, height=80, corner_radius=100, command=self.gui_initialization)
        self.start_button.grid(row=1, column=0, padx=20, pady=(10,50), sticky="n")

        self.separator = tk.Frame(self.presentation_frame, width=2, bg='white')
        self.separator.grid(row=2, column=0, padx= 60, sticky="ew")

        self.presentation2_label = ctk.CTkLabel(self.presentation_frame, text="This application is designed to help you explore and analyze data using simple linear regression models.\n\n You can upload your own datasets and generate graphs that display the relationship between variables,\n\n as well as make predictions based on your data and save your regression models.",
                                                font=("Arial", 18, 'bold'))
        self.presentation2_label.grid(
            row=3, column=0, padx=60, pady=30, sticky="n")

    def gui_initialization(self):

        if self.presentation_frame is not None:
            self.presentation_frame.destroy()

        self.initial_frame = ctk.CTkFrame(self.v,fg_color='#242424')
        self.initial_frame.grid(row=0, column=0, pady=(
            20, 10), padx=10, sticky="new")
        self.initial_frame.grid_columnconfigure(0, weight=0)
        self.initial_frame.grid_columnconfigure(1, weight=1)
        self.initial_frame.grid_columnconfigure(2, weight=0)

        self.file_path_label = ctk.CTkLabel(
            self.initial_frame, text="Path:", font=("Arial", 18, 'bold'))
        self.file_path_label.grid(
            row=0, column=0, padx=(40, 10), pady=10, sticky="w")

        self.file_path_entry = ctk.CTkEntry(
            self.initial_frame, width=100, font=("Arial", 12))
        self.file_path_entry.grid(
            row=0, column=1, padx=(0, 10), pady=10, sticky="ew")
        self.file_path_entry.insert(0, "No file selected")
        self.file_path_entry.configure(state="readonly")

        self.open_button = ctk.CTkButton(self.initial_frame, text="Open File", font=("Arial", 20, "bold"),
                                         width=140, height=40, corner_radius=100, command=self.preselection.open_files)
        self.open_button.grid(row=0, column=2, padx=(
            10, 20), pady=10, sticky="e")

        self.load_button = ctk.CTkButton(self.initial_frame, text="Load Model", font=("Arial", 20, "bold"),
                                         width=140, height=40, corner_radius=100, command=self.load.load_model)
        self.load_button.grid(
            row=0, column=3, padx=(0, 20), pady=10, sticky="e")

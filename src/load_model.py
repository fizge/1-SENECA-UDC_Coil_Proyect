import pickle
from tkinter import messagebox,filedialog
import customtkinter as ctk

class LoadModel:
    def __init__(self, app):
        self.app = app

    def load_model(self):
        file_path = filedialog.askopenfilename(filetypes=[("Model files", "*.pkl *.joblib")])
        if file_path:
            try:
                # Load the model file
                with open(file_path, "rb") as f:
                    model_data = pickle.load(f)
                
                # Hide existing frames
                if self.app.modeling.graphic_frame is not None:
                    self.app.modeling.graphic_frame.grid_forget()
                if self.app.selection_frame is not None:
                    self.app.selection_frame.grid_forget()
                if self.app.data_processing.tree_frame is not None:
                    self.app.data_processing.tree_frame.grid_forget()
                if self.app.data_processing.option_frame is not None:
                    self.app.data_processing.option_frame.grid_forget()

                # Create the frame to display the model data
                self.create_model_info_frame(model_data)
                
            except (pickle.UnpicklingError, AttributeError, KeyError) as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")

    def create_model_info_frame(self, model_data):
        # Create a new frame for displaying the model information
        self.app.button_frame.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        info_frame = ctk.CTkFrame(self.app.v)
        info_frame.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        # Display model formula
        formula = model_data.get("formula", "No disponible")
        formula_label = ctk.CTkLabel(info_frame, text=f"Fórmula: {formula}", font=("Arial", 12, 'bold'), text_color="white")
        formula_label.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="w")

        # Display R² and MSE
        r_squared = model_data.get("r_squared", "No disponible")
        mse = model_data.get("mse", "No disponible")
        r_squared_label = ctk.CTkLabel(info_frame, text=f"R²: {r_squared}", font=("Arial", 12, 'bold'), text_color="white")
        mse_label = ctk.CTkLabel(info_frame, text=f"MSE: {mse}", font=("Arial", 12, 'bold'), text_color="white")
        r_squared_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        mse_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        # Display description
        description = model_data.get("description", "No disponible")
        if description == "Write the model description here...":
            description = "No disponible"
        description_label = ctk.CTkLabel(info_frame, text="Descripción:", font=("Arial", 12, 'bold'), text_color="white")
        description_label.grid(row=5, column=0, padx=10, pady=(10, 0), sticky="w")
        description_text = ctk.CTkTextbox(info_frame, height=5, width=50)
        description_text.insert("1.0", description)
        description_text.configure(state="disabled")  # Make it read-only
        description_text.grid(row=6, column=0, padx=10, pady=5)

        info_frame.grid_rowconfigure(0, weight=1)
        info_frame.grid_columnconfigure(0, weight=1)

        # Set window geometry for the new model info
        self.app.v.geometry("1000x500")


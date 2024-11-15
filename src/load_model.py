
import pickle
from tkinter import messagebox, filedialog
import customtkinter as ctk
from modeling import *

class LoadModel:
    def __init__(self, app):
        self.app = app
        self.info_frame = None 
        self.model = None
        self.model_load = None 

    def load_model(self):
        file_path = filedialog.askopenfilename(filetypes=[("Model files", "*.pkl *.joblib")])
        if file_path:
            try:
                # Load the model file
                with open(file_path, "rb") as f:
                    data = pickle.load(f)  # Guardamos los datos del modelo aquí
                    self.output_column = data.get('output_column')  
                    self.input_column = data.get('input_column') 
                    self.model_load = data.get('model')
                    self.formula = data.get("formula", "No disponible")
                    self.r_squared = data.get("r_squared", "No disponible")
                    self.mse = data.get("mse", "No disponible")
                    self.description = data.get("description", "No disponible")
                    
                    
                
                # Hide existing frames
                # if self.Modeling.graphic_frame is not None:
                #     self.Modeling.graphic_frame.grid_forget()
                if self.app.selection_frame is not None:
                    self.app.selection_frame.grid_forget()
                if self.app.data_processing.tree_frame is not None:
                    self.app.data_processing.tree_frame.grid_forget()
                if self.app.data_processing.option_frame is not None:
                    self.app.data_processing.option_frame.grid_forget()
                

                # Create the frame to display the model data
                self.create_model_info_frame()
                
            except (pickle.UnpicklingError, AttributeError, KeyError) as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")

    def create_model_info_frame(self):
        # Create a new frame for displaying the model information
        self.app.button_frame.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")
        
        

        self.info_frame = ctk.CTkFrame(self.app.v)
        self.info_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        formula_label = ctk.CTkLabel(self.info_frame, text=f"Fórmula: {self.formula}\nR²: {self.r_squared:.3f} MSE: {self.mse:.3f}", font=("Arial", 12, 'bold'), text_color="white")
        formula_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        # Prediction button
        prediction2_button = ctk.CTkButton(
            self.info_frame, text="Predicción", font=("Arial", 18, "bold"),
            width=30, height=30, command=self.prediction_load_model)
        prediction2_button.grid(row=7, column=0, padx=10, pady=5, sticky="w")

        # Display description
        
        if self.description == "Write the model description here...":
            self.description = "No disponible"
        description_label = ctk.CTkLabel(self.info_frame, text="Descripción:", font=("Arial", 12, 'bold'), text_color="white")
        description_label.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")
        description_text = ctk.CTkTextbox(self.info_frame, height=5, width=50)
        description_text.insert("1.0", self.description)
        description_text.configure(state="disabled")  # Make it read-only
        description_text.grid(row=4, column=0, padx=10, pady=5,sticky="ew")
        
        self.prediction_input = ctk.CTkEntry(self.info_frame, width=30)
        self.prediction_input.grid(row=6, column=0, padx=10, pady=5, sticky="ew")

        self.info_frame.grid_rowconfigure(0, weight=1)
        self.info_frame.grid_columnconfigure(0, weight=1)

        # Set window geometry for the new model info
        self.app.v.geometry("1000x500")

    def prediction_load_model(self):
       
        if self.output_column and self.input_column :
                # Ask for input value
                input_value = float(self.prediction_input.get())  # Ensure you have a field to get this input
                prediction = self.model_load.predict([[input_value]])  # Make sure the model is available
                messagebox.showinfo("Archivo cargado", f"Archivo cargado. Columna de salida: {self.output_column}, Columna de entrada: {self.input_column} , modelo {self.model_load}")
                prediccion_label = ctk.CTkLabel(self.info_frame, 
                                                text=f"El valor calculado basado en la entrada proporcionada ({self.input_column} : {input_value}) es de -->  {prediction[0]:.2f} ({self.output_column})", 
                                                font=("Arial", 12, 'bold'), 
                                                text_color="white")
                prediccion_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        else:
                messagebox.showerror("Error", "No se pudo obtener el modelo o las columnas del archivo.")
       

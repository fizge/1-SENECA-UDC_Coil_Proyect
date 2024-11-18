
import pickle
from tkinter import messagebox, filedialog
import customtkinter as ctk
from modeling import *

class LoadModel:
    def __init__(self, app):
        self.app = app
        self.info_frame = None
        self.model = None 
        self.formula = None
        self.r_squared = None
        self.mse = None
        self.description = None
        self.output_column = None
        self.input_column = None
        
    def load_model(self):
        file_path = filedialog.askopenfilename(filetypes=[("Model files", "*.pkl *.joblib")])
        if file_path:
            try:
                # Load the model file
                with open(file_path, "rb") as f:
                    data = pickle.load(f)  # Guardamos los datos del modelo aquí
                    self.output_column = data.get('output_column')  
                    self.input_column = data.get('input_column') 
                    self.model = data.get('model')
                    self.formula = data.get("formula", "Not avalable")
                    self.r_squared = data.get("r_squared", "Not avalable")
                    self.mse = data.get("mse", "Not avalable")
                    self.description = data.get("description", "Not avalable")
            
                self.app.v.grid_columnconfigure(0, weight=1, uniform="column")
                self.app.v.grid_columnconfigure(1, weight=0, uniform="column2")
               
                if self.app.modeling.graphic_frame is not None:
                    self.app.modeling.graphic_frame.grid_forget()                     
                if self.app.data_processing.selection_frame is not None:
                    self.app.data_processing.selection_frame.grid_forget()
                if self.app.data_processing.tree_frame is not None:
                    self.app.data_processing.tree_frame.grid_forget()
                    self.app.tree = None
                if self.app.data_processing.option_frame is not None:
                    self.app.data_processing.option_frame.grid_forget()
                self.app.v.geometry("1000x450+200+0")

                # Create the frame to display the model data
                self.create_model_info_frame()
                messagebox.showinfo("Recovered model", f"Recovered model. Output Column: {self.output_column}, Input Column: {self.input_column}")
            except (pickle.UnpicklingError, AttributeError, KeyError) as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")

    def create_model_info_frame(self):
       
        self.app.initial_frame.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        if self.info_frame is not None:
             self.info_frame.destroy()
        self.info_frame = ctk.CTkFrame(self.app.v)
        self.info_frame.grid(row=2, column=0, columnspan=2, pady=(10,20), padx=10, sticky="ew")

        labels_frame = ctk.CTkFrame(self.info_frame, fg_color="#242424", border_width=3,border_color='white', corner_radius=10)  
        labels_frame.grid(row=0, column=0, rowspan=4, pady=30, padx=80, sticky="nw")      

        formula_label = ctk.CTkLabel(labels_frame, text=f"Linear Regresion Ecuation:", font=("Arial", 16, 'bold'), text_color="white")
        formula_label.grid(row=0, column=0, padx=20, pady=(10,0), sticky="w")
        formula2_label = ctk.CTkLabel(labels_frame, text=f"{self.formula}", font=("Arial", 14, 'bold'), text_color="white")
        formula2_label.grid(row=1, column=0, padx=20, pady=0, sticky="w")
        r2_label = ctk.CTkLabel(labels_frame, text=f"R²: {self.r_squared:.4f}", font=("Arial", 14, 'bold'), text_color="white")
        r2_label.grid(row=2, column=0, padx=20, pady=0, sticky="w")
        mse_label = ctk.CTkLabel(labels_frame, text=f"MSE: {self.mse:.4f}", font=("Arial", 14, 'bold'), text_color="white")
        mse_label.grid(row=3, column=0, padx=20, pady=(0,10), sticky="w")

        description_label = ctk.CTkLabel(self.info_frame, text="Description:", font=("Arial", 18, 'bold'), text_color="white")
        description_label.grid(row=0, column=1, padx=80, pady=(20,0), sticky="n")
        description_text = ctk.CTkTextbox(self.info_frame, height=90, width=400, fg_color="#242424",border_width=3,border_color='white', corner_radius=10)
        description_text.insert("1.0", self.description)
        description_text.configure(state="disabled")  
        description_text.grid(row=0, column=1,rowspan=3, padx=0, pady=60,sticky="e")
        
        prediction_label = ctk.CTkLabel(self.info_frame, text=f"Input value:", font=("Arial", 15, 'bold'), text_color="white")
        prediction_label.grid(row=4, column=0,columnspan=2, padx=80, pady=(0,20), sticky="w")

        self.prediction_input = ctk.CTkEntry(self.info_frame, width=550)
        self.prediction_input.grid(row=4, column=0, columnspan=2, padx=(180,10), pady=(0,20), sticky="w")

        prediction_button = ctk.CTkButton(
            self.info_frame, text="Output Prediction", font=("Arial", 16, "bold"),
            width=30, height=30, command=self.prediction_load_model)
        prediction_button.grid(row=4, column=0,columnspan=2, padx=(740,0), pady=(0,20), sticky="w")

        self.app.v.geometry("1000x430+200+0")
 
    def prediction_load_model(self):
       
        if self.output_column and self.input_column :
            try:
                input_value = float(self.prediction_input.get())  # Ensure you have a field to get this input
                prediction = self.model.predict([[input_value]])  # Make sure the model is available
                prediction_label = ctk.CTkLabel(self.info_frame , text =f"Estimate calculated on the input value provided ( {self.input_column} :{input_value} )          <{self.output_column}> = {prediction[0]:.2f} ",
                                                    font=("Arial", 14, 'bold'), text_color="white")
                prediction_label.grid(row=5, column=0,columnspan=2, padx=(80,0), pady=(0,30), sticky="w")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number to make the prediction.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred during prediction: {e}")
        else:
                messagebox.showerror("Error", "No se pudo obtener el modelo o las columnas del archivo.")
    

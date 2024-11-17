
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
                    self.formula = data.get("formula", "Not avalable")
                    self.r_squared = data.get("r_squared", "Not avalable")
                    self.mse = data.get("mse", "Not avalable")
                    self.description = data.get("description", "Not avalable")
            
                self.app.v.grid_columnconfigure(0, weight=1, uniform="column")
                self.app.v.grid_columnconfigure(1, weight=0, uniform="column2")
               
                if self.app.modeling.graphic_frame is not None:
                    self.app.modeling.graphic_frame.grid_forget()                     
                if self.app.selection_frame is not None:
                    self.app.selection_frame.grid_forget()
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
        # Create a new frame for displaying the model information
        self.app.button_frame.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        self.info_frame = ctk.CTkFrame(self.app.v)
        self.info_frame.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        formula_label = ctk.CTkLabel(self.info_frame, text=f"Fórmula: {self.formula}\nR²: {self.r_squared:.4f} MSE: {self.mse:.4f}", font=("Arial", 12, 'bold'), text_color="white")
        formula_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        # Prediction button
        prediction2_button = ctk.CTkButton(
            self.info_frame, text="Prediction", font=("Arial", 18, "bold"),
            width=30, height=30, command=self.prediction_load_model)
        prediction2_button.grid(row=7, column=0, padx=10, pady=5, sticky="w")

        # Display description
        
        if self.description == "Write the model description here...":
            self.description = "Not avaliable"
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
            try:
                input_value = float(self.prediction_input.get())  # Ensure you have a field to get this input
                prediction = self.model_load.predict([[input_value]])  # Make sure the model is available
                prediction_label = ctk.CTkLabel(self.info_frame , text =f"Estimate calculated on the input value provided ( {self.app.selected_input_column} :{input_value} )\n<{self.app.selected_output_column}> = {prediction[0]:.2f} ",
                                                    font=("Arial", 14, 'bold'), text_color="white")
                prediction_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number to make the prediction.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred during prediction: {e}")
        else:
                messagebox.showerror("Error", "No se pudo obtener el modelo o las columnas del archivo.")
    

import pandas as pd

from tkinter import messagebox
from tkinter import messagebox, filedialog, Text,Tk
import customtkinter as ctk
from tkinter.scrolledtext import ScrolledText
from save_model import SaveModel
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from load_model import LoadModel

class Modeling:
    def __init__(self, app):
        self.app = app
        self.graphic_frame = None
        self.description_text = None
        self.model = None
        
        self.prediction_input_value = None
        self.output_column = None
        self.input_column = None

    def save_file(self):
        # Get the text from the description
        description = self.description_text.get("1.0", "end").strip()
        
        # Check if the description is empty or contains the default placeholder text
        if not description or description == "Write the model description here...":
            messagebox.showwarning("Warning", "You have not written anything in the description.")
            return
        
        # If there is a description, proceed to save the model
        saver = SaveModel(
            self.model,
            self.app.selected_input_column,
            self.app.selected_output_column,
            self.r_squared,
            self.mse,
            description
        )
        saver.save_model()


    def clear_placeholder(self, event):
        if self.description_text.get("1.0", "end-1c") == "Write the model description here...":
            self.description_text.delete("1.0", "end")

    def restore_placeholder(self, event):
        if not self.description_text.get("1.0", "end-1c").strip():
            self.description_text.insert("1.0", "Write the model description here...")

    def generate_model(self):
        messagebox.showinfo("Model Generation", f"Model generated with Input: {self.app.selected_input_column} and Output: {self.app.selected_output_column}")

        X = self.app.loaded_data[[self.app.selected_input_column]]
        y = self.app.loaded_data[self.app.selected_output_column]

        if not pd.api.types.is_numeric_dtype(self.app.loaded_data[self.app.selected_input_column]) or not pd.api.types.is_numeric_dtype(self.app.loaded_data[self.app.selected_output_column]):
            messagebox.showerror("Error", "The selected input or output column contains non-numeric data. Please select numeric columns.")
            return

        try:
            self.model = LinearRegression()
            self.model.fit(X, y)
            predictions = self.model.predict(X)

            self.r_squared = r2_score(y, predictions)
            self.mse = mean_squared_error(y, predictions)

            formula = f"{self.app.selected_output_column} = ({self.model.coef_[0]:.4f}) * ({self.app.selected_input_column}) + ({self.model.intercept_:.4f})"

            if self.graphic_frame is not None:
               self.graphic_frame.destroy()

            self.graphic_frame = ctk.CTkFrame(self.app.v)
            self.graphic_frame.grid(row=0, column=1, rowspan=8, padx=10, pady=10, sticky="nsew")
            
            
            

            model_info_label = ctk.CTkLabel(
                self.graphic_frame,
                text=f"Model Formula: {formula}\n        R²: {self.r_squared:.4f} MSE: {self.mse:.4f}",
                font=("Arial", 12, 'bold'),
                text_color="white")
            model_info_label.grid(row=0, column=0, columnspan=2, padx=40, pady=(20, 10), sticky="w")

            self.description_text = ScrolledText(self.graphic_frame, wrap="word", width=25, height=5, font=("Arial", 12))
            self.description_text.grid(row=2, column=0, columnspan=2, padx=40, pady=(10, 20), sticky="nsew")
            self.description_text.insert("1.0", "Write the model description here...")

            self.description_text.bind("<FocusIn>", self.clear_placeholder)
            self.description_text.bind("<FocusOut>", self.restore_placeholder)

            self.app.save_model_button = ctk.CTkButton(
            self.graphic_frame, text="Save Model", font=("Arial", 18, "bold"),
            width=30, height=30, command=self.save_file)
            self.app.save_model_button.grid(row=3, column=0, padx=40, pady=(5,10), sticky="ew")

        
            # un enter para escribir el input de la prediccion 
            self.prediction_input = ctk.CTkEntry(self.graphic_frame, width=30)
            self.prediction_input.grid(row=5, column=0,columnspan=2, padx=40, pady=(5, 10), sticky="ew")

            # boton de prediccion 
            self.prediction_button = ctk.CTkButton(
                self.graphic_frame, text="Actual Model Prediction ( enter input below )", font=("Arial", 18, "bold"),
                width=30, height=30, command=self.make_prediction)
            self.prediction_button.grid(row=4, column=0,padx=40,pady=(5 ,10), sticky="ew")
            
            # # boton de prediccion para otro modelo que no sea la actual 
            # self.prediction2_button = ctk.CTkButton(
            #     self.graphic_frame, text="Load another model Prediction", font=("Arial", 18, "bold"),
            #     width=30, height=30, command=self.prediction_load_model)
            # self.prediction2_button.grid(row=6, column=0,padx=40,pady=(5 ,10), sticky="ew")

            self.plot_regression_plot(X, y, predictions, self.graphic_frame)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating the model: {e}")


   
    def make_prediction(self):
                try:
                    # Captura el valor de entrada y lo convierte a tipo numérico
                    input_value = float(self.prediction_input.get())
                    
                    # Realiza la predicción usando el modelo
                    prediction = self.model.predict([[input_value]])
                    
                    # Guarda los valores de entrada y predicción en atributos de clase
                    self.prediction_input_value = input_value
                    self.prediction_result = prediction[0]
                    prediccion_label = ctk.CTkLabel(self.graphic_frame , text =f"El valor calculado basado en la entrada proporcionada {self.app.selected_input_column} :{input_value} es de -->  {prediction[0]:.2f} ({self.app.selected_output_column})",
                                                    font=("Arial", 12, 'bold'), text_color="white")
                    prediccion_label.grid(row=1, column=0, columnspan=2, padx=40, pady=(20, 10), sticky="w")


                except ValueError:
                    messagebox.showerror("Error", "Por favor ingrese un número válido para realizar la predicción.")
                except Exception as e:
                    messagebox.showerror("Error", f"Ocurrió un error al realizar la predicción: {e}")

    def plot_regression_plot(self, X, y, predictions, parent_frame):
        fig = self.create_regression_plot(X, y, predictions)
        self.embed_plot_in_frame(fig, parent_frame)

    def create_regression_plot(self, X, y, predictions):
        fig, ax = plt.subplots(figsize=(7, 4))  
        ax.scatter(X, y, color='blue', label='Actual Data')
        ax.plot(X, predictions, color='red', label='Regression Line')
        ax.set_title('Linear Regression', fontsize=10, color='black')
        ax.set_xlabel(self.app.selected_input_column, fontsize=10, color='black')
        ax.set_ylabel(self.app.selected_output_column, fontsize=10, color='black')
        ax.legend()
        return fig

    def embed_plot_in_frame(self, fig, frame):
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw() 
        canvas.get_tk_widget().grid(padx=40, pady=(20,10), sticky="nse")  
        plt.close(fig)

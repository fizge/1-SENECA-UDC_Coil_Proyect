import pandas as pd
from tkinter import messagebox
import customtkinter as ctk
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.scrolledtext import ScrolledText
from save_model import SaveModel
from tkinter import messagebox, filedialog
import pickle
from tkinter import filedialog, messagebox, Toplevel, Label, Text

class Modeling:
    def __init__(self, app):
        self.app = app
        self.graphic_frame = None
        self.description_text = None
        self.model = None
        self.model_info_label = None
        

    def save_file(self):
        description = self.description_text.get("1.0", "end").strip()
        if not description:
            messagebox.showwarning("Warning", "You have not written anything in the description.")
            return
        saver = SaveModel(self.model, self.app.selected_input_column, self.app.selected_output_column, self.r_squared, self.mse, description)
        saver.save_model()

########## solo he tocado este trozo de codigo 
    def load_model(self):
           
            file_path = filedialog.askopenfilename(filetypes=[("Model files", "*.pkl *.joblib")])
            if file_path:
                try:
                   
                    with open(file_path, "rb") as f:
                        model_data = pickle.load(f)
                    
                    
                    self.display_model_info(model_data)

                except (pickle.UnpicklingError, AttributeError, KeyError) as e:
                   
                    messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")

    def display_model_info(self, model_data):
            #nueva ventana para la info
            info_window = Toplevel()
            info_window.title("Información del Modelo")

            #FORMULA
            formula = model_data.get("formula", "No disponible")
            Label(info_window, text=f"Fórmula: {formula}").pack(anchor="w", padx=10, pady=5)

            # LOS COEFICIENTES
            coef = model_data.get("coefficients", [])
            coef_text = "\n".join([f"Coeficiente {i+1}: {c:.4f}" for i, c in enumerate(coef)])
            Label(info_window, text="Coeficientes:").pack(anchor="w", padx=10, pady=(10, 0))
            Label(info_window, text=coef_text).pack(anchor="w", padx=20, pady=5)

     
            intercept = model_data.get("intercept", "No disponible")
            Label(info_window, text=f"Intercepto: {intercept:.4f}").pack(anchor="w", padx=10, pady=5)

           
            input_column = model_data.get("input_column", "No disponible")
            output_column = model_data.get("output_column", "No disponible")
            Label(info_window, text=f"Columna de entrada: {input_column}").pack(anchor="w", padx=10, pady=5)
            Label(info_window, text=f"Columna de salida: {output_column}").pack(anchor="w", padx=10, pady=5)

            
            r_squared = model_data.get("r_squared", "No disponible")
            mse = model_data.get("mse", "No disponible")
            Label(info_window, text=f"R²: {r_squared}").pack(anchor="w", padx=10, pady=5)
            Label(info_window, text=f"MSE: {mse}").pack(anchor="w", padx=10, pady=5)

            
            description = model_data.get("description", "No disponible")
            if description == "Write the model description here...":
                description = "No disponible"
            Label(info_window, text="Descripción:").pack(anchor="w", padx=10, pady=(10, 0))
            description_text = Text(info_window, height=5, width=50, wrap="word")
            description_text.insert("1.0", description)
            description_text.config(state="disabled") 
            description_text.pack(anchor="w", padx=10, pady=5)

           
            info_window.geometry("500x500")
#####   ######


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
            messagebox.showerror("Error", "Selected input or output column contains non-numeric data. Please select numeric columns.")
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

            formula_label = ctk.CTkLabel(self.graphic_frame, text=f"Model Formula:\n\n{formula}", font=("Arial", 14, 'bold'), text_color="white")
            formula_label.grid(row=0, column=0, columnspan=3, padx=10, pady=(20, 10), sticky="w")

            r_squared_label = ctk.CTkLabel(self.graphic_frame, text=f"R²: {self.r_squared:.4f}", font=("Arial", 12, 'bold'), text_color="white")
            r_squared_label.grid(row=1, column=0, padx=(10, 20), pady=(5, 0), sticky="w")

            mse_label = ctk.CTkLabel(self.graphic_frame, text=f"MSE: {self.mse:.4f}", font=("Arial", 12, 'bold'), text_color="white")
            mse_label.grid(row=2, column=0, padx=10, pady=(10, 20), sticky="w")

            self.description_text = ScrolledText(self.graphic_frame, wrap="word", width=25, height=5, font=("Arial", 12))
            self.description_text.grid(row=2, column=0, columnspan=3, padx=10, pady=(10, 20), sticky="ew")
            self.description_text.insert("1.0", "Write the model description here...")

            self.description_text.bind("<FocusIn>", self.clear_placeholder)
            self.description_text.bind("<FocusOut>", self.restore_placeholder)

            self.app.save_model_button = ctk.CTkButton(
                self.graphic_frame, text="Save Model", font=("Arial", 20, "bold"),
                width=140, height=40, command=self.save_file
            )
            self.app.save_model_button.grid(row=3, column=0, columnspan=3, padx=10, pady=(10, 0), sticky="nse")

            self.plot_regression_plot(X, y, predictions, self.graphic_frame)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating the model: {e}")

    def plot_regression_plot(self, X, y, predictions, parent_frame):
        fig = self.create_regression_plot(X, y, predictions)
        self.embed_plot_in_frame(fig, parent_frame)

    def create_regression_plot(self, X, y, predictions):
        fig, ax = plt.subplots(figsize=(6, 4))  # Adjusted size for better visibility
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
        canvas.get_tk_widget().grid(padx=20, pady=20, sticky="nse")  # Removed fill option
        plt.close(fig)

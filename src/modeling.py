import pandas as pd
from tkinter import messagebox
from tkinter import messagebox
import customtkinter as ctk
from tkinter.scrolledtext import ScrolledText
from save_model import SaveModel
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Modeling:
    def __init__(self, app):
        self.app = app
        self.graphic_frame = None
        self.description_text = None
        self.model = None
        self.r_squared = None
        self.mse = None
        self.prediction_label = None
        self.prediction_input = None
        self.prediction_button = None
        self.prediction_input_value = None
        self.output_column = None
        self.input_column = None
        self.save_model_button = None

    def save_file(self):
    
        description = self.description_text.get("1.0", "end").strip()

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
            if len(formula) > 47:
                formula = f"{self.app.selected_output_column} = \n({self.model.coef_[0]:.4f}) * ({self.app.selected_input_column}) + ({self.model.intercept_:.4f})"
            if self.graphic_frame is not None:
               self.graphic_frame.destroy()

            self.graphic_frame = ctk.CTkFrame(self.app.v)
            self.graphic_frame.grid(row=0, column=1, rowspan=8, padx=10, pady=10, sticky="nsew")
            
            self.save_model_button = ctk.CTkButton(
            self.graphic_frame, text="Save Model", font=("Arial", 18, "bold"),
            width=200, height=30, command=self.save_file)
            self.save_model_button.grid(row=0, column=0, padx=250, pady=(10,5), sticky="w")

            labels_frame = ctk.CTkFrame(self.graphic_frame,fg_color="#242424", border_width=3,border_color='white', corner_radius=10)  
            labels_frame.grid(row=1, column=0,pady=5, padx=40, sticky="nw")      

            formula_label = ctk.CTkLabel(labels_frame, text=f"Linear Regresion Ecuation:", font=("Arial", 14, 'bold'), text_color="white")
            formula_label.grid(row=0, column=0, padx=10, pady=(5,0), sticky="w")
            formula2_label = ctk.CTkLabel(labels_frame, text=f"{formula}", font=("Arial", 12, 'bold'), text_color="white")
            
            formula2_label.grid(row=1, column=0, padx=10, pady=0, sticky="w")
            r2_label = ctk.CTkLabel(labels_frame, text=f"R²: {self.r_squared:.4f}", font=("Arial", 12, 'bold'), text_color="white")
            r2_label.grid(row=2, column=0, padx=10, pady=0, sticky="w")
            mse_label = ctk.CTkLabel(labels_frame, text=f"MSE: {self.mse:.4f}", font=("Arial", 12, 'bold'), text_color="white")
            mse_label.grid(row=3, column=0, padx=10, pady=(0,5), sticky="w")


            self.description_text = ctk.CTkTextbox(self.graphic_frame, wrap="word",width=270,height=120, fg_color="#242424", font=("Arial", 12),border_width=3,border_color='white', corner_radius=10)
            self.description_text.grid(row=1, column=0, padx=(260,0), pady=5, sticky="n")
            self.description_text.insert("1.0", "Write the model description here...")

            self.description_text.bind("<FocusIn>", self.clear_placeholder)
            self.description_text.bind("<FocusOut>", self.restore_placeholder)

            self.prediction_label = ctk.CTkLabel(self.graphic_frame, text=f"Input value:", font=("Arial", 15, 'bold'), text_color="white")
            self.prediction_label.grid(row=2, column=0, padx=40, pady=5, sticky="w")

            self.prediction_input = ctk.CTkEntry(self.graphic_frame, width=300)
            self.prediction_input.grid(row=2, column=0, padx=(140,0), pady=5, sticky="w")

            self.prediction_button = ctk.CTkButton(
                self.graphic_frame, text="Output Prediction", font=("Arial", 18, "bold"),
                width=30, height=30, command=self.make_prediction)
            self.prediction_button.grid(row=2, column=0, padx=(470,0),pady=5, sticky="w")
            self.plot_regression_plot(X, y, predictions, self.graphic_frame)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating the model: {e}")



   
    def make_prediction(self):
                try:

                    input_value = float(self.prediction_input.get())
                    prediction = self.model.predict([[input_value]])  
                    self.prediction_input_value = input_value
                    prediction_label = ctk.CTkLabel(self.graphic_frame , text =f"Estimate calculated on the input value provided ( {self.app.selected_input_column} :{input_value} ) <{self.app.selected_output_column}> = {prediction[0]:.2f} ",
                                                    font=("Arial", 12, 'bold'), text_color="white")
                    prediction_label.grid(row=3, column=0, padx=40, pady=(0, 5), sticky="w")

                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid number to make the prediction.")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred during prediction: {e}")


    def plot_regression_plot(self, X, y, predictions, parent_frame):
        fig = self.create_regression_plot(X, y, predictions)
        self.embed_plot_in_frame(fig, parent_frame)

    def create_regression_plot(self, X, y, predictions):
        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor('#2b2b2b')
        ax.set_facecolor('#2b2b2b')
        ax.tick_params(axis='both', colors='white')
        ax.set_title('Linear Regression', fontsize=10, color='white')
        ax.set_xlabel(self.app.selected_input_column, fontsize=10, color='white')
        ax.set_ylabel(self.app.selected_output_column, fontsize=10, color='white')
        ax.scatter(X, y, color='#1465B1', label='Actual Data')
        ax.plot(X, predictions, color='red', label='Regression Line')
        ax.legend(facecolor='#2b2b2b', edgecolor='white', fontsize=10, loc='best', frameon=True, labelcolor='white')
        ax.grid(True, color='gray', linestyle='-', linewidth=0.5)
        for spine in ax.spines.values():
            spine.set_edgecolor('white')
        return fig

    def embed_plot_in_frame(self, fig, frame):
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=0, padx=50, pady=(15, 10), sticky="nse")
        plt.close(fig)

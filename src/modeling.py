import pandas as pd
from tkinter import messagebox
import customtkinter as ctk
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pickle
from tkinter import filedialog

class Modeling:
    def __init__(self, app):
        self.app = app
        self.graphic_frame = None

    def generate_model(self):
        messagebox.showinfo("Model Generation", f"Model generated with Input: {self.app.selected_input_column} and Output: {self.app.selected_output_column}")

        X = self.app.loaded_data[[self.app.selected_input_column]]
        y = self.app.loaded_data[self.app.selected_output_column]

        if not pd.api.types.is_numeric_dtype(self.app.loaded_data[self.app.selected_input_column]) or not pd.api.types.is_numeric_dtype(self.app.loaded_data[self.app.selected_output_column]):
            messagebox.showerror("Error", "Selected input or output column contains non-numeric data. Please select numeric columns.")
            return

        try:
            model = LinearRegression()
            model.fit(X, y)
            predictions = model.predict(X)

            r_squared = r2_score(y, predictions)
            mse = mean_squared_error(y, predictions)

            self.model = model
            self.r_squared = r_squared
            self.mse = mse

            formula = f"{self.app.selected_output_column} = ({model.coef_[0]:.4f}) * ({self.app.selected_input_column}) + ({model.intercept_:.4f})"

            if self.graphic_frame is not None:
                self.graphic_frame.destroy()

            self.graphic_frame = ctk.CTkFrame(self.app.v)
            self.graphic_frame.grid(row=0, column=1, rowspan=8, padx=20, pady=20, sticky="nsew")

            formula_label = ctk.CTkLabel(self.graphic_frame, text=f"Model Formula:\n\n{formula}", font=("Arial", 18, 'bold'), text_color="white")
            formula_label.pack(pady=30, padx=10, anchor="w")

            r_squared_label = ctk.CTkLabel(self.graphic_frame, text=f"R²: {r_squared:.4f}", font=("Arial", 14, 'bold'), text_color="white")
            r_squared_label.pack(pady=5, padx=10, anchor="w")

            mse_label = ctk.CTkLabel(self.graphic_frame, text=f"MSE: {mse:.4f}", font=("Arial", 14, 'bold'), text_color="white")
            mse_label.pack(pady=5, padx=10, anchor="w")

            self.plot_regression_plot(X, y, predictions, self.graphic_frame)
            
            # Create and display the 'Save Model' button after model generation
            self.app.save_model_button = ctk.CTkButton(
                self.app.button_frame, text="Save Model", font=("Arial", 20, "bold"),
                width=140, height=40, command=self.save_model
            )
            self.app.save_model_button.grid(row=0, column=3, padx=(10, 40), pady=10, sticky="e")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating the model: {e}")

    def plot_regression_plot(self, X, y, predictions, parent_frame):
        fig = self.create_regression_plot(X, y, predictions)
        self.embed_plot_in_frame(fig, parent_frame)

    def create_regression_plot(self, X, y, predictions):
        fig, ax = plt.subplots(figsize=(8, 7))
        ax.scatter(X, y, color='blue', label='Actual Data')
        ax.plot(X, predictions, color='red', label='Regression Line')
        ax.set_title('Linear Regression', fontsize=14, color='white')
        ax.set_xlabel(self.app.selected_input_column, fontsize=12, color='white')
        ax.set_ylabel(self.app.selected_output_column, fontsize=12, color='white')
        ax.legend()
        return fig

    def embed_plot_in_frame(self, fig, frame):
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=10, pady=10, fill="both", expand=True)
        plt.close(fig)

    def save_model(self):
        if not hasattr(self, 'model') or self.app.selected_input_column is None or self.app.selected_output_column is None:
            messagebox.showerror("Error", "No model available to save. Generate a model first.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pkl",
            filetypes=[("Pickle files", "*.pkl"), ("Joblib files", "*.joblib")]
        )

        if not file_path:
            return

        model_data = {
            "formula": f"{self.app.selected_output_column} = ({self.model.coef_[0]:.4f}) * ({self.app.selected_input_column}) + ({self.model.intercept_:.4f})",
            "coefficients": self.model.coef_,
            "intercept": self.model.intercept_,
            "input_column": self.app.selected_input_column,
            "output_column": self.app.selected_output_column,
            "r_squared": self.r_squared,
            "mse": self.mse,
            "description": "User-defined model details and metrics"
        }

        try:
            with open(file_path, 'wb') as file:
                pickle.dump(model_data, file)
            messagebox.showinfo("Success", f"Model saved successfully to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save the model: {e}")

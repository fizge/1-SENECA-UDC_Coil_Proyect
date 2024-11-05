import pandas as pd
from tkinter import messagebox
import customtkinter as ctk
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.scrolledtext import ScrolledText
from save_model import SaveModel

class Modeling:
    def __init__(self, app):
        self.app = app
        self.graphic_frame = None
        self.description_text = None
        self.model = None

    def save_file(self):
        description = self.description_text.get("1.0", "end").strip()
        if not description:
            messagebox.showwarning("Warning", "You have not written anything in the description.")
            return
        saver = SaveModel(self.model, self.app.selected_input_column, self.app.selected_output_column, self.r_squared, self.mse, description)
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

            formula_label = ctk.CTkLabel(self.graphic_frame, text=f"Model Formula:\n\n{formula}", font=("Arial", 10, 'bold'), text_color="blue")
            formula_label.pack(pady=30, padx=10, anchor="w")

            r_squared_label = ctk.CTkLabel(self.graphic_frame, text=f"R²: {self.r_squared:.4f}", font=("Arial", 10, 'bold'), text_color="green")
            r_squared_label.pack(pady=5, padx=10, anchor="w")

            mse_label = ctk.CTkLabel(self.graphic_frame, text=f"MSE: {self.mse:.4f}", font=("Arial", 10, 'bold'), text_color="red")
            mse_label.pack(pady=5, padx=10, anchor="w")

            self.description_text = ScrolledText(self.graphic_frame, wrap="word", width=10, height=10)
            self.description_text.pack(expand=True, fill="both", padx=10, pady=10)
            self.description_text.insert("1.0", "Write the model description here...")

            self.description_text.bind("<FocusIn>", self.clear_placeholder)
            self.description_text.bind("<FocusOut>", self.restore_placeholder)

            self.app.save_model_button = ctk.CTkButton(
                self.app.button_frame, text="Save Model", font=("Arial", 20, "bold"),
                width=140, height=40, command=self.save_file
            )
            self.app.save_model_button.grid(row=0, column=3, padx=(10, 40), pady=10, sticky="e")

            self.plot_regression_plot(X, y, predictions, self.graphic_frame)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating the model: {e}")

    def plot_regression_plot(self, X, y, predictions, parent_frame):
        fig = self.create_regression_plot(X, y, predictions)
        self.embed_plot_in_frame(fig, parent_frame)

    def create_regression_plot(self, X, y, predictions):
        fig, ax = plt.subplots(figsize=(2, 2))
        ax.scatter(X, y, color='blue', label='Actual Data')
        ax.plot(X, predictions, color='red', label='Regression Line')
        ax.set_title('Linear Regression', fontsize=10, color='black')
        ax.set_xlabel(self.app.selected_input_column, fontsize=10, color='black')
        ax.set_ylabel(self.app.selected_output_column, fontsize=10, color='black')
        ax.legend()
        return fig

    def embed_plot_in_frame(self, fig, frame):
        fig.set_size_inches(7, 6)
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=20, pady=20, fill="both", expand=True)
        plt.close(fig)

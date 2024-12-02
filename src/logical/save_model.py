import pickle
from tkinter import messagebox, filedialog


class SavedModel:
    """
    Clase para gestionar el guardado de modelos entrenados con sus atributos, métricas y descripción.
    """

    def __init__(self, model, input_column, output_column, r_squared, mse, description):
        self.model = model
        self.input_column = input_column
        self.output_column = output_column
        self.r_squared = r_squared
        self.mse = mse
        self.description = description

    def save_model(self):
        if self.model is None or self.input_column is None or self.output_column is None:
            messagebox.showerror(
                "Error", "No model available to save. Generate a model first.")
            return

        if self.description == "Write the model description here...":
            self.description = ""

        if not self.description or self.description == "":
            messagebox.showwarning(
                "Warning", "You have not written anything in the description.")

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pkl",
            filetypes=[("Pickle files", "*.pkl"), ("Joblib files", "*.joblib")]
        )

        if not file_path:
            return

        formula = f"{self.output_column} = ({self.model.coef_[0]:.4f}) * ({self.input_column}) + ({self.model.intercept_:.4f})"
        if len(formula) > 47:
            formula = f"{self.output_column} = \n({self.model.coef_[0]:.4f}) * ({self.input_column}) + ({self.model.intercept_:.4f})"

        self.model_data = {
            "model": self.model,
            "formula": formula,
            "coefficients": self.model.coef_,
            "intercept": self.model.intercept_,
            "input_column": self.input_column,
            "output_column": self.output_column,
            "r_squared": self.r_squared,
            "mse": self.mse,
            "description": self.description,
        }

        try:
            with open(file_path, 'wb') as file:
                pickle.dump(self.model_data, file)
            # Ajuste del mensaje para incluir el salto de línea (\n)
            messagebox.showinfo(
                "Success", f"Model saved successfully to:{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save the model: {e}")

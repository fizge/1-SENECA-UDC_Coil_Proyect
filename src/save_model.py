import pickle
from tkinter import messagebox, filedialog

class SaveModel:
    def __init__(self, model, input_column, output_column, r_squared, mse, description):
        self.model = model
        self.input_column = input_column
        self.output_column = output_column
        self.r_squared = r_squared
        self.mse = mse
        self.description = description
        
    def save_model(self):
        if self.model is None or self.input_column is None or self.output_column is None:
            messagebox.showerror("Error", "No model available to save. Generate a model first.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pkl",
            filetypes=[("Pickle files", "*.pkl"), ("Joblib files", "*.joblib")]
        )

        if not file_path:
            return

        self.model_data = {
            "model": self.model,
            "formula": f"{self.output_column} = ({self.model.coef_[0]:.4f}) * ({self.input_column}) + ({self.model.intercept_:.4f})",
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
            messagebox.showinfo("Success", f"Model saved successfully to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save the model: {e}")


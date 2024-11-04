import pickle
from tkinter import messagebox, filedialog
import customtkinter as ctk

def save_model_to_file(modeling_instance, description):

    if modeling_instance.model is None:
        messagebox.showerror("Error", "No model available to save. Generate a model first.")
        return

    if description is None or description.strip() == "":
        messagebox.showerror("Error", "Model description cannot be empty.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".pkl",
        filetypes=[("Pickle files", "*.pkl"), ("Joblib files", "*.joblib")]
    )

    if not file_path:
        return

    model_data = {
        "formula": f"{modeling_instance.app.selected_output_column} = ({modeling_instance.model.coef_[0]:.4f}) * ({modeling_instance.app.selected_input_column}) + ({modeling_instance.model.intercept_:.4f})",
        "coefficients": modeling_instance.model.coef_,
        "intercept": modeling_instance.model.intercept_,
        "input_column": modeling_instance.app.selected_input_column,
        "output_column": modeling_instance.app.selected_output_column,
        "r_squared": modeling_instance.r_squared,
        "mse": modeling_instance.mse,
        "description": description
    }

    try:
        with open(file_path, 'wb') as file:
            pickle.dump(model_data, file)
        messagebox.showinfo("Success", f"Model saved successfully to {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save the model: {e}")

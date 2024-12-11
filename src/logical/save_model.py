import pickle
from tkinter import messagebox, filedialog


class SavedModel:
    """
    A class to handle the saving of trained linear regression models along with their metadata.

    This class facilitates:
    - Checking model completeness before saving.
    - Generating a file dialog for saving the model.
    - Packaging model information and metadata into a dictionary for serialization.
    - Saving the model and metadata using the `pickle` library.
    """

    def __init__(self, model, input_column, output_column, r_squared, mse, description):
        """
        Initializes the SavedModel class.

        :param model: The trained linear regression model.
        :param input_column: The name of the input column used for the model.
        :param output_column: The name of the output column used for the model.
        :param r_squared: R² metric of the model.
        :param mse: Mean Squared Error of the model.
        :param description: Description of the model provided by the user.
        """
        self.model = model
        self.input_column = input_column
        self.output_column = output_column
        self.r_squared = r_squared
        self.mse = mse
        self.description = description

    def save_model(self):
        """
        Saves the trained model along with its metadata to a file.

        This method:
        - Validates the completeness of the model and its metadata.
        - Opens a file dialog for the user to specify the save location.
        - Serializes the model and metadata into a file using `pickle`.

        Shows appropriate error or success messages during the process.
        """
        # Check if the model or required attributes are missing
        if self.model is None or self.input_column is None or self.output_column is None:
            messagebox.showerror(
                "Error", "No model available to save. Generate a model first.")
            return

        # Handle default placeholder description
        if self.description == "Write the model description here...":
            self.description = ""

        # Warn if the description is empty
        if not self.description or self.description == "":
            messagebox.showwarning(
                "Warning", "You have not written anything in the description.")

        # Open a file dialog for saving the model
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pkl",
            filetypes=[("Pickle files", "*.pkl"), ("Joblib files", "*.joblib")]
        )

        # Exit if no file path is selected
        if not file_path:
            return

        # Generate a formula string for the regression equation
        formula = f"{self.output_column} = ({self.model.coef_[0]:.4f}) * ({self.input_column}) + ({self.model.intercept_:.4f})"
        if len(formula) > 47:  # Handle long formulas with line breaks
            formula = f"{self.output_column} = \n({self.model.coef_[0]:.4f}) * ({self.input_column}) + ({self.model.intercept_:.4f})"

        # Prepare the data to be saved
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

        # Save the model data using pickle
        try:
            with open(file_path, 'wb') as file:
                pickle.dump(self.model_data, file)
            messagebox.showinfo(
                "Success", f"Model saved successfully to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save the model: {e}")

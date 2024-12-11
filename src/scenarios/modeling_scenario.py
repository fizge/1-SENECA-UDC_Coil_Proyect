import pandas as pd
from tkinter import messagebox
from tkinter import messagebox
import customtkinter as ctk
from logical.save_model import SavedModel
from utils.charging_bar import ChargingWindow
from utils.placeholder import PlaceholderText
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class Modeling:
    """
    A class for managing the generation, visualization, and interaction with linear regression models.

    This class is responsible for:
    - Generating a linear regression model from user-selected data.
    - Displaying the model's equation, metrics (R² and MSE), and description.
    - Providing functionality to make predictions based on the model.
    - Saving the model along with its metadata.
    - Visualizing the model with matplotlib.
    """

    def __init__(self, app):
        """
        Initializes the `Modeling` class.

        :param app: Reference to the main application instance.
        """
        self.app = app
        self.graphic_frame = None  # Frame to display model information and plots.
        self.description_text = None  # Textbox for model description.
        self.model = None  # The generated linear regression model.
        self.r_squared = None  # R² metric of the model.
        self.mse = None  # Mean Squared Error of the model.
        self.prediction_label = None  # Label for prediction input.
        self.prediction_res_label = None  # Label to display prediction results.
        self.prediction_input = None  # Input field for prediction.
        self.prediction_button = None  # Button to make a prediction.
        self.prediction_input_value = None  # Value entered for prediction.
        self.output_column = None  # Output column (target) used for the model.
        self.input_column = None  # Input column (feature) used for the model.
        self.save_model_button = None  # Button to save the model.

    def save_file(self):
        """
        Saves the current model and its metadata using the `SavedModel` class.

        If the model has not been generated or required attributes are missing, 
        an error message will be displayed to the user.
        """
        description = self.description_text.get("1.0", "end").strip()

        saving = SavedModel(
            self.model,
            self.app.preselection.selected_input_column,
            self.app.preselection.selected_output_column,
            self.r_squared,
            self.mse,
            description
        )
        saving.save_model()

    def generate_model(self):
        """
        Generates a linear regression model from the selected input and output columns.

        This method performs the following:
        - Validates that the selected columns contain numeric data.
        - Fits a `LinearRegression` model using the selected columns.
        - Calculates R² and MSE metrics for the model.
        - Displays the model equation, metrics, and description in the UI.
        - Allows the user to make predictions and save the model.

        Raises:
            ValueError: If the selected columns are not numeric.
            Exception: For other errors during model generation.
        """
        charging = ChargingWindow(self.app)
        charging.bar()

        X = self.app.preselection.loaded_data[[self.app.preselection.selected_input_column]]
        y = self.app.preselection.loaded_data[self.app.preselection.selected_output_column]

        try:
            # Validate that the selected columns are numeric
            if not pd.api.types.is_numeric_dtype(self.app.preselection.loaded_data[self.app.preselection.selected_input_column]) or not pd.api.types.is_numeric_dtype(self.app.preselection.loaded_data[self.app.preselection.selected_output_column]):
                raise ValueError(
                    "The selected input or output column contains non-numeric data. Please select numeric columns.")

            # Generate the model
            self.model = LinearRegression()
            self.model.fit(X, y)
            predictions = self.model.predict(X)

            # Calculate metrics
            self.r_squared = r2_score(y, predictions)
            self.mse = mean_squared_error(y, predictions)

            # Format the model formula
            formula = f"{self.app.preselection.selected_output_column} = ({self.model.coef_[0]:.4f}) * ({self.app.preselection.selected_input_column}) + ({self.model.intercept_:.4f})"
            if len(formula) > 47:
                formula = f"{self.app.preselection.selected_output_column} = \n({self.model.coef_[0]:.4f}) * ({self.app.preselection.selected_input_column}) + ({self.model.intercept_:.4f})"

            # Reset the graphic frame if it already exists
            if self.graphic_frame is not None:
                self.graphic_frame.destroy()

            messagebox.showinfo(
                "Model Generation", f"Model generated with Input: {self.app.preselection.selected_input_column} and Output: {self.app.preselection.selected_output_column}")

            # Create and display the UI for the model
            self.graphic_frame = ctk.CTkFrame(self.app.v, fg_color='#242424')
            self.graphic_frame.grid(row=0, column=2, rowspan=8, padx=10, pady=10, sticky="nsew")

            info_label = ctk.CTkLabel(self.graphic_frame, text='Model Information:\t\t\tDescription:', font=(
                "Arial", 18, 'bold'), text_color="white")
            info_label.grid(row=0, column=0, padx=40, pady=(20, 0), sticky="W")

            labels_frame = ctk.CTkFrame(
                self.graphic_frame, fg_color="#242424", border_width=3, border_color='white', corner_radius=10)
            labels_frame.grid(row=1, column=0, pady=5, padx=40, sticky="nw")

            formula_label = ctk.CTkLabel(labels_frame, text=f"Linear Regression Equation:", font=(
                "Arial", 14, 'bold'), text_color="white")
            formula_label.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")
            formula2_label = ctk.CTkLabel(labels_frame, text=f"{formula}", font=(
                "Arial", 12, 'bold'), text_color="white")
            formula2_label.grid(row=1, column=0, padx=10, pady=0, sticky="w")

            r2_label = ctk.CTkLabel(labels_frame, text=f"R²: {self.r_squared:.4f}", font=(
                "Arial", 12, 'bold'), text_color="white")
            r2_label.grid(row=2, column=0, padx=10, pady=0, sticky="w")
            mse_label = ctk.CTkLabel(labels_frame, text=f"MSE: {self.mse:.4f}", font=(
                "Arial", 12, 'bold'), text_color="white")
            mse_label.grid(row=3, column=0, padx=10, pady=(0, 5), sticky="w")

            self.description_text = ctk.CTkTextbox(self.graphic_frame, wrap="word", width=270, height=120, fg_color="#242424", font=(
                "Arial", 12), border_width=3, border_color='white', corner_radius=10)
            self.description_text.grid(row=1, column=0, padx=(260, 0), pady=5, sticky="n")
            placeholder = PlaceholderText(self.description_text, "Write the model description here...")

            self.save_model_button = ctk.CTkButton(self.graphic_frame, text="Save Model", font=(
                "Arial", 18, "bold"), width=200, height=40, corner_radius=30, command=self.save_file)
            self.save_model_button.grid(row=2, column=0, padx=250, pady=(20, 5), sticky="w")

            title_prediction_label = ctk.CTkLabel(self.graphic_frame, text=f'{self.app.preselection.selected_output_column.capitalize()} prediction for a {self.app.preselection.selected_input_column} value:', font=(
                "Arial", 14, 'bold'), text_color="white")
            title_prediction_label.grid(row=4, column=0, padx=40, pady=(15, 5), sticky="w")

            self.prediction_label = ctk.CTkLabel(self.graphic_frame, text=f"{self.app.preselection.selected_input_column}:", font=(
                "Arial", 15, 'bold'), text_color="white")
            self.prediction_label.grid(row=5, column=0, padx=40, pady=15, sticky="w")

            self.prediction_input = ctk.CTkEntry(self.graphic_frame, width=300)
            self.prediction_input.grid(row=5, column=0, padx=(40, 0), pady=(5, 15), sticky="w")
            placeholder = PlaceholderText(self.prediction_input, f"Write here a {self.app.preselection.selected_input_column} value")

            self.prediction_button = ctk.CTkButton(self.graphic_frame, text="Predict", font=(
                "Arial", 18, "bold"), width=90, height=40, corner_radius=30, command=self.make_prediction)
            self.prediction_button.grid(row=5, column=0, padx=(360, 0), pady=(5, 15), sticky="w")

            self.plot_regression_plot(X, y, predictions, self.graphic_frame)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating the model: {e}")

        charging.close_bar()

    def make_prediction(self):
        """
        Makes a prediction using the generated model for a user-provided input.

        Validates the input, computes the prediction, and displays the result. 
        Handles errors related to invalid input or failed predictions.
        """
        try:
            input_value = float(self.prediction_input.get())
            prediction = self.model.predict([[input_value]])
            self.prediction_input_value = input_value

            if self.prediction_res_label is not None:
                self.prediction_res_label.destroy()

            self.prediction_res_label = ctk.CTkLabel(self.graphic_frame, text=f"<{self.app.preselection.selected_output_column}> = {prediction[0]:.2f} ",
                                                     font=("Arial", 17, 'bold'), text_color="white")
            self.prediction_res_label.grid(row=6, column=0, padx=40, pady=(0, 5), sticky="w")

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number to make the prediction.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during prediction: {e}")

    def plot_regression_plot(self, X, y, predictions, parent_frame):
        """
        Creates and embeds a regression plot in the provided frame.

        :param X: Input data used for the regression.
        :param y: Output data used for the regression.
        :param predictions: Predictions made by the model.
        :param parent_frame: Frame where the plot will be embedded.
        """
        fig = self.create_regression_plot(X, y, predictions)
        self.embed_plot_in_frame(fig, parent_frame)

    def create_regression_plot(self, X, y, predictions):
        """
        Creates a matplotlib plot showing the regression line and actual data points.

        :param X: Input data used for the regression.
        :param y: Output data used for the regression.
        :param predictions: Predictions made by the model.
        :return: A matplotlib figure object.
        """
        fig, ax = plt.subplots(figsize=(7, 5))
        fig.patch.set_facecolor('#242424')
        ax.set_facecolor('#242424')
        ax.tick_params(axis='both', colors='white')
        ax.set_title('Linear Regression', fontsize=10, color='white')
        ax.set_xlabel(self.app.preselection.selected_input_column, fontsize=10, color='white')
        ax.set_ylabel(self.app.preselection.selected_output_column, fontsize=10, color='white')
        ax.scatter(X, y, color='#1465B1', label='Actual Data')
        ax.plot(X, predictions, color='red', label='Regression Line')
        ax.legend(facecolor='#2b2b2b', edgecolor='white', fontsize=10,
                  loc='best', frameon=True, labelcolor='white')
        ax.grid(True, color='gray', linestyle='-', linewidth=0.5)
        for spine in ax.spines.values():
            spine.set_edgecolor('white')
        plt.tight_layout()
        return fig

    def embed_plot_in_frame(self, fig, frame):
        """
        Embeds a matplotlib figure in a Tkinter frame.

        :param fig: Matplotlib figure to embed.
        :param frame: Frame where the figure will be displayed.
        """
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=3, column=0, padx=50, pady=(15, 10), sticky="nsew")
        plt.close(fig)

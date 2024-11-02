import pandas as pd
from tkinter import messagebox
import customtkinter as ctk
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Modeling:
    """
    A class responsible for building and displaying a linear regression model within a Tkinter GUI application.
    
    Attributes:
    ----------
    app : object
        The main application instance that holds the GUI components and data.
    graphic_frame : ctk.CTkFrame
        The frame where the model's results and regression plot are displayed.
    """

    def __init__(self, app):
        """
        Initializes the Modeling class with the given application instance.
        
        Parameters:
        ----------
        app : object
            The main application instance containing the loaded data and GUI components.
        """
        self.app = app
        self.graphic_frame = None

    def generate_model(self):
        """
        Generates a linear regression model using the selected input and output columns from the loaded data.
        
        Displays:
        --------
        - A message box indicating the start of model generation.
        - An error message if non-numeric columns are selected.
        - The formula, R² score, and MSE of the trained model within a custom Tkinter frame.
        """
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

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating the model: {e}")

    def plot_regression_plot(self, X, y, predictions, parent_frame):
        """
        Creates a regression plot and embeds it into the specified parent frame.

        Parameters:
        ----------
        X : pd.DataFrame
            The input features used in the regression model.
        y : pd.Series
            The target output used in the regression model.
        predictions : np.ndarray
            The predicted values from the regression model.
        parent_frame : ctk.CTkFrame
            The frame where the plot will be embedded.
        """
        fig = self.create_regression_plot(X, y, predictions)
        self.embed_plot_in_frame(fig, parent_frame)

    def create_regression_plot(self, X, y, predictions):
        """
        Generates a matplotlib figure showing the actual data points and the regression line.

        Parameters:
        ----------
        X : pd.DataFrame
            The input features used in the regression model.
        y : pd.Series
            The target output used in the regression model.
        predictions : np.ndarray
            The predicted values from the regression model.
        
        Returns:
        -------
        matplotlib.figure.Figure
            A matplotlib figure with the regression plot.
        """
        fig, ax = plt.subplots(figsize=(8, 7))
        ax.scatter(X, y, color='blue', label='Actual Data')
        ax.plot(X, predictions, color='red', label='Regression Line')
        ax.set_title('Linear Regression', fontsize=14, color='white')
        ax.set_xlabel(self.app.selected_input_column, fontsize=12, color='white')
        ax.set_ylabel(self.app.selected_output_column, fontsize=12, color='white')
        ax.legend()
        return fig

    def embed_plot_in_frame(self, fig, frame):
        """
        Embeds a matplotlib plot into a given custom Tkinter frame.

        Parameters:
        ----------
        fig : matplotlib.figure.Figure
            The matplotlib figure to be embedded.
        frame : ctk.CTkFrame
            The frame where the plot will be displayed.
        """
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=10, pady=10, fill="both", expand=True)
        plt.close(fig)

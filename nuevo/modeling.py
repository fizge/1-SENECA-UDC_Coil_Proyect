import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import messagebox,ttk
import customtkinter as ctk
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename, asksaveasfilename

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
        self.descripcion_texto = None  ###aqui creo la instancia
        
    
                    


    def guardar_archivo(self):
        
        descripcion = self.descripcion_texto.get("1.0", "end").strip() 
        if not descripcion:
            messagebox.showwarning("Advertencia", "No has escrito nada.")
            return 

        archivo = asksaveasfilename(defaultextension=".txt", 
                                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if archivo:
            ###Guardar la descripción en un archivo de texto
            with open(archivo, "w") as file:
                file.write(self.descripcion_texto.get("1.0", "end"))
                
    def clear_placeholder(self, event):
        if self.descripcion_texto.get("1.0", "end-1c") == "Escribe la descripción del modelo aquí...":
            self.descripcion_texto.delete("1.0", "end")

    def restore_placeholder(self, event):
        if not self.descripcion_texto.get("1.0", "end-1c").strip():
            self.descripcion_texto.insert("1.0", "Escribe la descripción del modelo aquí...")

                
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

            
            if hasattr(self, 'graphic_frame') and self.graphic_frame is not None:
                self.graphic_frame.destroy()
        
            self.graphic_frame = ctk.CTkFrame(self.app.v)
            self.graphic_frame.grid(row=0, column=1, rowspan=8, padx=10, pady=10, sticky="nsew")
            
            mycanvas = tk.Canvas(self.graphic_frame)
            mycanvas.grid(row=0, column=0, sticky="nsew")  

            ###Crear el Scrollbar 
            yscrollbar = tk.Scrollbar(self.graphic_frame, orient="vertical", command=mycanvas.yview)
            yscrollbar.grid(row=0, column=1, sticky="ns") 
            mycanvas.configure(yscrollcommand=yscrollbar.set)
            
            xscrollbar = tk.Scrollbar(self.graphic_frame, orient="horizontal", command=mycanvas.xview)
            xscrollbar.grid(row=1, column=0, sticky="ew")  
            mycanvas.configure(xscrollcommand=xscrollbar.set)

          
            myframe = tk.Frame(mycanvas)
            mycanvas.create_window((0, 0), window=myframe, anchor="nw")
            myframe.bind("<Configure>", lambda e: mycanvas.configure(scrollregion=mycanvas.bbox('all')))

            ###Asegura de que el marco gráfico expanda el canvas
            self.graphic_frame.columnconfigure(0, weight=1)  
            self.graphic_frame.rowconfigure(0, weight=1)  

            
            formula_label = ctk.CTkLabel(myframe, text=f"Model Formula:\n\n{formula}", font=("Arial", 10, 'bold'), text_color="black")
            formula_label.pack(pady=30, padx=10, anchor="w")

            r_squared_label = ctk.CTkLabel(myframe, text=f"R²: {r_squared:.4f}", font=("Arial", 10, 'bold'), text_color="black")
            r_squared_label.pack(pady=5, padx=10, anchor="w")

            mse_label = ctk.CTkLabel(myframe, text=f"MSE: {mse:.4f}", font=("Arial", 10, 'bold'), text_color="black")
            mse_label.pack(pady=5, padx=10, anchor="w")

       ### añade el recuadro de texto
            self.descripcion_texto = ScrolledText(myframe, wrap="word", width=10, height=10)
            self.descripcion_texto.pack(expand=True, fill="both", padx=10, pady=10)
            self.descripcion_texto.insert("1.0", "Escribe la descripción del modelo aquí...")

            ###configura los eventos para el texto de marcador de posición
            self.descripcion_texto.bind("<FocusIn>", self.clear_placeholder)
            self.descripcion_texto.bind("<FocusOut>", self.restore_placeholder)

            save_button = ctk.CTkButton(myframe, text="SAVE text", command=self.guardar_archivo,
                                        font=("Arial", 10, 'bold'), width=20, height=20, fg_color="#1976D2", hover_color="#1565C0", corner_radius=10)
            save_button.pack(pady=10, padx=10)

            
            self.plot_regression_plot(X, y, predictions, myframe)

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
        fig, ax = plt.subplots(figsize=(2, 2))
        ax.scatter(X, y, color='blue', label='Actual Data')
        ax.plot(X, predictions, color='red', label='Regression Line')
        ax.set_title('Linear Regression', fontsize=10, color='black')
        ax.set_xlabel(self.app.selected_input_column, fontsize=10, color='black')
        ax.set_ylabel(self.app.selected_output_column, fontsize=10, color='black')
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
        fig.set_size_inches(7, 6)
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=20, pady=20,fill="both", expand=True)
        plt.close(fig)

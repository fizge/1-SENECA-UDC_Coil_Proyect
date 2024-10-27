import pandas as pd
from tkinter import messagebox
import customtkinter as ctk
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Modeling:
    def __init__(self, app):
        self.app = app
        self.v2 = None  # Definir v2 como None hasta que se cree

    def generate_model(self):
        messagebox.showinfo("Model Generation", f"Model generated with Input: {self.app.selected_input_column} and Output: {self.app.selected_output_column}")

        if not self.app.selected_input_column or not self.app.selected_output_column:
            messagebox.showerror("Error", "You must confirm Input and Output selections before generating the model.")
            return

        if self.app.loaded_data is None:
            messagebox.showerror("Error", "No data loaded.")
            return

        if self.app.selected_input_column not in self.app.loaded_data.columns or self.app.selected_output_column not in self.app.loaded_data.columns:
            messagebox.showerror("Error", "Selected columns do not exist in the loaded data.")
            return

        X = self.app.loaded_data[[self.app.selected_input_column]]
        y = self.app.loaded_data[self.app.selected_output_column]

        if self.app.selected_input_column == 'ocean_proximity' or self.app.selected_output_column == 'ocean_proximity':
            messagebox.showerror("Error", "Cannot use 'ocean_proximity' as input or output variable. Please select a numeric variable.")
            return

        try:
            model = LinearRegression()
            model.fit(X, y)
            predictions = model.predict(X)

            r_squared = r2_score(y, predictions)
            mse = mean_squared_error(y, predictions)

            formula = f"{self.app.selected_output_column} = ({model.coef_[0]:.4f}) * ({self.app.selected_input_column}) + ({model.intercept_:.4f})"

            self.create_v2_window()

            self.show_model_results(formula, r_squared, mse, X, y, predictions)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating the model: {e}")

    def create_v2_window(self):
        if self.v2 is None or not self.v2.winfo_exists():
            self.v2 = ctk.CTkToplevel(self.app.v)
            self.v2.title("Modeling Results")
            self.v2.geometry("600x400")
            self.v2.configure(bg="#2B2B2B")
            self.v2.grid_rowconfigure(0, weight=1)
            self.v2.grid_columnconfigure(0, weight=1)
            self.v2.grid_columnconfigure(1, weight=1)
            self.app.v.withdraw()  # Cerrar v

        else:
            self.v2.lift()

    def show_model_results(self, formula, r_squared, mse, X, y, predictions):
        # Crear un marco para los labels de resultados
        labels_frame = ctk.CTkFrame(self.v2, fg_color="#333333", corner_radius=15)
        labels_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Labels en negrita
        formula_label = ctk.CTkLabel(labels_frame, text=f"Model Formula:\n\n{formula}",
                                     font=("Arial", 16, 'bold'), text_color="white", justify="left")
        formula_label.grid(row=0, column=0, pady=15, padx=20, sticky="w")

        r_squared_label = ctk.CTkLabel(labels_frame, text=f"R²: {r_squared:.4f}",
                                       font=("Arial", 14, 'bold'), text_color="white")
        r_squared_label.grid(row=1, column=0, pady=10, padx=20, sticky="w")

        mse_label = ctk.CTkLabel(labels_frame, text=f"MSE: {mse:.4f}",
                                 font=("Arial", 14, 'bold'), text_color="white")
        mse_label.grid(row=2, column=0, pady=10, padx=20, sticky="w")

        # Botones ajustados
        buttons_frame = ctk.CTkFrame(self.v2, fg_color="#333333", corner_radius=15)
        buttons_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        graph_button = ctk.CTkButton(buttons_frame, text="Graphic", command=lambda: self.plot_regression_plot(X, y, predictions),
                                     font=("Arial", 14, 'bold'), width=160, height=60, fg_color="#1976D2", hover_color="#1565C0", corner_radius=10)
        graph_button.grid(row=0, column=1, pady=20, padx=10, sticky="ew")

        back_button = ctk.CTkButton(buttons_frame, text="Back", command=self.go_back_to_v,
                                    font=("Arial", 14, 'bold'), width=160, height=60, fg_color="#1976D2", hover_color="#1565C0", corner_radius=10)
        back_button.grid(row=0, column=0, pady=20, padx=20, sticky="ew")

        # Espacio para la gráfica al lado de los botones
        self.plot_frame = ctk.CTkFrame(self.v2, fg_color="#333333", corner_radius=15)
        

        for i in range(3):
            labels_frame.grid_rowconfigure(i, weight=0)

    def go_back_to_v(self):
        if self.v2:
            self.v2.destroy()  # Cerrar v2
            self.app.v.deiconify()  # Mostrar v de nuevo

    def plot_regression_plot(self, X, y, predictions):
        self.v2.geometry("1200x600")
        self.plot_frame.grid(row=0, column=1, rowspan=2, padx=20, pady=20, sticky="nsew")
        fig = self.create_regression_plot(X, y, predictions)
        self.embed_plot_in_frame(fig)

    def create_regression_plot(self, X, y, predictions):
        fig, ax = plt.subplots(figsize=(8, 7))
        ax.scatter(X, y, color='blue', label='Datos reales')
        ax.plot(X, predictions, color='red', label='Línea de regresión')
        ax.set_title('Regresión Lineal', fontsize=14, color='white')
        ax.set_xlabel(self.app.selected_input_column, fontsize=12, color='white')
        ax.set_ylabel(self.app.selected_output_column, fontsize=12, color='white')
        ax.legend()
        return fig

    def embed_plot_in_frame(self, fig):
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        plt.close(fig)  # Cerrar la ventana de matplotlib para evitar que se mantenga abierta

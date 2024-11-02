import pandas as pd
from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.scrolledtext import ScrolledText


from tkinter.filedialog import askopenfilename, asksaveasfilename



class Modeling:
    def __init__(self, app):
        self.app = app
        self.v2 = None  # Definir v2 como None hasta que se cree
        self.descripcion_texto = None  ###aqui creo la instancia

    def generate_model(self):
        messagebox.showinfo("Model Generation", f"Model generated with Input: {self.app.selected_input_column} and Output: {self.app.selected_output_column}")

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





## he cambiado solo esta parte 

    def create_v2_window(self):
        if self.v2 is None or not self.v2.winfo_exists():
            self.v2 = ctk.CTkToplevel(self.app.v)
            self.v2.title("Modeling Results")
            self.v2.geometry("800x500")
            self.v2.configure(bg="#2B2B2B")
            self.v2.grid_rowconfigure(0, weight=1)
            self.v2.grid_columnconfigure(0, weight=1)
            self.v2.grid_columnconfigure(1, weight=1)
            self.app.v.withdraw()  # Cerrar v

             ###agregar área de texto para la descripción del modelo
            self.descripcion_texto = ScrolledText(self.v2,wrap="word")
            self.descripcion_texto.pack(expand="True",fill="both")
            self.descripcion_texto.insert("1.0", "Escribe la descripción del modelo aquí...")

           ## le indica al usuario donde escribir , y al pinchar le deja espacio 
            self.descripcion_texto.bind("<FocusIn>", self.clear_placeholder)
            self.descripcion_texto.bind("<FocusOut>", self.restore_placeholder)
            self.descripcion_texto.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

        else:
            self.v2.lift()
            
    def clear_placeholder(self, event):
        if self.descripcion_texto.get("1.0", "end-1c") == "Escribe la descripción del modelo aquí...":
            self.descripcion_texto.delete("1.0", "end")

    def restore_placeholder(self, event):
        if not self.descripcion_texto.get("1.0", "end-1c").strip():
            self.descripcion_texto.insert("1.0", "Escribe la descripción del modelo aquí...")



    def abrir_archivo(self):
        archivo = askopenfilename()
        if archivo:
            self.descripcion_texto.delete("1.0", "end")
            with open(archivo, "r") as file:
                self.descripcion_texto.insert("1.0", file.read())


    def guardar_archivo(self):
       
        descripcion = self.descripcion_texto.get("1.0", "end").strip() 
        if not descripcion:
            messagebox.showwarning("Advertencia", "No has escrito nada.")
            return 

        archivo = asksaveasfilename(defaultextension=".txt", 
                                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if archivo:
            # Guardar la descripción en un archivo de texto
            with open(archivo, "w") as file:
                file.write(self.descripcion_texto.get("1.0", "end"))

            


## no tocadao

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




##### BOTONES PARA GUARDAR Y ABRIR ARCHIVOS DE TEXTO 

        graph_button = ctk.CTkButton(buttons_frame, text="Graphic", command=lambda: self.plot_regression_plot(X, y, predictions),
                                     font=("Arial", 14, 'bold'), width=30, height=30, fg_color="#1976D2", hover_color="#1565C0", corner_radius=10)
        graph_button.grid(row=0, column=1, pady=20, padx=10, sticky="ew")

        back_button = ctk.CTkButton(buttons_frame, text="Back", command=self.go_back_to_v,
                                    font=("Arial", 14, 'bold'), width=30, height=30, fg_color="#1976D2", hover_color="#1565C0", corner_radius=10)
        back_button.grid(row=0, column=4, pady=20, padx=20, sticky="ew")
### añadido 

        save_button = ctk.CTkButton(buttons_frame, text="SAVE text", command=self.guardar_archivo,
                                    font=("Arial", 14, 'bold'), width=30, height=30, fg_color="#1976D2", hover_color="#1565C0", corner_radius=10)
        save_button.grid(row=0, column=3, pady=20, padx=20, sticky="ew")

        OPEN_button = ctk.CTkButton(buttons_frame, text="OPEN text", command=self.abrir_archivo,
                                    font=("Arial", 14, 'bold'), width=30, height=30, fg_color="#1976D2", hover_color="#1565C0", corner_radius=10)
        OPEN_button.grid(row=0, column=2, pady=20, padx=20, sticky="ew")

## no tocado 
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
        self.plot_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")
        fig = self.create_regression_plot(X, y, predictions)
        self.embed_plot_in_frame(fig)
        

    def create_regression_plot(self, X, y, predictions):
        fig, ax = plt.subplots(figsize=(8,7))
        ax.scatter(X, y, color='blue', label='Datos reales')
        ax.plot(X, predictions, color='red', label='Línea de regresión')
        ax.set_title('Regresión Lineal', fontsize=9)
        ax.set_xlabel(self.app.selected_input_column, fontsize=9)
        ax.set_ylabel(self.app.selected_output_column, fontsize=9)
        ax.legend()
        
        return fig


    def Pembed_plot_in_frame(self, fig):
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        plt.close(fig)  
    

## cambiado 

    def embed_plot_in_frame(self, fig): ### mostrar la grafica en el canva , aunque no doy hecho que se muestre la variable del eje y 
       
        frame_width = self.plot_frame.winfo_width()
        frame_height = self.plot_frame.winfo_height()
        
        
        dpi = fig.get_dpi()  # Obtener los DPI de la figura
        fig.set_size_inches(frame_width / dpi, frame_height / dpi)  

        
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()

        
        canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.plot_frame.grid_rowconfigure(0, weight=1)
        self.plot_frame.grid_columnconfigure(0, weight=1)
        plt.close(fig)

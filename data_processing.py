
import pandas as pd
from tkinter import messagebox, ttk
from file_reader import read_csv_or_excel, read_sqlite
import customtkinter as ctk

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DataProcessing:
    def __init__(self, app):
        self.app = app
        self.loaded_data = None

    def import_data(self, file_path):
        self.app.deleted_rows = None  
        if self.app.show_deleted_button:
            self.app.show_deleted_button.grid_forget()
        
        if file_path.endswith(('.csv', '.xlsx', '.xls')):
            self.app.loaded_data = read_csv_or_excel(file_path)
        elif file_path.endswith(('.sqlite', '.db')):
            self.app.loaded_data = read_sqlite(file_path)
        
        if self.app.loaded_data is not None:
            self.detect_nan(self.app.loaded_data)
            self.display_data_in_treeview(self.app.loaded_data)

    def detect_nan(self, data):
        nan_info = data.isna().sum()
        nan_cols = nan_info[nan_info > 0]
        if not nan_cols.empty:
            messagebox.showinfo("Missing Values", f"NaN detected in: \n{nan_cols}")
        else:
            messagebox.showinfo("No Missing Values", "There are no missing values in the data.")

    def display_data_in_treeview(self, data):
        
        if self.app.tree is None:
            self.tree_frame = ctk.CTkFrame(self.app.v)  
            self.tree_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
            
            self.app.tree = ttk.Treeview(self.tree_frame)  
            self.app.tree.grid(row=0, column=0, sticky="nsew")
            
            scrollbar_x = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.app.tree.xview)
            self.app.tree.configure(xscrollcommand=scrollbar_x.set)
            scrollbar_x.grid(row=1, column=0, sticky="ew")
            
            scrollbar_y = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.app.tree.yview)
            self.app.tree.configure(yscrollcommand=scrollbar_y.set)
            scrollbar_y.grid(row=0, column=1, sticky="ns")
            
            self.app.v.grid_rowconfigure(5, weight=1)
        
        self.app.tree.delete(*self.app.tree.get_children())  
        self.app.tree['columns'] = list(data.columns)
        self.app.tree['show'] = 'headings'
        
        for col in self.app.tree['columns']:
            self.app.tree.heading(col, text=col)
        
        for _, row in data.iterrows():
            self.app.tree.insert("", "end", values=list(row))

        self.tree_frame.grid_rowconfigure(0, weight=1)  
        self.tree_frame.grid_columnconfigure(0, weight=1)
        
        self.add_input_output_buttons(data.columns)

    def add_input_output_buttons(self, columns):
        if self.app.selection_frame is not None:
            self.app.selection_frame.grid_forget()
        
        self.app.selection_frame = ctk.CTkFrame(self.app.v)
        self.app.selection_frame.grid(row=3, column=0, columnspan=2, pady=10, padx=10)

        self.app.v.geometry("1000x700")

        input_label = ctk.CTkLabel(self.app.selection_frame, text="Select Input:", font=("Arial", 14, 'bold'))
        input_label.grid(row=0, column=4, padx=10, pady=10)
        
        self.app.input_select = ctk.CTkOptionMenu(self.app.selection_frame, values=list(columns))
        self.app.input_select.grid(row=0, column=5, padx=10, pady=10)

        output_label = ctk.CTkLabel(self.app.selection_frame, text="Select Output:", font=("Arial", 12, 'bold'))
        output_label.grid(row=1, column=4, padx=10, pady=10)
        
        self.app.output_select = ctk.CTkOptionMenu(self.app.selection_frame, values=list(columns))
        self.app.output_select.grid(row=1, column=5, padx=10, pady=10)

        generate_button = ctk.CTkButton(self.app.selection_frame, text="Generate model", font=("Arial", 12, "bold"), width=70, height=30, command=self.generate_model)
        generate_button.grid(row=0, column=0, columnspan=3, rowspan=2, padx=(40, 140), pady=10, sticky="ew")
        
        confirm_button = ctk.CTkButton(self.app.selection_frame, text="Confirm Selections", font=("Arial", 12, "bold"), width=70, height=30, command=self.confirm_selections)
        confirm_button.grid(row=0, column=6, rowspan=2, padx=(20, 10), pady=10)

    def confirm_selections(self):
        self.app.selected_input_column = self.app.input_select.get()
        self.app.selected_output_column = self.app.output_select.get()
        
        if not self.app.selected_input_column or not self.app.selected_output_column:
            messagebox.showerror("Error", "Please select both Input and Output columns.")
            return

        messagebox.showinfo("Selections Confirmed", f"Input Column: {self.app.selected_input_column}\nOutput Column: {self.app.selected_output_column}")



# generar el modelo

    def generate_model(self):
        if not self.app.selected_input_column or not self.app.selected_output_column:
            messagebox.showerror("Error", "You must confirm Input and Output selections before generating the model.")
            return

        # Verificar que los datos estén disponibles
        if self.app.loaded_data is None:
            messagebox.showerror("Error", "No data loaded.")
            return

        # Verificar que las columnas seleccionadas existen en los datos
        if self.app.selected_input_column not in self.app.loaded_data.columns or \
        self.app.selected_output_column not in self.app.loaded_data.columns:
            messagebox.showerror("Error", "Selected columns do not exist in the loaded data.")
            return

        # Extraer las columnas seleccionadas
        X = self.app.loaded_data[[self.app.selected_input_column]]  
        y = self.app.loaded_data[self.app.selected_output_column]   

        # Verificar si la columna de entrada o salida es 'ocean_proximity' o no es numérica
        if self.app.selected_input_column == 'ocean_proximity' or self.app.selected_output_column == 'ocean_proximity':
            messagebox.showerror("Error", "Cannot use 'ocean_proximity' as input or output variable. Please select a numeric variable.")
            return

        try:
            # Crear y ajustar el modelo de regresión lineal
            model = LinearRegression()
            model.fit(X, y)

            # Obtener las predicciones
            predictions = model.predict(X)

            # Calcular métricas
            r_squared = r2_score(y, predictions)
            mse = mean_squared_error(y, predictions)

            # Mostrar resultados
            formula = f"{self.app.selected_output_column} = ({model.coef_[0]:.4f}) * ({self.app.selected_input_column}) + ({model.intercept_:.4f})"

            # Pasar resultados a la función de visualización
            self.show_model_results(formula, r_squared, mse, X, y, predictions)
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating the model: {e}")
            
# mostrar resultados

    def show_model_results(self, formula, r_squared, mse, X, y, predictions):
    
        # Crear un nuevo frame para los resultados
        self.results_frame = ctk.CTkFrame(self.app.v)
        self.results_frame.grid(row=7, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)

        # Crear un canvas para el scroll
        self.results_canvas = ctk.CTkCanvas(self.results_frame)
        self.results_canvas.grid(row=0, column=0, sticky="nsew")

        # Crear un scrollbar vertical
        vertical_scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.results_canvas.yview)
        vertical_scrollbar.grid(row=0, column=1, sticky="ns")

        # Configurar el canvas para que use los scrollbars
        self.results_canvas.configure(yscrollcommand=vertical_scrollbar.set)

        # Crear y configurar un marco para los resultados dentro del canvas
        self.results_inner_frame = ctk.CTkFrame(self.results_canvas)
        self.results_inner_frame.grid(row=3, column=0, columnspan=2, pady=10, padx=10)

        # Crear una ventana dentro del canvas para el frame de resultados
        self.results_window = self.results_canvas.create_window((0, 0), window=self.results_inner_frame, anchor='nw')

        # Mostrar la fórmula del modelo
        formula_label = ctk.CTkLabel(self.results_inner_frame, text=f"Model Formula:\n\nSalida: {formula}", font=("Arial", 14))
        formula_label.grid(row=0, column=0, pady=5, sticky="w")

        # Mostrar el R²
        r_squared_label = ctk.CTkLabel(self.results_inner_frame, text=f"R²: {r_squared:.4f}", font=("Arial", 14))
        r_squared_label.grid(row=1, column=0, pady=5, sticky="w")

        # Mostrar el MSE
        mse_label = ctk.CTkLabel(self.results_inner_frame, text=f"MSE: {mse:.4f}", font=("Arial", 14))
        mse_label.grid(row=2, column=0, pady=5, sticky="w")

        # Botón para eliminar los resultados y su espacio
        close_button = ctk.CTkButton(self.results_inner_frame, text="Clear Results", command=self.clear_results)
        close_button.grid(row=3, column=0, pady=10, sticky="w")
        

        # Botón para mostrar la gráfica
        graph_button = ctk.CTkButton(self.results_inner_frame, text="Graphic", command=lambda: self.plot_regression_plot(X, y, predictions,pltShow=False))
        graph_button.grid(row=3, column=1, pady=10, sticky="w")

        graph_big_button = ctk.CTkButton(self.results_inner_frame, text="big graphic", command=lambda: self.plot_regression_plot(X, y, predictions,pltShow=True))
        graph_big_button.grid(row=2, column=1, pady=10, sticky="w")
        
    
        # Configurar filas en el frame de resultados
        for i in range(4):
            self.results_inner_frame.grid_rowconfigure(i, weight=0)  # Configura los textos para cada fila
            
        # Habilitar el scrollbar
        self.results_canvas.bind("<Configure>", lambda e: self.results_canvas.config(scrollregion=self.results_canvas.bbox("all")))

        self.results_frame.grid_rowconfigure(0, weight=3)  
        self.results_frame.grid_columnconfigure(0, weight=3)  

        self.app.selection_frame.grid_forget()   #### pongo esto para que haya mas espacio para la grafica pero luego vuelve a aparecer pq lo llama en clear
        
    def plot_regression_plot(self, X, y, predictions,pltShow=False):
        """Maneja el evento del botón para mostrar la gráfica de regresión."""
        
        if pltShow :
            # Crear la figura de matplotlib
            fig = self.create_regression_plot(X, y, predictions)
    
            plt.show()
        else:
        
            # Crear la figura de matplotlib
            fig = self.create_regression_plot(X, y, predictions)
            
            # Incrustar la gráfica en el frame
            self.embed_plot_in_frame(fig)

    def create_regression_plot(self, X, y, predictions):
        """Crea una figura de regresión lineal."""
        fig, ax = plt.subplots(figsize=(8, 7))
        
        # Gráfica de los datos reales
        ax.scatter(X, y, color='blue', label='Datos reales')
        
        # Gráfica de la línea de regresión
        ax.plot(X, predictions, color='red', label='Línea de regresión')

        ax.set_title('Regresión Lineal')
        ax.set_xlabel(self.app.selected_input_column)
        ax.set_ylabel(self.app.selected_output_column)
        ax.legend()
        

        return fig

    def embed_plot_in_frame(self, fig):
        """Incrusta la figura en el frame de resultados."""
        # Incrustar la gráfica en la columna 1
        canvas = FigureCanvasTkAgg(fig, master=self.results_inner_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    def clear_results(self):
        """Destruir el frame de resultados."""
        if hasattr(self, 'results_frame'):
            self.app.selection_frame.grid(row=3, column=0, columnspan=2, pady=10, padx=10)  #### vuelve a aparacer 
            plt.close('all') ### se estaba ejecutando el plt en segundo plano , por lo que no se cerraba la app
            self.results_frame.destroy()
            

    


        


 
 
 ##no tocado
 
 
 
 
    def apply_preprocessing(self, option):
        if self.app.loaded_data is None:
            messagebox.showerror("Error", "Please load a file first.")
            return

        if not self.app.selected_input_column or not self.app.selected_output_column:
            messagebox.showerror("Error", "Please confirm Input and Output selections first.")
            return

        if self.app.selected_input_column not in self.app.loaded_data.columns or self.app.selected_output_column not in self.app.loaded_data.columns:
            messagebox.showerror("Error", "One or more selected columns no longer exist in the dataset.")
            return
        
        columns_to_process = [self.app.selected_input_column, self.app.selected_output_column]
        
        if option == "Remove rows with NaN":
            df_original = self.app.loaded_data.copy()  
            self.app.loaded_data.dropna(subset=columns_to_process, inplace=True)
            self.app.deleted_rows = pd.concat([df_original, self.app.loaded_data]).drop_duplicates(keep=False)
            if self.app.deleted_rows.empty:
                messagebox.showinfo("No Rows Deleted", "No rows were deleted.")
            else:
                messagebox.showinfo("Success", "Rows with NaN have been deleted.")
                # if not self.app.show_deleted_button:
                #     self.app.show_deleted_button = ctk.CTkButton(self.app.v, text="Show Deleted Rows", command=lambda: self.show_deleted_rows(self.app.deleted_rows))
                # self.app.show_deleted_button.grid(row=6, column=0, columnspan=2, pady=10)

        elif option in ["Fill with Mean", "Fill with Median", "Fill with Constant Value"]:
            self.fill_na_values(option, columns_to_process)

        # elif option == "Show rows with NaN":
        #     self.show_nan_rows(self.app.loaded_data[columns_to_process])

        self.display_data_in_treeview(self.app.loaded_data)

    def fill_na_values(self, method, columns):
        columns_with_nan = [col for col in columns if self.app.loaded_data[col].isna().any()]

        if not columns_with_nan:
            messagebox.showinfo("No NaN", "No columns with NaN values found in the selected Input and Output.")
            return

        if method == "Fill with Constant Value":
            top = ctk.CTkToplevel(self.app.v)
            top.title("Fill NaN Values")
            top.lift()

            ctk.CTkLabel(top, text="Enter constant values for the selected columns with NaN:").pack(pady=10)

            entries = {}
            
            for column in columns_with_nan:
                ctk.CTkLabel(top, text=f"{column}:").pack(pady=5)
                entry = ctk.CTkEntry(top)
                entry.pack(pady=5)
                entries[column] = entry

            def apply_values():
                for column in columns_with_nan:
                    entry = entries[column]
                    if entry.get():  
                        try:
                            constant_value = float(entry.get())
                            self.app.loaded_data[column] = self.app.loaded_data[column].fillna(constant_value)
                            messagebox.showinfo("Success", f"NaN values in '{column}' filled with: {constant_value}")
                        except ValueError:
                            messagebox.showerror("Error", f"Invalid numeric value for '{column}'.")
                            return

                top.destroy()
                self.display_data_in_treeview(self.app.loaded_data)

            ctk.CTkButton(top, text="Apply", command=apply_values).pack(pady=10)
            top.protocol("WM_DELETE_WINDOW", top.destroy)
        else:
            for column in columns_with_nan:
                if method == "Fill with Mean":
                    value = self.app.loaded_data[column].mean()
                    self.app.loaded_data[column] = self.app.loaded_data[column].fillna(value)
                    messagebox.showinfo("Success", f"NaN values in '{column}' filled with mean: {value:.2f}")
                elif method == "Fill with Median":
                    value = self.app.loaded_data[column].median()
                    self.app.loaded_data[column] = self.app.loaded_data[column].fillna(value)
                    messagebox.showinfo("Success", f"NaN values in '{column}' filled with median: {value:.2f}")

        self.display_data_in_treeview(self.app.loaded_data)


    
import pickle
import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk
from utils.charging_bar import ChargingWindow
from utils.placeholder import PlaceholderText


class LoadModel:
    def __init__(self, app):
        self.app = app
        self.info_frame = None
        self.model = None
        self.formula = None
        self.r_squared = None
        self.mse = None
        self.description = None
        self.output_column = None
        self.input_column = None
        self.prediction_res_label = None

    def load_model(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Model files", "*.pkl")])
        self.app.file_path_entry.configure(state="normal")
        self.app.file_path_entry.delete(0, tk.END)
        self.app.file_path_entry.insert(0, "")
        self.app.file_path_entry.configure(state="readonly")

        if file_path:
            charging = ChargingWindow(self.app)
            charging.bar()

            try:

                with open(file_path, "rb") as f:
                    data = pickle.load(f)
                    self.output_column = data.get('output_column')
                    self.input_column = data.get('input_column')
                    self.model = data.get('model')
                    self.formula = data.get("formula", "Not avalable")
                    self.r_squared = data.get("r_squared", "Not avalable")
                    self.mse = data.get("mse", "Not avalable")
                    self.description = data.get("description", "Not avalable")

                self.app.v.grid_columnconfigure(0, weight=1, uniform="column")
                self.app.v.grid_columnconfigure(1, weight=0, uniform="column2")
                self.app.v.grid_columnconfigure(2, weight=0, uniform="column3")
                if self.app.modeling.graphic_frame is not None:
                    self.app.modeling.graphic_frame.grid_forget()
                if self.app.preselection.selection_frame is not None:
                    self.app.preselection.selection_frame.grid_forget()
                if self.app.preselection.tree_frame is not None:
                    self.app.preselection.tree_frame.grid_forget()
                    self.app.preselection.tree = None
                if self.app.preselection.option_frame is not None:
                    self.app.preselection.option_frame.grid_forget()
                self.app.v.geometry("1000x450+200+0")

                self.create_model_info_frame()

                charging.close_bar()

                messagebox.showinfo(
                    "Recovered model", f"Recovered model. Output Column: {self.output_column}, Input Column: {self.input_column}")
            except (pickle.UnpicklingError, AttributeError, KeyError) as e:
                messagebox.showerror(
                    "Error", f"No se pudo cargar el archivo: {str(e)}")

    def create_model_info_frame(self):

        self.app.initial_frame.grid(
            row=0, column=0, pady=10, padx=10, sticky="ew")
        if self.app.preselection.separator is not None:
            self.app.preselection.separator.grid_forget()
        if self.info_frame is not None:
            self.info_frame.destroy()
        self.info_frame = ctk.CTkFrame(self.app.v,fg_color='#242424')
        self.info_frame.grid(row=2, column=0, columnspan=2,
                             pady=(10, 20), padx=10, sticky="ew")

        labels_frame = ctk.CTkFrame(
            self.info_frame, fg_color="#242424", border_width=3, border_color='white', corner_radius=10)
        labels_frame.grid(row=0, column=0, rowspan=4,
                          pady=20, padx=(80, 40), sticky="nw")

        formula_label = ctk.CTkLabel(labels_frame, text=f"Linear Regresion Ecuation:", font=(
            "Arial", 16, 'bold'), text_color="white")
        formula_label.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="w")
        formula2_label = ctk.CTkLabel(labels_frame, text=f"{self.formula}", font=(
            "Arial", 14, 'bold'), text_color="white")
        formula2_label.grid(row=1, column=0, padx=20, pady=0, sticky="w")
        r2_label = ctk.CTkLabel(labels_frame, text=f"R²: {self.r_squared:.4f}", font=(
            "Arial", 14, 'bold'), text_color="white")
        r2_label.grid(row=2, column=0, padx=20, pady=0, sticky="w")
        mse_label = ctk.CTkLabel(labels_frame, text=f"MSE: {self.mse:.4f}", font=(
            "Arial", 14, 'bold'), text_color="white")
        mse_label.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="w")

        description_label = ctk.CTkLabel(self.info_frame, text="Description:", font=(
            "Arial", 18, 'bold'), text_color="white")
        description_label.grid(row=0, column=1, padx=80,
                               pady=(20, 0), sticky="n")
        description_text = ctk.CTkTextbox(self.info_frame, height=90, width=320,
                                          fg_color="#242424", border_width=3, border_color='white', corner_radius=10)
        description_text.insert("1.0", self.description)
        description_text.configure(state="disabled")
        description_text.grid(row=0, column=1, rowspan=3,
                              padx=(0, 20), pady=(60, 40), sticky="e")

        title_prediction_label = ctk.CTkLabel(self.info_frame, text=f'{self.output_column.capitalize()} prediction for a {self.input_column} value:', font=(
            "Arial", 14, 'bold'), text_color="white")
        title_prediction_label.grid(
            row=4, column=0, padx=80, pady=(0, 10), sticky="w")

        self.prediction_input = ctk.CTkEntry(self.info_frame, width=350)
        self.prediction_input.grid(row=5, column=0, columnspan=2, padx=(
            80, 10), pady=(0, 10), sticky="w")
        placeholder = PlaceholderText(
            self.prediction_input, f"Write here a {self.input_column} value")

        prediction_button = ctk.CTkButton(
            self.info_frame, text=f"Predict", font=("Arial", 16, "bold"),
            width=90, height=40,corner_radius=30, command=self.prediction_loaded_model)
        prediction_button.grid(row=5, column=0, columnspan=2, padx=(
            460, 0), pady=(0, 10), sticky="w")

        self.app.v.geometry("1000x430+200+0")

    def prediction_loaded_model(self):

        if self.output_column and self.input_column:
            try:
                input_value = float(self.prediction_input.get())
                prediction = self.model.predict([[input_value]])
                if self.prediction_res_label is not None:
                    self.prediction_res_label.destroy()
                self.prediction_res_label = ctk.CTkLabel(self.info_frame, text=f"<{self.output_column}> = {prediction[0]:.2f} ",
                                                         font=("Arial", 14, 'bold'), text_color="white")
                self.prediction_res_label.grid(
                    row=6, column=0, columnspan=2, padx=(80, 0), pady=(0, 20), sticky="w")
            except ValueError:
                messagebox.showerror(
                    "Error", "Please enter a valid number to make the prediction.")
            except Exception as e:
                messagebox.showerror(
                    "Error", f"An error occurred during prediction: {e}")
        else:
            messagebox.showerror(
                "Error", "No se pudo obtener el modelo o las columnas del archivo.")

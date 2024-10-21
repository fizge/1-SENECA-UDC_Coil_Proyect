
import tkinter as tk
from tkinter import filedialog, ttk  
import customtkinter as ctk
import pandas as pd
from file_reader import read_csv_or_excel, read_sqlite

class DataDisplayApp:
    def __init__(self):
        self.v = self.create_window()
        self.label = None
        self.tree = None
        self.loaded_data = None
        self.create_label()
        self.create_button()
    
    def create_window(self):
        v = tk.Tk()
        v.title("Display Data")
        v.geometry("700x600")
        

        v.grid_rowconfigure(0, weight=1)
        v.grid_columnconfigure(0, weight=1)
        return v

    def open_files(self):
        file = filedialog.askopenfilename(
            title="Open",
            filetypes=(("CSV Files","*.csv"),
                       ("Excel Files","*.xlsx"),
                       ("Excel Files","*.xls"),
                       ("SQLite Files","*.sqlite"),
                       ("DB Files","*.db"))
        )
        if file: 
            self.label.config(text=f"FILE PATH: {file}") 
            self.import_data(file)

    def create_label(self):
        label2 = tk.Label(self.v,
                          text="FILE READER",
                          font="skia 35 bold")
        label2.grid(row=0,
                    column=0,
                    columnspan=2,
                    pady=20,
                    sticky="ew"
                    )
        
        self.label = tk.Label(self.v,
                              text="FILE PATH: ", 
                              font="skia 12")
        self.label.grid(row=1,
                        column=0,
                        sticky="w",
                        padx=10,
                        pady=10
                        )

    def clear_table(self):
        if self.tree is not None:
            self.tree.delete(*self.tree.get_children())

    def create_button(self):
        b_open = ctk.CTkButton(self.v,
                               text="Open File",
                               fg_color="green",
                               hover_color="darkred", 
                               text_color="white",
                               command=self.open_files)
        b_open.grid(row=2,
                    column=0,
                    padx=10,
                    pady=10,
                    sticky="e"
                    )
        
        b_clear = tk.Button(self.v, 
                            text='Clear', 
                            bg='white',
                            command=self.clear_table)
        b_clear.grid(row=2,
                     column=1,
                     padx=10,
                     pady=10,
                     sticky="w"
                     )

    def import_data(self, file_path):
        try:
            if file_path.endswith(('.csv', '.xlsx', '.xls')):
                self.loaded_data = read_csv_or_excel(file_path)
            elif file_path.endswith(('.sqlite', '.db')):
                self.loaded_data = read_sqlite(file_path)
            else:
                print("File format not supported")
                return
            
            if self.loaded_data is not None:
                self.display_data_in_treeview(self.loaded_data)
        except Exception as e:
            print(f"ERROR {e}")

    def display_data_in_treeview(self, data):
        if self.tree is None:
            self.tree = ttk.Treeview(self.v)
            self.tree.grid(row=3,
                           column=0,
                           columnspan=2,
                           padx=10,
                           pady=10,
                           sticky="nsew"
                           )
            self.v.grid_rowconfigure(3, weight=1)  
            self.v.grid_columnconfigure(1, weight=1)

        self.clear_table()  

        self.tree['columns'] = list(data.columns)
        self.tree['show'] = 'headings'

        for col in self.tree['columns']:
            self.tree.heading(col, text=col)  

        for index, row in data.iterrows():
            self.tree.insert("", "end", values=list(row))  

    def run(self):
        self.v.mainloop()

if __name__ == "__main__":
    app = DataDisplayApp()  
    app.run()  

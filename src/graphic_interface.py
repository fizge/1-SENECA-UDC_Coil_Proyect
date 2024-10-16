

import tkinter as tk
from file_reader import read_csv_or_excel
from file_reader import read_sqlite
from tkinter import filedialog, ttk  
import customtkinter as ctk
import pandas as pd

v = None  
label = None  
tree = None  

def create_window():
    global v
    v = tk.Tk()  
    v.title("Display Data") 
    v.geometry("700x600")
    
    i = tk.PhotoImage(file="imagen.png")  
    v.iconphoto(True, i)
    
    v.grid_rowconfigure(0, weight=1)
    v.grid_columnconfigure(0, weight=1)
    
    return v

def open_files():
    global file
    file = filedialog.askopenfilename(title="Open",
                                     filetypes=(("CSV Files","*.csv"),
                                                ("Excel Files","*.xlsx"),
                                                ("Excel Files","*.xls"),
                                                ("SQLite Files","*.sqlite"),
                                                ("DB Files","*.db")
                                                )
                                     )
    if file: 
        path = file
        label.config(text=f"FILE PATH: {path}") 
        import_data(path)  

def create_label():
    global label  
    
    label2 = tk.Label(v,
                      text="FILE READER",
                      font="skia 35 bold "
                      )
    label2.grid(row=0,
                column=0,
                columnspan=2,
                pady=20,
                sticky="ew"
                )  
    v.grid_columnconfigure(0, weight=1) 
    
    label =tk.Label(v,
                     text="FILE PATH: ", 
                     font="skia 12 ")         
    label.grid(row=1,
               column=0,
               sticky="w",
               padx=10,
               pady=10
               )  
def clear_table():
    tree.delete(*tree.get_children())
    
def create_button():
    global b2, b3
    b2 = ctk.CTkButton(v,
                       text="Open File",
                       fg_color="green",
                       hover_color="darkred", 
                       text_color="white",
                       command=open_files
                       )
    b2.grid(row=2, column=0, padx=10, pady=10, sticky="e")
    
    b3 = tk.Button(v, 
                   text='Clear', 
                   bg='white',
                   command=clear_table)
    b3.grid(row=2, column=1, padx=10, pady=10, sticky="w")
    
    
def import_data(file_path):
    global loaded_data
    if file_path.endswith('.csv') or file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        loaded_data = read_csv_or_excel(file_path)
    elif file_path.endswith('.sqlite') or file_path.endswith('.db'):
        loaded_data = read_sqlite(file_path)
    else:
        print("File format not supported")

    if loaded_data is not None:
        display_data_in_treeview(loaded_data)  
        

def display_data_in_treeview(data):
    global tree
    if tree is None:
        tree = ttk.Treeview(v)
        tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        v.grid_rowconfigure(3, weight=1)  
        v.grid_columnconfigure(1, weight=1)

    for child in tree.get_children():
        tree.delete(child)

    tree['columns'] = list(data.columns)
    tree['show'] = 'headings'

    for col in tree['columns']:
        tree.heading(col, text=col)  

    for index, row in data.iterrows():
        tree.insert("", "end", values=list(row))  

def main():
    create_window()
    create_label() 
    create_button() 
    v.mainloop()

if __name__ == "__main__":
    main()
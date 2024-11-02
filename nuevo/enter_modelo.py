import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox

def abrir_archivo(): # por si en vez de escribir , queramos abrir un texto ya escrito 
    archivo = askopenfilename()
    if archivo:
        texto_desplazable.delete("1.0", "end")
        with open(archivo, "r") as file:
            texto_desplazable.insert("1.0", file.read())


def guardar_archivo():
       
        descripcion = texto_desplazable.get("1.0", "end").strip() 
        if not descripcion:
            messagebox.showwarning("Advertencia", "No has escrito nada.")
            return 

        archivo = asksaveasfilename(defaultextension=".txt", 
                                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if archivo:
            # Guardar la descripción en un archivo de texto
            with open(archivo, "w") as file:
                file.write(texto_desplazable.get("1.0", "end"))


def clear_placeholder(event):
    if texto_desplazable.get("1.0", "end-1c") == "Escribe la descripción del modelo aquí...":
        texto_desplazable.delete("1.0", "end")


def restore_placeholder(event):
    if not texto_desplazable.get("1.0", "end-1c").strip():
        texto_desplazable.insert("1.0", "Escribe la descripción del modelo aquí...")

## crear ventana
ventana = tk.Tk()


### guia para el  usuaria ,que le indica donde escribir , al pulsar desaparece el texto indicativo
texto_desplazable = ScrolledText(ventana, wrap="word")
texto_desplazable.pack(expand=True, fill="both")
texto_desplazable.insert("1.0", "Escribe la descripción del modelo aquí...")


texto_desplazable.bind("<FocusIn>", clear_placeholder)
texto_desplazable.bind("<FocusOut>", restore_placeholder)


##botones 
boton_abrir = tk.Button(ventana, text="Abrir", command=abrir_archivo)
boton_abrir.pack(side="left")

boton_guardar = tk.Button(ventana, text="Guardar", command=guardar_archivo)
boton_guardar.pack(side="left")


### mostra ventana
ventana.mainloop()

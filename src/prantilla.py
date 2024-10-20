


"""
    colores : https://cs111.wellesley.edu/archive/cs111_fall14/public_html/labs/lab12/tkintercolor.html
    
    import customtkinter as ctk  librerias con más diseños de colores
    
"""


import tkinter as tk # modulo propio de python



# APARIENCIA DE LA VENTANA

def crear_ventana():
    v = tk.Tk()   # clase ventana
    v.title("INTERFAZ GRAFICA") 
    v.geometry("600x400") # tamaño ventana
    #v.configure(bg="sky blue") # fondo de la ventana
    v.minsize(500,300) # no se pone entre comillas ; minimo tamaño de la ventana .
    #v.iconbitmap() poner entre comillas la imagen.ico , que es el logo
    v.attributes("-alpha",0.9) #la trasparencia de las ventanas
    return v


def crear_frames(v): # se pasa la clase ventana
    # Crear un Frame y establecer su tamaño
    frame1 = tk.Frame(v)
    frame1.configure(width=500,
                     height=300,
                     bg="light gray",
                     bd=9
                     )  # tamaños del frame ,color y grosor
    frame1.place(relx=0.5,
                 rely=0.5,
                 anchor="center"
                 )  # centrar el Frame
    return frame1 # retornas frame para usar en labels
    
    
def crear_labels(v): # etiquetas == labels 
    
    # Agregar un Label dentro del Frame
    l = tk.Label(v,
                 text="¡Esto es una etiqueta !\n Dime tu nombre :)"
                 )
    # centrar el Label dentro del Frame
    #l.place(relx=0.5, rely=0.5, anchor="center")  # centrar el Label
    l.pack(pady=10,
           padx=10
           ) # usarlos siempre para que se ejecute y se muestre su separacion
    return l 
    
    
    
# DESTROY 
def cerrar(ventana):
    ventana.destroy()
    
    
  
# escribir algo pulsar el boton y mostrar  

    
def actualizar(dato,label):
    # Actualizar el texto del Label
    texto = dato.get()
    texto = texto.capitalize() # en este caso si pregunto por el nombre la primera letra en mayuscula
    label.config(text=f"¡¡¡¡¡Hola {texto} ,gracias por pulsa el boton !!!!!",
                 fg="black",  # Cambia el color del texto
                 font=("Helvetica", 16, "bold"),
                 )  #color ,letra , marcar la letra en negro
    
def crear_boton(v,dato,label):
    b = tk.Button(v, text="PRESIONA AQUÍ", command=lambda: actualizar(dato, label),
                  fg="red",
                  font=("Helvetica", 16, "bold")
                  )  # Comando para el botón
    b.pack(pady=10)  # Agregar un poco de espacio vertical alrededor del botón

def crear_entrada(v):
    e = tk.Entry(v,width=30) # entry no tiene config 
    e.pack(pady=10,padx=10) # separacion arriba y abajo
    return e
    

def main():
    v=crear_ventana()
    crear_frames(v)
    l=crear_labels(v)
    e=crear_entrada(v)
    crear_boton(v,e,l)
    v.mainloop()

main()

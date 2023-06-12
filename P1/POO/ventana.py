import tkinter as tk
from tkinter import ttk, font
from tkinter import *
from logica import *

controlador=ControladorBD()

def nuevo():
    titulo.configure(text="Agregar Bebida")
    panel.add (pestana2, text='Agregar')
    txtNom.delete("0", "end")
    txtClasif.delete("0", "end")
    txtMarca.delete("0", "end")
    txtPrecio.delete("0", "end")
    panel.select(1)
    btna.pack()
    btnactu.pack_forget()
    btnDelete.pack_forget()

def agregar():
    if controlador.SaveBeverage(varNom.get(),varClasif.get(),varMarca.get(),varPrecio.get()):
        txtNom.delete("0", "end")
        txtClasif.delete("0", "end")
        txtMarca.delete("0", "end")
        txtPrecio.delete("0", "end")
        panel.forget(1)
        panel.select(0)

def modificar():
    titulo.configure(text="Modificar Bebida")
    panel.add (pestana2, text='Modificar')
    btnactu.pack()
    btnDelete.pack()
    btna.pack_forget()
    txtNom.delete("0", "end")
    txtClasif.delete("0", "end")
    txtMarca.delete("0", "end")
    txtPrecio.delete("0", "end")
    selected = tree.selection()[0]
    # obtener los valores del elemento seleccionado
    values = tree.item(selected)['values']
    txtId.insert(0, values[0])
    txtNom.insert(0, values[1])
    txtClasif.insert(0, values[2])
    txtMarca.insert(0, values[3])
    txtPrecio.insert(0, values[4])
    panel.select(1)

def actualizar():
    if controlador.UpdateBeverage(varIdUp.get(),varNom.get(),varClasif.get(),varMarca.get(),varPrecio.get()):
        txtId.delete("0", "end")
        txtNom.delete("0", "end")
        txtClasif.delete("0", "end")
        txtMarca.delete("0", "end")
        txtPrecio.delete("0", "end")
        panel.forget(1)
        panel.select(0)
        
def DeleteProd():
    if controlador.DeleteBeverage(varIdUp.get()):
        txtId.delete("0", "end")
        txtNom.delete("0", "end")
        txtClasif.delete("0", "end")
        txtMarca.delete("0", "end")
        txtPrecio.delete("0", "end")
        panel.forget(1)
        panel.select(0)
        
#funciones que llaman a las consultas de: 

# Calcular Precio promedio de bebidas
def Promedio():
    controlador.AVG()
    
    
# Cantidad de bebidas de una Marca

def ventanaEmergente():
    global varVE, ventanaMarcas
    ventanaMarcas = tk.Toplevel()
    ventanaMarcas.title("Ventana emergente")
    varVE = tk.StringVar()
    combobox = ttk.Combobox(ventanaMarcas, textvariable=varVE ,values=controlador.GetBrands())
    combobox.pack()
    boton = Button(ventanaMarcas, text="Obtener cantidad de bebidas",command=ObtenerMarca)
    boton.pack()
    
def ObtenerMarca():
    controlador.GetBeverageBrands(varVE.get())
    ventanaMarcas.destroy() 
    

# Cantidad por clasificación
def Clasificacion_Bebida():
    controlador.BeverageClasification()
    

Ventana= Tk()
Ventana.title("Almacen")
Ventana.geometry("1200x500")

panel=ttk.Notebook (Ventana)
panel.pack(fill='both', expand='yes')
pestana1=ttk.Frame (panel)
pestana2=ttk.Frame (panel)


panel.add (pestana1, text='Consultar')

fuente = font.Font(family='Helvetica', size=12, weight='bold')
TituloCons=Label(pestana1,text="Consultar Bebida", fg="blue").pack()


columns = ('ID', 'Nombre', 'Clasificación','Marca','Precio')
tree = ttk.Treeview(pestana1, columns=columns, show='headings')
tree.heading("ID", text="ID")
tree.heading("Nombre", text="Nombre")
tree.heading("Clasificación", text="Clasificación")
tree.heading("Marca", text="Marca")
tree.heading("Precio", text="Precio")
tree.pack()
btnUpdate=Button(pestana1, text='Actualizar',command=modificar)
#pero se oculta para que se ejecute solamente cuando se presiona un registro(para evitar bugs y errores por los usuarios)
btnUpdate.pack_forget()

buttonContainer = Frame(pestana1)
buttonContainer.pack(anchor='center')

BtnAdd = Button(buttonContainer, text='Nueva Bebida', command=nuevo)
BtnAdd.pack(side='left')

btnPrecioPromedio = Button(buttonContainer, text='Precio Promedio', command=Promedio)
btnPrecioPromedio.pack(side='left')

btnBebidasXMarca = Button(buttonContainer, text='BebidasXMarca',command=ventanaEmergente)
btnBebidasXMarca.pack(side='left')

btnBebidasXClasificacion = Button(buttonContainer, text='BebidasXClasificacion', command=Clasificacion_Bebida)
btnBebidasXClasificacion.pack(side='left')





#pestaña 2 
titulo = Label(pestana2, text="Agregar Bebida", fg="blue", font=fuente)
titulo.pack()

varIdUp=tk.StringVar()
txtId= Entry(pestana2, textvariable=varIdUp)

varNom = tk.StringVar()
lblNom = Label(pestana2, text="Nombre de la bebida: ")
lblNom.pack()
txtNom = Entry(pestana2, textvariable=varNom)
txtNom.pack()



varClasif = tk.StringVar()
lblClasif = tk.Label(pestana2, text="Clasificación: ")
lblClasif.pack()
txtClasif = tk.ttk.Combobox(pestana2, textvariable=varClasif, values=["Bebida Azucarada", "Bebida sin Azúcar", "Bebida Gaseosa", "Bebida Energética"])
txtClasif.pack()


varMarca = tk.StringVar()
lblMarca = tk.Label(pestana2, text="Marca: ")
lblMarca.pack()
txtMarca = tk.Entry(pestana2, textvariable=varMarca)
txtMarca.pack()

varPrecio = tk.StringVar()
lblPrecio = tk.Label(pestana2, text="Precio: ")
lblPrecio.pack()
txtPrecio = tk.Entry(pestana2, textvariable=varPrecio)
txtPrecio.pack()
btna=Button(pestana2,text="Agregar",command=agregar)
btnDelete=Button(pestana2,bg="red",fg="white",text="Eliminar!!!",command=DeleteProd)



btnactu=Button(pestana2,text="Actualizar",command=actualizar)

def Consultar(event):
    # verificar si la pestaña seleccionada es la pestaña de Consultar usuarios
    current_tab = event.widget.tab('current')['text']
    if current_tab == 'Consultar':
        #si es así pues se borran los datos del treeview para evitar que se escriban muchas veces los datos
        for row in tree.get_children():
            tree.delete(row)
        #aqui "a" va a mostrar los registros pero hare uso de un ciclo para mostrar todos los registros.
        a=controlador.ConsultBeverage()
        while a:
            row = a.pop(0)  
            #aqui se insertan los datos del ciclo en el tree por filas.
            tree.insert('', tk.END, values=(row))   
#investigue esta opcion que ejecuta la función cada que se cambia a la pestaña indicada arriba.
panel.bind('<<NotebookTabChanged>>', Consultar)


# función que muestra el botón de actualizar
def Mostrarboton(event):
    #hace uso del if un treeview esta seleccionado, muestra el botón
    if tree.selection():
        # si hay elementos seleccionados, mostrar el botón
        btnUpdate.pack()
    else:
        # si no hay elementos seleccionados, ocultar el botón
        btnUpdate.pack_forget()

# vincular la función al evento <<TreeviewSelect>>
tree.bind('<<TreeviewSelect>>', Mostrarboton)



Ventana.mainloop()

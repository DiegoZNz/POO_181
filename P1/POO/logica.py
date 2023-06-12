from tkinter import messagebox
import sqlite3


class ControladorBD:
    
    def __init__(self):
        pass
    
    #Metodos para crear conexiones
    def conexionBD(self):
        try:
            conexion= sqlite3.connect("C:/Users/diego/Desktop/UPQ/6to cuatrimestre/PROGRAMACIÓN ORIENTADA A OBJETOS/POO_181/POO/Db_BeverageWarehouse.db")
            return conexion
        except sqlite3.OperationalError:
            print("No se pudo conectar a la base de datos")
            
            
    
    def SaveBeverage(self,nom,clasif,marc,prec):
        #1. usamos una conexion 
        conx=self.conexionBD()
        #2. validar parámetros vacíos
        if(nom=="" or clasif=="" or marc=="" or prec==""):
            messagebox.showwarning("Errorsote","Formulario incompleto")
            conx.close
            return False   
        if clasif not in ["Bebida Azucarada", "Bebida sin Azúcar", "Bebida Gaseosa", "Bebida Energética"]:
            messagebox.showwarning("Error","El campo de clasificación solo admite los valores de la lista, favor de seleccionar una opción válida")
            return False
        try:
            #por ultimo validamos que el precio sea un número flotante, si es así se ejecuta la consulta de agregar producto, de lo contrario manda error.
            int(prec)
            #3. Preparamos el cursor, datos que voy a insertar y el querySQL
            cursor= conx.cursor()
            datos=(nom,clasif,marc,prec)
            qrInsert="insert into TbBeverage (Nombre, Clasificacion, Marca, Precio) values (?,?,?,?)" 
            #4.Ejecutamos el insert y cerramos la conexion
            cursor.execute(qrInsert,datos)           
            conx.commit()
            conx.close
            messagebox.showinfo("Exito","Bebida Guardada")
            conx.close()
            return True
        except ValueError:
            messagebox.showwarning("Error", "El precio debe ser un NÚMERO válido.")
            conx.close
            return False

     
    def ConsultBeverage(self):
        #1. usamos una conexion 
        conx=self.conexionBD()
        try:
            cursor=conx.cursor()
            selectquery = "SELECT * FROM TbBeverage"
            #4.ejecuta y guarda la consulta
            cursor.execute(selectquery)
            rsProd = cursor.fetchall()
            conx.close()
            #5. retornar resultados en un while
            lista = []
            for row in rsProd:
                lista.append(row)
            conx.close()
            return lista
    
        except sqlite3.OperationalError:
            print("error consulta")
            conx.close()
            
    def UpdateBeverage(self, id,nom,clasif,marc,prec):
        #1. usamos una conexion 
        conx=self.conexionBD()
        #2. validar parámetros vacíos
        if(nom=="" or clasif=="" or marc=="" or prec==""):
            messagebox.showwarning("Campos incompletos","No puedes actualzar un formulario y dejar campos vacíos")
            return False
        if clasif not in ["Bebida Azucarada", "Bebida sin Azúcar", "Bebida Gaseosa", "Bebida Energética"]:
            messagebox.showwarning("Error","El campo de clasificación solo admite los valores de la lista, favor de seleccionar una opción válida")
            return False
        try:
            #por ultimo validamos que el precio sea un número flotante, si es así se ejecuta la consulta de agregar producto, de lo contrario manda error.
            int(prec)
            #3. Preparamos el cursor, datos que voy a insertar y el querySQL
            cursor= conx.cursor()
            datosUP=(nom,clasif,marc,prec)
            qrUPD="UPDATE TbBeverage SET Nombre=?, Clasificacion=?, Marca=?, Precio=? Where id="+id
            #4.Ejecutamos el insert y cerramos la conexion
            cursor.execute(qrUPD,datosUP)           
            conx.commit()
            messagebox.showinfo("Exito","Bebida Actualizada")
            return True
        except ValueError:
            messagebox.showwarning("Error", "La cantidad debe ser un NÚMERO válido.")
            return False
        
    def DeleteBeverage(self,id):
        conx=self.conexionBD()
        #Preguntar si quiere eliminar 
        confirmar = messagebox.askyesno("Eliminar Producto", "¿Está seguro que desea eliminar este Producto? Ya no habrá punto de retorno")
        if confirmar==True:
            try:
                #3 cursos y query
                cursor=conx.cursor()
                DLTQR = "DELETE FROM TbBeverage WHERE id="+id
                #4.ejecuta y guarda la consulta
                cursor.execute(DLTQR)
                conx.commit()
                conx.close
                return True
            except sqlite3.OperationalError:
                print("error consulta")
        else:
            messagebox.showerror("Error", "No se pudo eliminar el producto.")
            conx.close
            return False
        
    def AVG(self):
        conx=self.conexionBD()
        try:
            cursor = conx.cursor()
            avg_query = "SELECT AVG(Precio) AS PrecioPromedio FROM TbBeverage;"
            cursor.execute(avg_query)
            promedio = cursor.fetchone()[0]
            messagebox.showinfo("Promedio de precios de bebidas", f"El precio promedio de las bebidas es: {promedio}")
            conx.close()
            
        except sqlite3.OperationalError:
            print("Error en la consulta")
            conx.close()
            
    def BeverageClasification(self):
        conx=self.conexionBD()
        try:
            cursor = conx.cursor()
            ClasificacionQuery = "SELECT Clasificacion, COUNT(*) AS CantidadDeBebidas FROM TbBeverage GROUP BY Clasificacion;"
            cursor.execute(ClasificacionQuery)
            resultados = cursor.fetchall()
            conx.close()

            if len(resultados) == 0:
                messagebox.showinfo("Cantidad de bebidas por clasificación", "No hay bebidas registradas en la base de datos.")
            else:
                mensaje = ""
                for resultado in resultados:
                    clasificacion = resultado[0]
                    cantidad = resultado[1]
                    mensaje += f"Clasificación: {clasificacion}\nCantidad: {cantidad}\n\n"
                messagebox.showinfo("Cantidad de bebidas por clasificación", mensaje)
                
        except sqlite3.OperationalError:
            print("Error en la consulta")
            conx.close()
        
    def GetBrands(self):
        conx=self.conexionBD()
        try:
            cursor = conx.cursor()
            consulta = "SELECT DISTINCT Marca FROM TbBeverage;"
            cursor.execute(consulta)
            marcas = cursor.fetchall()
            conx.close()
            return [marca[0] for marca in marcas]
                
        except sqlite3.OperationalError:
            print("Error en la consulta")
            conx.close()
            
            
    def GetBeverageBrands(self,marcaUser):
        if(marcaUser==""):
            messagebox.showwarning("Campos incompletos","No puedes consultar si tienes los campos vacios, por favor selecciona un campo")
            
        else:
            try:
                marca = marcaUser
                conx=self.conexionBD()
                cursor = conx.cursor()
                consulta = f"SELECT COUNT(*) FROM TbBeverage WHERE Marca = '{marca}';"
                cursor.execute(consulta)
                cantidad = cursor.fetchone()[0]
                conx.close()
                

                if cantidad is not None:
                    messagebox.showinfo("Cantidad de bebidas por marca", f"La cantidad de bebidas de la marca '{marca}' es: {cantidad}")
                else:
                    messagebox.showinfo("Cantidad de bebidas por marca", f"No se encontraron bebidas de la marca '{marca}'.")
                
            except sqlite3.OperationalError:
                print("Error en la consulta")
                conx.close()

        



        

    
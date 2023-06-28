#aquí se importa el framework 
from flask import Flask,render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from flask import flash
#inicialización del APP
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_flask'
mysql = MySQL(app)
app.secret_key = "mi_clave_secreta"


#declaración de la ruta http://localhost:5000
@app.route('/')#ruta index o raiz, busca el método index y regresa un hola mundo.
def index():
    #creamos un cursor y le decimos que ejecute la consulta para traer todos los albums y que los guarde en QueryAlbums
    #con la funcion fetchall y los imprimimos en la consola por el momento
    cursor = mysql.connection.cursor()
    cursor.execute("Select * from tbalbums")
    QueryAlbums = cursor.fetchall()
    
    cursor.execute("SELECT 1")
    result = cursor.fetchone()

    if result:
        return render_template('index.html',listAlbums = QueryAlbums)
    else:
        return "No se pudo conectar a la base de datos"

#creacion de nuevas rutas y para acceder a ellas solamente es escribir el /ruta en el navegador
#después de el localhost


@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method == 'POST':
        #pasamos a variables al contenido de los inputs
        Vtitulo = request.form['txtTitulo']
        Vartista = request.form['txtArtista']
        Vaño = request.form['txtAnio']
        
        #haremos la conex a la db y ejecutar el insert
        CS = mysql.connection.cursor()
        CS.execute('INSERT INTO tbalbums (Titulo, Artista, Anio) values (%s,%s,%s)',(Vtitulo,Vartista,Vaño))
        mysql.connection.commit()
    flash('El album fue agregado correctamente')
    return redirect(url_for('index'))




@app.route('/eliminar')
def eliminar():
    return "Se elimino en el BD"

#ejecución del servidor 
if __name__ =='__main__':
    app.run(port=5000,debug=True)
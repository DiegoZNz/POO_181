#aquí se importa el framework 
from flask import Flask,render_template, request
from flask_mysqldb import MySQL
#inicialización del APP
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_flask'
mysql = MySQL(app)

#declaración de la ruta http://localhost:5000
@app.route('/')#ruta index o raiz, busca el método index y regresa un hola mundo.
def index():
        # Ejecutar una consulta SQL simple
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()

    if result:
        return render_template('index.html')
    else:
        return "No se pudo conectar a la base de datos"

#creacion de nuevas rutas y para acceder a ellas solamente es escribir el /ruta en el navegador
#después de el localhost


@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method == 'POST':
        titulo = request.form['txtTitulo']
        artista = request.form['txtArtista']
        año = request.form['txtAnio']
        
        print(titulo,artista,año)
        
    return "los datos llegaron"


@app.route('/eliminar')
def eliminar():
    return "Se elimino en el BD"

#ejecución del servidor 
if __name__ =='__main__':
    app.run(port=5000,debug=True)
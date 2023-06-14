#aquí se importa el framework 
from flask import Flask
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
    return "HOLA MUNDO FLASK"
#creacion de nuevas rutas y para acceder a ellas solamente es escribir el /ruta en el navegador
#después de el localhost
@app.route('/guardar')
def guardar():
    return "Se guardo en el BD"
@app.route('/eliminar')
def eliminar():
    return "Se elimino en el BD"

#ejecución del servidor 
if __name__ =='__main__':
    app.run(port=5000,debug=True)
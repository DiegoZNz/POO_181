 #aquí se importa el framework 
from flask import Flask,render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from flask import flash
#inicialización del APP
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_floreria'
mysql = MySQL(app)
app.secret_key = "mi_clave_secreta"



@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    if result:
        return render_template('indexF.html')
    else:
        return "No se pudo conectar a la base de datos"



@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method == 'POST':
        VNombre = request.form['txtNombre']
        VCantidad = request.form['txtCantidad']
        Vprecio = float(request.form['txtPrecio'])
        #haremos la conex a la db y ejecutar el insert
        CS = mysql.connection.cursor()
        CS.execute('INSERT INTO tbflores (nombre, cantidad, precio) VALUES (%s, %s, %s)', (VNombre, VCantidad, Vprecio))
        mysql.connection.commit()
    flash('La flor fue agregada correctamente')
    return redirect(url_for('mostrar'))


@app.route('/mostrar')
def mostrar():
    cursor = mysql.connection.cursor()
    cursor.execute("Select * from tbflores")
    QueryFlores = cursor.fetchall()
    return render_template('tablaflores.html',listFlores = QueryFlores)
    



@app.route('/edit/<id>')
def edit(id):
    CS = mysql.connection.cursor()
    CS.execute('Select * from tbflores where id = %s',(id,))
    QueryId = CS.fetchone()
    print (QueryId)
    return render_template('deleteflores.html',listIdDlt = QueryId)

@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    if request.method == 'POST':
        if request.form.get('action') == 'delete':
            UpdCur = mysql.connection.cursor()
            UpdCur.execute('delete from tbflores where id = %s', (id,))
            mysql.connection.commit()
            flash('El album fue borrado correctamente')
        elif request.form.get('action') == 'cancel':
            flash('Borrado cancelado')
    return redirect(url_for('mostrar'))





if __name__ =='__main__':
    app.run(port=5000,debug=True)
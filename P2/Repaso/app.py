 #aquí se importa el framework 
from flask import Flask,render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from flask import flash
#inicialización del APP
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_fruteria'
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
        Vfruta = request.form['txtFruta']
        Vtemporada = request.form['txtTemporada']
        Vprecio = float(request.form['txtPrecio'])
        Vstock = int(request.form['txtStock'])
        #haremos la conex a la db y ejecutar el insert
        CS = mysql.connection.cursor()
        CS.execute('INSERT INTO tbFrutas (fruta, temporada, precio, stock) VALUES (%s, %s, %s, %s)', (Vfruta, Vtemporada, Vprecio, Vstock))
        mysql.connection.commit()
    flash('La fruta fue agregada correctamente')
    return redirect(url_for('mostrar'))


@app.route('/mostrar')
def mostrar():
    cursor = mysql.connection.cursor()
    cursor.execute("Select * from tbFrutas")
    QueryFrutas = cursor.fetchall()
    return render_template('tablafruta.html',listFrutas = QueryFrutas)
    



@app.route('/edit/<id>')
def edit(id):
    CS = mysql.connection.cursor()
    CS.execute('Select * from tbFrutas where id = %s',(id,))
    QueryId = CS.fetchone()
    print (QueryId)
    return render_template('editfrutas.html',listId = QueryId)

@app.route('/update/<id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
    
        Vfruta = request.form['txtFruta']
        Vtemporada = request.form['txtTemporada']
        Vprecio = float(request.form['txtPrecio'])
        Vstock = int(request.form['txtStock'])
        UpdCur = mysql.connection.cursor()
        UpdCur.execute('UPDATE tbFrutas SET fruta = %s, temporada = %s, precio = %s, stock = %s WHERE id = %s', (Vfruta, Vtemporada, Vprecio, Vstock, id))
        mysql.connection.commit()
    flash('La fruta fue actualizada correctamente')
    return redirect(url_for('mostrar'))

@app.route('/edit2/<id>')
def edit2(id):
    CS = mysql.connection.cursor()
    CS.execute('Select * from tbFrutas where id = %s',(id,))
    QueryId = CS.fetchone()
    print (QueryId)
    return render_template('deletefrutas.html',listIdDlt = QueryId)

@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    if request.method == 'POST':
        if request.form.get('action') == 'delete':
            UpdCur = mysql.connection.cursor()
            UpdCur.execute('delete from tbFrutas where id = %s', (id,))
            mysql.connection.commit()
            flash('El album fue borrado correctamente')
        elif request.form.get('action') == 'cancel':
            flash('Borrado cancelado')
    return redirect(url_for('mostrar'))

@app.route('/buscar')
def buscarname():
    return render_template('buscarName.html')


@app.route('/mostrarSN', methods=['POST'])
def sn():
    if request.method == 'POST':
        Vfruta = request.form['txtFruta']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM tbFrutas WHERE fruta LIKE %s', ('%' + Vfruta + '%',))
        resultados = cursor.fetchall()
        mysql.connection.commit()
        
        return render_template('buscarName.html', resultados=resultados)
       
    return redirect(url_for('buscarname'))






if __name__ =='__main__':
    app.run(port=5000,debug=True)
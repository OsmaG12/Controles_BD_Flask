from flask import Flask, render_template, request
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy
from pymysql import connect


app = Flask(__name__)

# Configuration for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Frutillita12@localhost:3306/ejemplodb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model definition for users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    pais = db.Column(db.String(45), nullable=False)

@app.route('/')
def index():
    usuarios = db.session.query(User).all()
    return render_template('usuarios.html', usuarios=usuarios)


@app.route('/agregar')
def agregar():
    return render_template('agregar.html')

@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    nombre = request.form['nombre']
    correo = request.form['correo_electronico']
    pais = request.form['pais']

    nuevo_usuario = User(nombre=nombre, correo=correo, pais=pais)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return redirect(url_for('obtener_usuarios'))


@app.route('/obtener_usuarios')
def obtener_usuarios():
    usuarios = db.session.query(User).all()
    return render_template('usuarios.html', usuarios=usuarios)


@app.route('/modificar_usuario/<int:id>', methods=['GET', 'POST'])
def modificar_usuario(id):
    usuario = db.session.query(User).filter_by(id=id).first()

    if request.method == 'POST':
        usuario.nombre = request.form['nombre']
        usuario.correo = request.form['correo_electronico']
        usuario.pais = request.form['pais']
        db.session.commit()
        return redirect(url_for('obtener_usuarios'))

    return render_template('modificar.html', usuario=usuario)

@app.route('/eliminar_usuario/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    usuario = db.session.query(User).filter_by(id=id).first()
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('obtener_usuarios'))


if __name__ == '__main__':
    app.run(debug=True)
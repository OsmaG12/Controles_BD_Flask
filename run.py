#Librerias para que funcione SqlAlchemy que es un ORM
from flask_sqlalchemy import SQLAlchemy
from pymysql import connect
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

Base = declarative_base()

#Aqui se hace el modelado de la tabla
class User(Base):
    __tablename__ = 'usuarios'#Nombre de la tabla que se modela

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(45), unique=True, nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    pais = Column(String(45), unique=True, nullable=False)

#Aqui ya se hace la conexion a la BD
DATABASE_HOST = 'localhost'
DATABASE_NAME = 'ejemploDB'#Nombre de la base de datos
DATABASE_USERNAME = 'sa'
DATABASE_PASSWORD = '12345'#Contraseña

SQLALCHEMY_DATABASE_URI = f'mssql+pyodbc://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}?driver=ODBC Driver 17 for SQL Server'#Esto del final es el JDBC
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

db = SQLAlchemy(app)

# Rutas de ejemplo
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
    return redirect(url_for('obtener_usuarios'))  # O redirecciona a otra página


@app.route('/obtener_usuarios')
def obtener_usuarios():
    usuarios = db.session.query(User).all()  # Use db.session
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
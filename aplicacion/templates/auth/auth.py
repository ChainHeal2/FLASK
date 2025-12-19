"""Bienvenido a nuestro primer Blueprint"""
import functools
from flask import (Blueprint,flash,g,render_template,request,url_for,session,redirect)
from werkzeug.security import check_password_hash , generate_password_hash
from aplicacion.db import get_db
#creamos nuestro Blueprint que llamaremos bp
#lo llamaremos auth y cada vez que necesitemos acceder a alguna funcion como register
#en el navegador sera http://127.0.0.1:5000/auth/register (pero podemos personalizar claro)
bp = Blueprint('auth',__name__, url_prefix='/auth')
@bp.route('/register',methods=['GET','POST'])
def register():
    """Nuestra primera pagina que no sea index"""
    #preguntamos si existe alguna peticion enviada desde register.html
    if request.method == 'POST':
        username = request.form['usuario']#es el nombre que tiene en el html
        password = request.form['password']
        db,c = get_db()#utilizamos 2 fuciones de la base de datos
        error = None # establecemos un error por defecto
        c.execute(
            'select id from user where username = %s',(username,)
        )
        if not username:
            error ='Username es requerido'
        if not password:
            error = 'password es requerido'
        elif c.fetchone() is not None:
            error = f'Usuario {username} se encuentra registrado.'
        elif error is None:
            c.execute(
                'insert into user (username,password) values (%s,%s)',
            (username,generate_password_hash(password)))
            db.commit()
            return redirect(url_for('auth.login'))
        flash(error)#si por cualquier cosa fallara retornaria este mensaje
        #podemos usar mensajes por defecto ("error usuario",'error')
        #esto seria un mensaje con categoria bastante util para el manejo de errores
    return render_template('/auth/register.html')

@bp.route('/login',methods = ['GET','POST'])
def login():
    """Un Login sencillo"""
    if request.method == 'POST':
        username = request.form['usuario']
        password = request.form['password']
        db,c = get_db()
        error = None
        c.execute(
            'select * from user where username = %s',(username,)
        )
        user=c.fetchone()
        if user is None:
            error = 'Usuario y o contraseña invalida'
        elif not check_password_hash(user['password'],password):
            error = 'Usuario y o contraseña invalida'
        if error is None:
            session.clear()
            session['user_id']= user['id']
            session['username']= user['username'] 
            #capturamos la session para utilizarla donde queramos en este caso en index
            return redirect(url_for('inicio.index'))
    #flash(error)
    return(render_template('auth/login.html'))
def login_required(view):
    """Funcion decoradora que toma el en este caso el login"""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

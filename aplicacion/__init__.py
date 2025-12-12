"""usar __init__ lo que hace es que interprete la carpeta de aplicacion
como si esta fuera un modulo

para que funcione debemos usar export FLASK_APP=aplicacion:create_app
esto crea una instacia de nuestra aplicacion
para que la variable de entorno detecte que estamos usando nuestra app
"""
import os # lo usamos para sacar las variables del sistema.
from flask import Flask

def create_app():
    """Creamos la APP
    desde app.config.from_mapping: son las variables del OS (operative system)
    basicamente desde donde nos estan enviado la peticion
    la SECRET_KEY seria una cookie que va firmaba con la peticion y si llegara a cambiar
    flask devuelve un error
    los datos despues de secret_key:
    HOST-PASSWORD-USER-DATABASE
    se los asigne con el comando por terminal EXPORT FLASK_DATABASE_HOST : 'localhost'
    es como si simularamos de donde nos estan enviando la peticion

    si quieres evitar estar escribiendo esto puedes usar:
    (al final del archivo activate de tu entorno de desarrolo (VENV))
    export FLASK_DATABASE_HOST='127.0.0.1'
    export FLASK_DATABASE_USER='user'
    export FLASK_DATABASE_PASSWORD='password'
    export FLASK_DATABASE='tudatabase'
    export FLASK_APP='aplicacion:create_app'
    """
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = "mikey",
        DATABASE_HOST = os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD = os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER = os.environ.get('FLASK_DATABASE_USER'),
        DATABASE = os.environ.get('FLASK_DATABASE'),
    )
    from . import db
    db.init_app(app)
    from .templates.auth import auth # importamos nuestro primer Blueprint tiene como nombre auth ver en auth.py
    app.register_blueprint(auth.bp) #ignoramos el PEP 8 en esta ocacion por la el tipo de implementacion de flask
    from .templates.index import index
    app.register_blueprint(index.bp)
    #ayuda a generar nuestras rutas dentro de la pagina, la dejaremos comentada para que no sea nuestra principal
    #@app.route('/')
    @app.route('/saludo')#podemos tener las rutas que necesitemos
    def hola():
        """Devuelve un hola mundo como simulando lo que seria un index"""
        return 'Hola Mundo!!! esta es una pagina secreta que solo se podra acceder si tenemos la ruta /saludo'
    return app
"""Solo contiene el index"""
from flask import (Blueprint,flash,g,render_template,request,url_for,session,redirect)
bp = Blueprint('inicio',__name__)#podemos no usar prefix como en auth para no generar mas rutas
@bp.route('/')
@bp.route('/index', methods = ['GET','POST'])
def index():
    """Pagina de index"""
    return render_template('base.html')# si el archivo estuviera solo dentro de templates

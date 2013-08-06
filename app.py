# -*- coding: utf-8 -*-


# all the imports
from flask import Flask, request, session, g, redirect, url_for,\
    abort, render_template, flash, make_response

import os
import csv

from Inventario import *
from Bom import *
from Mrp import *
from Abc import *

# configuration
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'xx'

UPLOADED_FILES_ALLOW = '.csv'
UPLOADS_FOLDER = 'upload/'

app = Flask(__name__)
app.config.from_object(__name__)

valores = []
cantidad = ''
sumatoria = ''
media = ''
rango = ''
desvio_estandar = ''
limites_control = ''
datos_estadisticos = {}

LISTADO_ABC = []
TOTALES_ABC = {}
TOTALES_ABC_ACUM = []
TOTALES_ABC_ACUM_JSON = []
TOTALES = ''
totales = ''
TOTAL = 0
grupos = {}

inventario = ''
bom = ''
mrp = ''


def leer_csv_inventario(archivo):
    global inventario
    reader = csv.reader(open(archivo, 'rb'))
    inventario = Inventario()
    listado = []

    for row in reader:
        listado.append(row)

    inventario.cargar_inventario(listado)


def leer_csv_bom(archivo):
    global bom
    reader = csv.reader(open(archivo, 'rb'))
    bom = Bom()
    listado = []
    for row in reader:
        listado.append(row)

    bom.cargar_bom(listado)


def calcular_mrp():
    global mrp, bom, inventario
    mrp = Mrp()
    mrp.calucar_necesidades(bom, inventario, cantidad)
    return mrp.obtener_necesidades()


def es_archivo_permitido(archivo):
    "Retorna True si el archivo indicado se puede subir al servidor."
    return '.' in archivo and archivo.endswith('csv')


# Vistas
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/abc_min.csv', methods=['GET'])
def ejemplo():
  response = make_response(open('abc_min.csv').read())
  response.headers["Content-type"] = "text/plain"
  response.headers['Content-disposition'] = 'attachment';
  return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = u'Nombre de usuario inválido'
        elif request.form['password'] != app.config['PASSWORD']:
            error = u'Contraseña inválida'
        else:
            session['logged_in'] = True
            flash(u'Se encuentra logueado en la aplicación!')
        return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash(u'Está deslogueado de la aplicación')
    return redirect(url_for('home'))


@app.route('/abc')
def abc():
    return render_template('abc.html')


@app.route('/abc_subir_archivo', methods=['POST'])
def abc_subir_archivo():
    global LISTADO_ABC, TOTALES, TOTALES_ABC_ACUM_JSON
    if not session.get('logged_in'):
        abort(401)

    if request.method == 'POST':
        file = request.files['archivo']
        if file and es_archivo_permitido(file.filename):
            filename = file.filename
            file.save(os.path.join(UPLOADS_FOLDER, filename))
            abc = Abc()
            abc.leer_csv_abc(os.path.join(UPLOADS_FOLDER, filename))
            abc.calcular_totales()
            flash(u'Datos analizados')
            return render_template('abc_grafico.html',
                                   totales = abc.TOTALES_ABC,
                                   totales_acum = abc.TOTALES_ABC_ACUM_JSON,
                                   monto_total = abc.TOTAL,
                                   grupos = abc.grupos)
        else:
            flash(u"El archivo %s no es un archivo válido" %
                  (file.filename), "error")
            return render_template('archivo_subido.html')

    return render_template('archivo_subido.html')



@app.route('/mrp')
def mrp():
    return render_template('mrp.html')


@app.route('/mrp_enviar_datos', methods=['POST'])
def mrp_enviar_datos():
    if not session.get('logged_in'):
        abort(401)

    if request.method == 'POST':
        file_inventario = request.files['archivo_inventario']
        file_bom = request.files['archivo_bom']
        global cantidad

        if file_inventario and es_archivo_permitido(file_inventario.filename):
            filename = file_inventario.filename
            file_inventario.save(os.path.join(UPLOADS_FOLDER, filename))
            leer_csv_inventario(os.path.join(UPLOADS_FOLDER, filename))
        else:
            flash(u"El archivo %s no es un archivo válido" %
                  (file_inventario.filename), "error")

        if file_bom and es_archivo_permitido(file_bom.filename):
            filename = file_bom.filename
            file_bom.save(os.path.join(UPLOADS_FOLDER, filename))
            leer_csv_bom(os.path.join(UPLOADS_FOLDER, filename))
        else:
            flash(u"El archivo %s no es un archivo válido" %
                  (file_bom.filename), "error")

        cantidad = int(request.form.values()[0])
        necesidades = calcular_mrp()
        return render_template('mrp_datos_subidos.html', necesidades = necesidades)


if __name__ == "__main__":
    app.run()

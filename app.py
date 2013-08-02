# -*- coding: utf-8 -*-


# all the imports
from flask import Flask, request, session, g, redirect, url_for,\
    abort, render_template, flash

import os
import csv
from operator import itemgetter, attrgetter
import json
from Inventario import *
from Bom import *
from Mrp import *

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


def leer_csv_abc(archivo):
    global TOTALES, TOTALES_ABC, LISTADO_ABC
    reader = csv.reader(open(archivo, 'rb'))
    for row in reader:
        LISTADO_ABC.append(row)


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


def calcular_totales(listado):
    global TOTALES, TOTALES_ABC, TOTAL, TOTALES_ABC_ACUM_JSON, grupos
    TOTALES_ABC = {}
    TOTALES_ABC_ACUM = []
    TOTALES_ABC_ACUM_JSON = []
    TOTALES = ''
    TOTAL = 0
    grupos = {}

    for row in listado:
        a = convertir_a_float(row[1]) * convertir_a_float(row[2])
        TOTALES_ABC[row[0]] = a
        TOTAL = TOTAL + a

    TOTALES_ABC = TOTALES_ABC.items()
    TOTALES_ABC = sorted(TOTALES_ABC, key=itemgetter(1), reverse=True)
    porcentaje = 0
    for total in TOTALES_ABC:
        porcentaje = porcentaje + (total[1]/TOTAL)
        TOTALES_ABC_ACUM.append((total[0], porcentaje))

    grupos = obtener_grupos(TOTALES_ABC_ACUM)

    TOTALES_ABC = json.dumps(TOTALES_ABC)
    TOTALES_ABC_ACUM_JSON = json.dumps(TOTALES_ABC_ACUM)


def obtener_grupos(acumulados):
    "Los productos que representan el 80%"

    productos_a = []
    por_a = 0
    productos_b = []
    por_b = 0
    productos_c = []
    por_c = 0

    for i in acumulados:
        por = i[1]
        if(por <= 0.80):
            productos_a.append(i[0])
            por_a = i[1]
        elif(por > 0.8 and por <= 0.9):
            productos_b.append(i[0])
            por_b = i[1]
        elif(por > 0.9):
            productos_c.append(i[0])
            por_c = i[1]

    resultado = {'a': [productos_a, round(por_a, 2)],
                 'b': [productos_b, round(por_b, 2)],
                 'c': [productos_c, round(por_c, 2)]}
    return resultado


def convertir_a_float(numero_str):
    nro = float(numero_str.replace(',', '.'))
    return nro


def es_archivo_permitido(archivo):
    "Retorna True si el archivo indicado se puede subir al servidor."
    return '.' in archivo and archivo.endswith('csv')


# Vistas
@app.route('/')
def home():
    return render_template('home.html')


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
        #import ipdb; ipdb.set_trace()
        file = request.files['archivo']
        if file and es_archivo_permitido(file.filename):
            filename = file.filename
            file.save(os.path.join(UPLOADS_FOLDER, filename))
            leer_csv_abc(os.path.join(UPLOADS_FOLDER, filename))
            calcular_totales(LISTADO_ABC)
            flash(u'Datos analizados')
            return render_template('abc_grafico.html', totales = TOTALES_ABC, totales_acum = TOTALES_ABC_ACUM_JSON, monto_total = TOTAL, grupos = grupos)
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

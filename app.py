# -*- coding: utf-8 -*-


# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for,\
    abort, render_template, flash
from contextlib import closing

from inspect import getmembers
from pprint import pprint
import os
import csv
from numpy import *

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


def leer_csv(archivo):
    reader = csv.reader(open(archivo, 'rb'))
    for row in enumerate(reader):
        valores.append(float(row[1][0]))

    cantidad = obtener_cantidad(valores)
    sumatoria = obtener_sumatoria(valores)
    media = obtener_media(valores)
    rango = obtener_rango(valores)
    desvio_estandar = obtener_desvio(valores)

    print cantidad
    print sumatoria
    print media
    print rango
    print desvio_estandar


def es_archivo_permitido(archivo):
    "Retorna True si el archivo indicado se puede subir al servidor."
    return '.' in archivo and archivo.endswith('csv')


def obtener_cantidad(valores):
    return len(valores)


def obtener_sumatoria(valores):
    return sum(valores)


def obtener_media(valores):
    if(len(valores) > 0):
        media = average(valores)
        return media


def obtener_rango(valores):
    v = array(valores)
    max = v.max()
    min = v.min()
    rango = max - min
    return rango


def obtener_desvio(valores):
    return std(valores)


# Vistas
@app.route('/')
def show_productos():
    #cur = g.db.execute('select id, nombre\
        #                   from productos order by id desc')
    productos = {'codigo': '1', 'nombre': 'Nombre'}
    return render_template('show_productos.html', productos=productos)


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
        return redirect(url_for('show_productos'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash(u'Está deslogueado de la aplicación')
    return redirect(url_for('show_productos'))


@app.route('/analizar_datos')
def analizar_datos():
    return render_template('analizar_datos.html')


@app.route('/subir_archivo', methods=['POST'])
def subir_archivo():
    if not session.get('logged_in'):
        abort(401)

    if request.method == 'POST':
        #import ipdb; ipdb.set_trace()
        file = request.files['archivo']
        if file and es_archivo_permitido(file.filename):
            filename = file.filename
            file.save(os.path.join(UPLOADS_FOLDER, filename))
            leer_csv(os.path.join(UPLOADS_FOLDER, filename))
            return render_template('archivo_subido.html')
        else:
            flash(u"El archivo %s no es un archivo válido" %
                  (file.filename), "error")
            return render_template('archivo_subido.html')

    return render_template('archivo_subido.html')


if __name__ == "__main__":
    app.run()

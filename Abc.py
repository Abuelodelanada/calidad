# -*- coding: utf-8 -*-

import csv
import json
from operator import itemgetter, attrgetter


class Abc():

    LISTADO_ABC = []
    TOTALES_ABC = {}
    TOTALES_ABC_ACUM = []
    TOTALES_ABC_ACUM_JSON = []
    TOTALES = ''
    TOTAL = 0
    grupos = {}

    def __init__(self, ):
        """
        """

    def __exit__(self, ):
        del self

    def convertir_a_float(self, numero_str):
        nro = float(numero_str.replace(',', '.'))
        return nro

    def leer_csv_abc(self, archivo):
        reader = csv.reader(open(archivo, 'rb'))
        for row in reader:
            self.LISTADO_ABC.append(row)

    def calcular_totales(self):

        for row in self.LISTADO_ABC:
            a = self.convertir_a_float(row[1]) * self.convertir_a_float(row[2])
            self.TOTALES_ABC[row[0]] = a
            self.TOTAL = self.TOTAL + a

        self.TOTALES_ABC = self.TOTALES_ABC.items()
        self.TOTALES_ABC = sorted(self.TOTALES_ABC, key=itemgetter(1),
                                  reverse=True)
        porcentaje = 0
        for total in self.TOTALES_ABC:
            porcentaje = porcentaje + (total[1]/self.TOTAL)
            self.TOTALES_ABC_ACUM.append((total[0], porcentaje))

        self.grupos = self.obtener_grupos(self.TOTALES_ABC_ACUM)
        self.TOTALES_ABC = json.dumps(self.TOTALES_ABC)
        self.TOTALES_ABC_ACUM_JSON = json.dumps(self.TOTALES_ABC_ACUM)
        print self.TOTALES_ABC

    def obtener_grupos(self, acumulados):
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

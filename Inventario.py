# -*- coding: utf-8 -*-


class Inventario():
    INVENTARIO = {}

    def __init__(self, ):
        self.INVENTARIO.clear()

    def cargar_inventario(self, listado):
        """
        Carga el inventario a partir de una lista de tuplas
        del tipo (codigo, cantidad)
        """

        for tupla in listado:
            self.INVENTARIO[tupla[0]] = tupla[1]

    def obtener_inventario(self):
        return self.INVENTARIO

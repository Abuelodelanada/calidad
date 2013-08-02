# -*- coding: utf-8 -*-


class Bom():
    BOM = {}

    def __init__(self, ):
        self.BOM.clear()

    def cargar_bom(self, listado):
        """
        Carga el BOM a partir de una lista de tuplas
        del tipo (codigo, cantidad)
        """

        for tupla in listado:
            codigo = tupla[0]
            cantidad = tupla[1]

            if codigo not in self.BOM:
                self.BOM[codigo] = int(cantidad)
            else:
                self.BOM[codigo] = self.BOM[codigo] + int(cantidad)

    def obtener_bom(self):
        return self.BOM

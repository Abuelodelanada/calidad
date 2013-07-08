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
            nivel = tupla[1]
            cantidad = tupla[2]

            if nivel not in self.BOM:
                self.BOM[nivel] = [(codigo, cantidad)]
            else:
                self.BOM[nivel].append((codigo, cantidad))

    def obtener_bom(self):
        return self.BOM
